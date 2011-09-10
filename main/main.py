#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/09/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/09/09 $Date$"
import urllib2
import simplejson
# Skeleton Python Implemention of Random Art
# Adapted by Chris Stone from code by Andrew Farmer

import random, Image, math

random.seed()

# MISSING CODE: plotIntensity assumes there is a function evalExpr
#   that given an expression, and x and y coordinates, returns a
#   result in [-1,1].

def plotIntensity(exp, pixelsPerUnit = 150):
    """Return an grayscale image of the given function"""
    # Create a blank canvas
    canvasWidth = 2 * pixelsPerUnit + 1
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    # For each pixel in the canvas...
    for py in range(0, canvasWidth):
        for px in range(0, canvasWidth):
            # Convert pixel location to [-1,1] coordinates
            #  Note that x and y conversions are not exactly the same
            #  because increasing px goes left to right (increasing x)
            #  but increasing py goes from top to bottom (decreasing y)
            x = float(px - pixelsPerUnit) / pixelsPerUnit 
            y = -float(py - pixelsPerUnit) / pixelsPerUnit
            # Evaluate the expression at that point
            z = evalExpr(exp,x,y)
            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            canvas.putpixel((px,py), intensity)
    return canvas


def plotColor(redExp, greenExp, blueExp, pixelsPerUnit = 150):
    """Return an image constructed from the three RGB intensity functions"""
    redPlane   = plotIntensity(redExp, pixelsPerUnit)
    greenPlane = plotIntensity(greenExp, pixelsPerUnit)
    bluePlane  = plotIntensity(blueExp, pixelsPerUnit)
    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))

# MISSING CODE: makeGray and makeColor assume there is a function
#   buildExpr that produces a random expression, suitable for passing
#   to evalExpr.

def makeGray(numPics = 20):
    """Creates n grayscale image files named gray0.png, gray1.png, ...""" 
    random.seed()
    for i in range(0,numPics):
        print i, ":"
        grayExp = buildExpr()
        print str(grayExp), "\n"
        image = plotIntensity(grayExp)
        image.save("gray" + str(i) + ".png", "PNG")

def makeColor(numPics = 20):
    """Creates n color image files named color0.png, color1.png, ...""" 
    random.seed()
    for i in range(0,numPics):
        print i, ":"
        redExp = buildExpr()
        print "red = ", str(redExp)
        greenExp = buildExpr()
        print "green = ", str(greenExp)
        blueExp = buildExpr()
        print "blue = ", str(blueExp), "\n"
        image = plotColor(redExp, greenExp, blueExp)
        image.save("color" + str(i) + ".png", "PNG")


# Generate a bunch of random grayscale and color pictures.
makeGray();
makeColor();

# now have some fun with the results...
def main():
    url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=dx&key=ABQIAAAAqJEWmz1HqZQkHSnAZ_AX7RQ4fymw322orKfoXaRWVOGt8Sn9SBRqR7eeWq78y71L10jtRhrR6_SAFQ&userip=146.164.2.32')
    
    #request = urllib2.Request(url, None, {'Referer': 'www.ufrj.br'})
    #response = urllib2.urlopen(request)
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10 ( .NET CLR 3.5.30729)')
    #data = urllib2.urlopen(request)
    data = opener.open(request).read()
    print data
    return
    
    # Process the JSON string.
    results = simplejson.loads(data)
    for result in results['responseData']['results']:
        print result['url']
    return
    from jeppeto import Jeppeto
    from pygame_factory import GUI
    main = Jeppeto()
    main.inicia(GUI())
    
if __name__ == "__main__":
    main()

