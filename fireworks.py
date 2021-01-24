#!/usr/bin/env python3
# An implementation using the rpi_ws281x library.
# Based on examples provided by: https://github.com/jgarff/rpi_ws281x

import time
from rpi_ws281x import *
import argparse
import random

# LED strip configuration:                                                                                                                                              
LED_COUNT      = 329     # Number of LED pixels.                                                                                                                        
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).                                                                                             
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)                                                                                               
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)                                                                                            
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest                                                                                                   
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)                                                                            
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
	
def allPixels(strip, color):
    for pixel in range(strip.numPixels()):
        strip.setPixelColor(pixel, color)
    strip.show()

def radiate(strip, color, index, radius):
    strip.setPixelColor(index-radius, color)
    strip.setPixelColor(index+radius, color)
    strip.show()
	
def animate(strip, index, radius):
    colorList = colorSequence(radius)
    for radial in range(0, radius+1):
        radiate(strip, colorList[radial], index, radial)
        time.sleep(20/1000.0)

def colorSequence(length):
    step = int(255 / length)
    colorList = [[],[],[]]
    for graduation in range(0, length + 1):
        colorList[0].append(Color(255, 255 - step * graduation, 255 - step * graduation))
    for graduation in range(0, length + 1):
        colorList[1].append(Color(255 - step * graduation, 255, 255 - step * graduation))
    for graduation in range(0, length + 1):
        colorList[2].append(Color(255 - step * graduation, 255 - step * graduation, 255))
    return colorList[random.randint(0,2)]
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print ('Press Ctrl-C to quit.')
    try:
        while True:
            allPixels(strip, Color(0, 0, 0))
            for iteration in range(10):
                random.seed()
                radius = random.randint(4,50)
                index = random.randint(radius,LED_COUNT-radius)
                animate(strip, index, radius)
                time.sleep(1000/1000.0)
		
    except KeyboardInterrupt:
        allPixels(strip, Color(0, 0, 0))
