#!/usr/bin/env python
import __main__

class ResizableSurface(object):
  def __init__(self, surface):
    self.surf = surface
    self.surfrect = self.surf.get_rect()
    self.dx = 0
    self.dy = 0
  
  def __getattr__(self, attr):
    try: return super(ResizableSurface, self).__getattr__(attr)
    except AttributeError: return getattr(self.surf, attr)
  
  def blit(self, surf, pos, *args):
    pos = (pos[0]+self.dx, pos[1]+self.dy)
    blitrect = surf.get_rect(topleft = pos)
    if self.surfrect.contains(blitrect):
      return self.surf.blit(surf, pos, *args)
    topleft = blitrect.topleft
    resized_rect = self.surfrect.union(blitrect)
    oldsurf = self.surf
    self.surf = __main__.pygame.surface.Surface(resized_rect.size, __main__.pygame.SRCALPHA)
    if -1 in map(cmp, topleft, (0,0)):
      self.surf.blit(oldsurf, (-topleft[0], -topleft[1]))
      self.dx += topleft[1]
      self.dy += topleft[0]
      return self.surf.blit(surf, (0,0))
    else:
      self.surf.blit(oldsurf, (0,0))
      return self.surf.blit(surf, (topleft[0], topleft[1]))