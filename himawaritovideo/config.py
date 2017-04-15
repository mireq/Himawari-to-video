# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import itertools
import sys
from datetime import datetime, timedelta


def argument_to_date(s):
	try:
		return datetime.strptime(s, "%Y-%m-%d")
	except ValueError:
		try:
			return datetime.strptime(s, "%Y-%m-%d %H:%M")
		except ValueError:
			msg = "Not a valid date: '{0}'.".format(s)
			raise argparse.ArgumentTypeError(msg)


class ConfigRegistry(object):
	def __init__(self):
		parser = argparse.ArgumentParser(description="Download himawari8 images and make video")
		parser.add_argument('--start-date', type=argument_to_date, dest='start_date', help="Start date")
		parser.add_argument('--frames', type=int, dest='frames', help="Number of frames")
		parser.add_argument('--resolution', type=int, dest='resolution', help="Resolutin of downloaded frames", choices=[1, 2, 4, 8, 16, 20])
		parser.add_argument('--output', dest='output', help="Output file")
		parser.set_defaults(start_date=datetime.now() - timedelta(days=1), frames=144, resolution=1, output='video.mkv')
		args = parser.parse_args(list(itertools.takewhile(lambda arg: arg != '--', sys.argv[1:])))
		forwarded_args = list(itertools.dropwhile(lambda arg: arg != '--', sys.argv[1:]))[1:]

		self.start_date = args.start_date
		self.frames = args.frames
		self.resolution = args.resolution
		self.output = args.output
		self.forwarded_args = forwarded_args

	def __repr__(self):
		return repr({'start_date': self.start_date, 'frames': self.frames, 'resolution': self.resolution, 'output': self.output})


def get_config():
	if get_config.registry is None:
		get_config.registry = ConfigRegistry()
	return get_config.registry
get_config.registry = None
