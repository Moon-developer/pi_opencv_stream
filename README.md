# pi_security_opencv_stream
Using Raspberry Pi 3 with Stretch Lite to detect objects as smoothly as possible and output a stream.

## ABOUT

This project was put together using guides written by Adrian on www.pyimagesearch.com along with guides written by Migual on blog.miguelgrinberg.com. The challenge was getting everything setup on a Raspberry Pi 3 using Stretch Lite OS. Once opencv was setup the second challeng was to capture a camera rtsp stream, process it thru opencv to recognize the objects and then output a stream for clien side to access. All of this to run locally on the pi at optimal speeds.

## Dependency

The following was required for this project
```
opencv
flask
python
imutils
numpy
argparse
```

## Setup for intense\_version

Follow the guide on pyimagesearch to setup opencv on a raspberry pi in a python enviroment.  
Once you're setup run the following while in the python enviroment you created following the tutorials.
```
python main.py --prototext <prototext_here> --model <caffemodel_here> -ip <your_local_ip>
```
this will start the server.  
To view the stream click on a prefered browser and enter the following URL into it.
```
http://<IP given>:5000
```
give it a second to start processing the stream and you should see a "live" object detection stream.

## Setup for light\_version

Follow the guide on pyimagesearch to setup opencv on a raspberry pi in a python enviroment.  
Once you're setup run the following while in the python enviroment you created following the tutorials.
```
python main.py --cascade <chosen_cascade> -ip <your_local_ip>
```
this will start the server.  
To view the stream click on a prefered browser and enter the following URL into it.
```
http://<IP given>:5000
```
give it a second to start processing the stream and you should see a "live" object detection stream.

## NOTES

if you're trying to run this on a macOS and it complains about a fork() issue run the following command
```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```
the new macOS comes with a security update that affect the way fork() works.

## Versions

![Marks](https://img.shields.io/badge/Raspberry%20Pi-3%20B-blue.svg)
![Marks](https://img.shields.io/badge/Raspbian-Stretch%20Lite-blue.svg)
![Marks](https://img.shields.io/badge/OpenCV-4.0.0-orange.svg)
![Marks](https://img.shields.io/badge/license-MIT-orange.svg)
![Marks](https://img.shields.io/pypi/pyversions/Django.svg)
![Marks](https://img.shields.io/pypi/status/Django.svg)
