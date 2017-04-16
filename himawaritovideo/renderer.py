# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess

from .config import get_config


FFMPEG_BIN = 'ffmpeg'


class Renderer(object):
	def __init__(self):
		self.__config = get_config()
		self.__ffmpeg = None

	def render_video(self, frames):
		for frame in frames:
			self.__render_frame(frame)

	def flush(self):
		self.__ffmpeg.stdin.close()
		self.__ffmpeg.wait()
		self.__ffmpeg = None

	def __render_frame(self, frame):
		if self.__ffmpeg is None:
			self.__initialize_ffmpeg(frame.size)
		self.__ffmpeg.stdin.write(frame.tobytes())

	def __initialize_ffmpeg(self, resolution):
		command = [
			FFMPEG_BIN,
			'-f', 'rawvideo',
			'-s', '%dx%d' % (resolution),
			'-pix_fmt', 'rgb24',
			'-i', '-',
			'-an',
		]
		if self.__config.forwarded_args:
			command += self.__config.forwarded_args
		else:
			command += [
				'-y',
				'-r', '25',
				'-crf', '22',
				'-c:v', 'libx264',
				'-pix_fmt', 'yuv420p',
				'-preset', 'placebo',
				'-level', '5.2',
			]
		command.append(self.__config.output)
		self.__ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE)
