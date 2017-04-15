# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import himawaritovideo


def main():
	downloader = himawaritovideo.Downloader()
	renderer = himawaritovideo.Renderer()
	renderer.render_video(downloader)


if __name__ == "__main__":
	main()
