# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess

from .config import get_config


FFMPEG_BIN = 'ffmpeg'


class Renderer(object):
	def __init__(self):
		self.config = get_config()
		self.ffmpeg = None

	def render_video(self, frames):
		for frame in frames:
			self.render_frame(frame)

	def render_frame(self, frame):
		if self.ffmpeg is None:
			self.initialize_ffmpeg(frame.size)
		self.ffmpeg.stdin.write(frame.tobytes())

	def initialize_ffmpeg(self, resolution):
		command = [
			FFMPEG_BIN,
			'-f', 'rawvideo',
			'-s', '%dx%d' % (resolution),
			'-pix_fmt', 'rgb24',
			'-i', '-',
			'-an',
		]
		if self.config.forwarded_args:
			command += self.config.forwarded_args
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
		command.append(self.config.output)
		self.ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE)

	def flush(self):
		self.ffmpeg.stdin.close()
		self.ffmpeg.wait()
		self.ffmpeg = None
