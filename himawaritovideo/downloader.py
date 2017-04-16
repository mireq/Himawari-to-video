# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import timedelta
from multiprocessing.dummy import Pool as ThreadPool

import requests
from PIL import Image, ImageChops

from .config import get_config


SECONDS_BETWEEN_FRAMES = 600
IMAGE_RESOLUTION = 550
POOL_SIZE = 16


class EmptyImageException(Exception):
	pass


class Downloader(object):

	def __init__(self):
		self.__config = get_config()
		self.__start_date = self.__config.start_date
		self.__downloader_pool = ThreadPool(processes=POOL_SIZE)
		self.__empty_image = Image.open(open(os.path.join(os.path.dirname(__file__), 'empty.png'), 'rb'), 'r').convert('RGB')

	def __get_urls(self, frame_date):
		url_template = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/{resolution}d/550/{year}/{month}/{day}/{hour}{minute}00_{x}_{y}.png'
		year, month, day, hour = frame_date.strftime('%Y.%m.%d.%H').split('.')
		minute = str(frame_date.minute // 10 * 10).zfill(2)
		context = {
			'resolution': self.__config.resolution,
			'year': year,
			'month': month,
			'day': day,
			'hour': hour,
			'minute': minute,
		}
		for x in range(self.__config.resolution):
			for y in range(self.__config.resolution):
				context['x'] = x
				context['y'] = y
				yield url_template.format(**context)

	def __compose_image(self, urls):
		s = IMAGE_RESOLUTION * self.__config.resolution
		im = Image.new('RGB', (s, s))
		try:
			responses = self.__downloader_pool.map(lambda url: requests.get(url, stream=True), urls)
			for i, response in enumerate(responses):
				part = Image.open(response.raw).convert('RGB')
				if ImageChops.difference(self.__empty_image, part).getbbox() is None:
					raise EmptyImageException()
				im.paste(part, ((i // self.__config.resolution) * IMAGE_RESOLUTION, (i % self.__config.resolution) * IMAGE_RESOLUTION))
		except EmptyImageException:
			return None
		except Exception as e:
			print(e)
			return None
		return im

	def __iter__(self):
		for i in range(self.__config.frames):
			frame_date = self.__start_date + timedelta(seconds=i*SECONDS_BETWEEN_FRAMES)
			img = self.__compose_image(self.__get_urls(frame_date))
			if img is not None:
				yield img
