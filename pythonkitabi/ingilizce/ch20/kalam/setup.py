#!/usr/bin/env python

from distutils.core import setup

setup(name = "kalam",
      version = "1.0",
      description = "Kalam - the extensible Python editor",
      author = "Boudewijn Rempt",
      author_email = "boud@rempt.xs4all.nl",
      url = "http://www.valdyas.org",
      packages = ["charmap",
                  "kalamlib",
                  "typometer",
                  "workspace",
                  ""],
      data_files = [("kalam/data", ["data/Blocks.txt"]),
                    ("kalam/pixmaps", ["pixmaps/listspace.png",
                                       "pixmaps/splitspace.png",
                                       "pixmaps/stackspace.png",
                                       "pixmaps/tabmanager.png",
                                       "pixmaps/workspace.png"])],
      scripts = ["kalam","kalam.bat"],
      long_description = """
Kalam is a plain-text editor. It is written in Python using
the PyQt GUI toolkit as an example and tutorial for the book
GUI programming with Python and Qt, published by Opendocs.
"""          
      )    
