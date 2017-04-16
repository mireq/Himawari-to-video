=================
Himawari-to-video
=================

.. image:: https://raw.githubusercontent.com/wiki/mireq/Himawari-to-video/logo.jpg

This program creates video from himawari sattelite images.

Requirements
^^^^^^^^^^^^

* requests - https://pypi.python.org/pypi/requests
* Pillow - https://pypi.python.org/pypi/Pillow
* working ffmpeg

Usage
-----

.. code::
	main.py [-h] [--start-date START_DATE] [--frames FRAMES]
	               [--resolution {1,2,4,8,16,20}] [--output OUTPUT]
	
	Download himawari8 images and make video
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --start-date START_DATE
	                        Start date
	  --frames FRAMES       Number of frames
	  --resolution {1,2,4,8,16,20}
	                        Resolutin of downloaded frames
	  --output OUTPUT       Output file


To adjust ffmpeg parameters call this program with additional `--` followed with
fffmpeg arguments.

To make 4K video call:

`python main.py --start-date 2017-01-01 --frames 1500 --resolution 4 -- -y -r 25
-crf 22 -c:v libx264 -pix_fmt yuv420p -preset placebo -level 5.0 -vf
crop=2200:2160:20:20,pad=4096:2160:968:0`
