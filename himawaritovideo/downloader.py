# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
import requests
from PIL import Image

from .config import get_config


class Downloader(object):
	SECONDS_BETWEEN_FRAMES = 600
	IMAGE_RESOLUTION = 550

	def __init__(self):
		self.config = get_config()
		self.start_date = self.config.start_date

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
		s = self.IMAGE_RESOLUTION * self.config.resolution
		im = Image.new('RGB', (s, s))
		try:
			for i, url in enumerate(urls):
				response = requests.get(url, stream=True)
				part = Image.open(response.raw)
				im.paste(part, ((i // self.config.resolution) * self.IMAGE_RESOLUTION, (i % self.config.resolution) * self.IMAGE_RESOLUTION))
		except Exception as e:
			print(e)
			return im
		return im

	def __iter__(self):
		for i in range(self.config.frames):
			frame_date = self.start_date + timedelta(seconds=i*self.SECONDS_BETWEEN_FRAMES)
			yield self.compose_image(self.get_urls(frame_date))
