"""
Simple module that allows access to all images in a deeper folder
"""
import pathlib
import pygame
import os
import re


class ImageLoader:

    instance = None
    class _ImageLoader:

        def __init__(self, pathToimages):
            self._images = {}
            for (dirpath, dirnames, filenames) in  os.walk(pathToimages):
                self._images.update({filename.split('.')[0]: os.path.join(dirpath, filename) for filename in filenames if filename.endswith('png')})

        def __getattr__(self, imageName):
            return pygame.image.load(self._images[imageName]).convert_alpha()

    def __init__(self, arg):
        if not ImageLoader.instance:
            ImageLoader.instance = _ImageLoader(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
