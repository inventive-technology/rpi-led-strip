#!/usr/bin/env python3
# An implementation using the rpi_ws281x library.
# Based on examples provided by: https://github.com/jgarff/rpi_ws281x

import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 329     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def everyN(strip, color, n, wait_ms=10):
    """Same colour, every n pixels."""
    for pixel in range(0, strip.numPixels(), n):
        strip.setPixelColor(pixel, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Scan from R to L in white, then repeat turning off
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            everyN(strip, Color(0, 0, 0), 1, 1)
            time.sleep(1000/1000.0)
            everyN(strip, Color(255, 255, 255), 1, 1)
            time.sleep(1000/1000.0)

    except KeyboardInterrupt:
        everyN(strip, Color(0,0,0), 1, 10)
