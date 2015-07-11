#!/usr/bin/env python

import pygame

class BasicSprite(pygame.sprite.DirtySprite):
  def __init__(self, surf, x,y, layer=0):
    pygame.sprite.DirtySprite.__init__(self)
    self.image = surf
    self.rect = self.image.get_rect()
    self.set_pos(x,y)
    self.layer = layer
    self.orig_x, self.orig_y = x,y
    
  def set_pos(self, x,y):
    self.x, self.y = self.rect.x, self.rect.y = x,y
    
  def move(self, dx, dy):
    self.x += dx
    self.y += dy
    self.rect.x += dx
    self.rect.y += dy