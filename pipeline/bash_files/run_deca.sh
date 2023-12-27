#!/bin/bash

cd $1
python demos/demo_video.py -i $2 --savefolder $3 --rasterizer_type=pytorch3d -a $4 --visualize True
