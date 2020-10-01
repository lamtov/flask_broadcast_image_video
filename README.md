# Simple Flask broadcast Image, Video 
Simple broadcast Image, Video  with the help of Flask and Opencv
## SETUP With conda
```bash
conda create -n demo  python=3.8
conda activate demo
conda  install  -y -c anaconda numpy
conda install   -y -c anaconda flask
conda install   -y -c conda-forge opencv
git clone https://github.com/lamtov/flask_broadcast_image_video.git
cd flask_broadcast_image_video/

python main.py
# for cloud vm only: sudo apt install libgl1-mesa-glx
```
## Preview Demo:
```bash
http://34.126.113.23:4009/
```
