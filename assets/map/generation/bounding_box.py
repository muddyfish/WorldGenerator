#!/usr/bin/env python

class BBox(object):
    """A basic bounding box"""
    def __init__(self, offsets):
        self.offsets = offsets
        
    def __str__(self):
        return str(self.offsets)
