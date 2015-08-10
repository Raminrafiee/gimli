#!/usr/bin/env python
# encoding: utf-8

"""
File: sidebar_gallery.py
Author: Florian Wagner <fwagner@gfz-potsdam.de>
Description: Add all examples/tutorials to sidebar gallery
Created on: 2013-10-13
"""

from __future__ import print_function
import os
from glob import glob
from os.path import abspath, join, dirname, basename
import random


SPHINXDOC_PATH='.'
TRUNK_PATH='..'
EXCLUDEBASE_PATH=''
DOC_BUILD_DIR=''

try:
    from _build.conf_environment import *
except:
    pass


###################
#  Path settings  #
###################

publish = os.getenv("PUBLISH")
if publish:
    build_dir = "http://www.pygimli.org"
else:
    build_dir = ""

example_dir = "examples"
tutorial_dir = "tutorials"
img_dir = join(build_dir, "_images")

# Get examples/tutorials
examples = glob(join(example_dir, "*/*plot*.py"))
tutorials = glob(join(tutorial_dir, "*/*plot*.py"))

# Get captions
def readRSTSecTitles(fname, verbose=False):
    """ Return list of section titles found in a given RST file. """
    import re
    rst_titles = re.compile(r"^(.+)\n+[-=]+\n", re.MULTILINE)
    with open(fname) as file:
        titles = re.findall(rst_titles, file.read())
        if verbose:
            print("File:", fname)
            print("Title:", titles)
    return titles

ex_titles = [readRSTSecTitles(ex)[0] for ex in examples]
tut_titles = [readRSTSecTitles(tut)[0] for tut in tutorials]
titles = ex_titles + tut_titles

# Adjust paths to output directory for html links
examples = [e.replace(example_dir, join(build_dir, "_examples_auto"))
            for e in examples]

tutorials = [t.replace(tutorial_dir, join(build_dir, "_tutorials_auto"))
             for t in tutorials]

# Create HTML gallery for sidebar with random start item
gallery = examples + tutorials
print("\nAdding %d examples/tutorials to sidebar gallery." % len(gallery))
print(titles)

html_top = """\
<!-- This file is automatically generated by sidebar_gallery.py -->
<div id="sidebar_example_gallery" class="carousel slide">
<div class="carousel-inner">"""

html_bottom = """\
</div>
<a class="carousel-control left" href="#sidebar_example_gallery" data-slide="prev">&lsaquo;</a>
<a class="carousel-control right" href="#sidebar_example_gallery" data-slide="next">&rsaquo;</a>
</div>"""

html_item = """\
<div class="item">
<a href="{}">
<img src="{}">
<div class="carousel-caption">
{}
</div>
</a>
</div>"""

id = random.randint(0, len(gallery) - 1)
items = []
for ix, (item, title) in enumerate(zip(gallery, titles)):
    dir = dirname(item)
    name = basename(item)
    url = join(dir, name.replace(".py", ".html"))
    img = join(img_dir, "sphx_glr_" + name.replace(".py", "_thumb.png"))
    item = html_item.format(url, img, title)

    if ix == id:
        item = item.replace("item", "active item")

    items.append(item)

items.insert(0, html_top)
items.append(html_bottom)
html = "\n".join(items)

with open("_templates/gallery.html", "w") as file:
   file.write(html)
