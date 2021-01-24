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

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for pixel in range(strip.numPixels()):
        strip.setPixelColor(pixel, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for iteration in range(iterations):
        for frame in range(3):
            for pixel in range(0, strip.numPixels(), 3):
                strip.setPixelColor(pixel+frame, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for pixel in range(0, strip.numPixels(), 3):
                strip.setPixelColor(pixel+frame, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for iteration in range(256*iterations):
        for pixel in range(strip.numPixels()):
            strip.setPixelColor(pixel, wheel((pixel+iteration) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for iteration in range(256*iterations):
        for pixel in range(strip.numPixels()):
            strip.setPixelColor(pixel, wheel((int(pixel * 256 / strip.numPixels()) + iteration) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for iteration in range(256):
        for frame in range(3):
            for pixel in range(0, strip.numPixels(), 3):
                strip.setPixelColor(pixel+frame, wheel((pixel+iteration) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for pixel in range(0, strip.numPixels(), 3):
                strip.setPixelColor(pixel+frame, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print ('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0))
            colorWipe(strip, Color(0, 255, 0))
            colorWipe(strip, Color(0, 0, 255))
            print ('Theater chase animations.')
            theaterChase(strip, Color(127, 127, 127))
            theaterChase(strip, Color(127,   0,   0))
            theaterChase(strip, Color(  0,   0, 127))
            print ('Rainbow animations.')
            rainbow(strip)
            rainbowCycle(strip)
            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
