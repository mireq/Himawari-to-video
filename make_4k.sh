#!/bin/sh
python main.py --start-date 2017-01-01 --frames 1500 --resolution 4 -- -y -r 25 -crf 22 -c:v libx264 -pix_fmt yuv420p -preset placebo -level 5.0 -vf crop=2160:2160:20:20,pad=4096:2160:968:0
