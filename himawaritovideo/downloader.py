# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import timedelta
from multiprocessing.dummy import Pool as ThreadPool

import requests
from PIL import Image, ImageChops

from .config import get_config


class EmptyImageException(Exception):
	pass


class Downloader(object):
	SECONDS_BETWEEN_FRAMES = 600
	IMAGE_RESOLUTION = 550
	POOL_SIZE = 16

	def __init__(self):
		self.config = get_config()
		self.start_date = self.config.start_date
		self.downloader_pool = ThreadPool(processes=self.POOL_SIZE)
		self.empty_image = Image.open(open(os.path.join(os.path.dirname(__file__), 'empty.png'), 'rb'), 'r')

	def get_urls(self, frame_date):
		url_template = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/{resolution}d/550/{year}/{month}/{day}/{hour}{minute}00_{x}_{y}.png'
		year, month, day, hour = frame_date.strftime('%Y.%m.%d.%H').split('.')
		minute = str(frame_date.minute // 10 * 10).zfill(2)
		context = {
			'resolution': self.config.resolution,
			'year': year,
			'month': month,
			'day': day,
			'hour': hour,
			'minute': minute,
		}
		for x in range(self.config.resolution):
			for y in range(self.config.resolution):
				context['x'] = x
				context['y'] = y
				yield url_template.format(**context)

	def compose_image(self, urls):
		urls = list(urls)
		s = self.IMAGE_RESOLUTION * self.config.resolution
		im = Image.new('RGB', (s, s))
		try:
			responses = self.downloader_pool.map(lambda url: requests.get(url, stream=True), urls)
			for i, response in enumerate(responses):
				part = Image.open(response.raw)
				if ImageChops.difference(self.empty_image, part).getbbox() is None:
					raise EmptyImageException()
				im.paste(part, ((i // self.config.resolution) * self.IMAGE_RESOLUTION, (i % self.config.resolution) * self.IMAGE_RESOLUTION))
		except EmptyImageException:
			return None
		except Exception as e:
			print(e)
			return None
		print(urls)
		im.save('/dev/shm/test.png')
		return im

	def __iter__(self):
		for i in range(self.config.frames):
			frame_date = self.start_date + timedelta(seconds=i*self.SECONDS_BETWEEN_FRAMES)
			img = self.compose_image(self.get_urls(frame_date))
			if img is not None:
				yield img
