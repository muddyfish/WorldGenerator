#!/usr/bin/env python

from ..entity_base import Entity
from .resizable_surface import ResizableSurface
import xml.etree.ElementTree as ElementTree
import os, ast
import __main__

class Animation(Entity):
  anim_speed = 1.0/40
  finish_anim_funcs = {}
  auto_update = True
  transparent_colour = (255,255,255)
  auto_resize = True

  def __setattr__(self, attr, value):
    super(Animation, self).__setattr__(attr, value)
    if attr == "current_anim" and hasattr(self, "spritesheets") and self.auto_update: self.load_animation()
  
  def blit(self, x_mod=0, y_mod=0):
    try: self.get_blit()(self.surf, (self.x+x_mod, self.y+y_mod))
    except TypeError: self.get_blit()(self.surf.surf, (self.x+x_mod, self.y+y_mod))
  
  def load_animation_sheet(self, anim_name):
    config_manager = self.get_main().config_manager
    try:
      xml_tree = AnimationXML(ElementTree.parse(anim_name).getroot())
    except IOError:
      xml_tree = AnimationXML(ElementTree.parse(os.path.join(self.get_path(), anim_name)).getroot())    
    spritesheets = xml_tree["Content"]["Spritesheets"]["Spritesheet"]
    if not isinstance(spritesheets, list): spritesheets = [spritesheets]
    self.spritesheet_xml = {int(spritesheet.Id):spritesheet.Path for spritesheet in spritesheets}
    
    layers = xml_tree["Content"]["Layers"]["Layer"]
    if not isinstance(layers, list): layers = [layers]
    self.layers = {int(layer.Id):(layer.Name, int(layer.SpritesheetId)) for layer in layers}
    
    self.animation_xml = {animation.Name: animation for animation in xml_tree["Animations"]["Animation"]}
    
    self.default_anim = xml_tree["Animations"].DefaultAnimation
    self.current_anim = self.default_anim
    self.old_anim = None
    self.anim_state = 0
    self.anim_time = 0
    if not hasattr(self, "rotate_amount"): self.rotate_amount = 0

    self.load_spritesheets()    
    self.load_animation()
    #print self.frames
    
  def run_anim(self, d_time):
    total_anim_time = self.anim_speed*int(self.animation_xml[self.current_anim].FrameNum)
    old = self.anim_time <= total_anim_time
    self.anim_time += d_time
    new = self.anim_time <= total_anim_time
    if old and not new: # Has the animation just finished
      self.on_finish_anim()
      return
    elif self.old_anim != self.current_anim or new: # Is the current animation still playing
      if self.old_anim != self.current_anim:
        self.anim_state = 0
        self.anim_time = 0
      else:
        self.anim_state = int(self.anim_time/self.anim_speed)
      pygame = self.get_pygame()
      frames = []
      for frame in self.frames:
        if self.frames[frame]:
          delay = [int(f.attributes["Delay"]) for f in self.frames[frame]]
          f_id = 0
          for j in range(len(delay)):
            cur_delay = sum(delay[:j+1])
            if cur_delay > self.anim_state: break
            f_id = j
          frames.append(self.frames[frame][f_id])
      size = map(max, zip(*[frame.surf.get_size() for frame in frames]))
      self.surf = pygame.surface.Surface(size, pygame.SRCALPHA)
      if self.auto_resize: self.surf = ResizableSurface(self.surf)
      for frame in frames: self.surf.blit(frame.surf, [i[0]/2+i[1] for i in zip(size, frame.blit_pos)])
      if self.rotate_amount != 0:
        self.surf = pygame.transform.rotate(self.surf.surf, self.rotate_amount)
        if self.auto_resize: self.surf = ResizableSurface(self.surf)
    self.old_anim = self.current_anim
    if d_time == 0:
      self.bounding_rect = self.surf.get_bounding_rect()
      self.update_collision()
  
  def on_finish_anim(self):
    curr = self.current_anim
    if curr in self.finish_anim_funcs:
      self.finish_anim_funcs[curr]()
    if self.animation_xml[curr].Loop == "True":
      self.load_animation(curr)
    self.run_anim(0)
  
  def load_animation(self, new = None):
    self.frames = {}
    self.old_anim = ""
    if new is not None: self.current_anim = new
    layer_animations = self.animation_xml[self.current_anim]["LayerAnimations"]["LayerAnimation"]
    if not isinstance(layer_animations, list): layer_animations = [layer_animations]
    for layer_animation in layer_animations:
      if layer_animation.Visible == "True" and "Frame" in layer_animation:
        frames = layer_animation["Frame"]
        if not isinstance(frames, list): frames = [frames]
        self.frames[int(layer_animation.LayerId)] = map(AnimationFrame,
                                                        frames,
                                                        [int(layer_animation.LayerId)]*len(frames),
                                                        [self]*len(frames))
      else:
        self.frames[int(layer_animation.LayerId)] = []
  
  def load_spritesheets(self):
    try:
      self.spritesheets = {k: self.get_pygame().image.load(
          os.path.join(self.get_path(), "gfx", spritesheet))
        for k, spritesheet in self.spritesheet_xml.iteritems()}
    except self.get_pygame().error:
      self.spritesheets = {k: self.get_pygame().image.load(
          os.path.join(os.path.dirname(__main__.__file__), "assets", "gfx", spritesheet))
        for k, spritesheet in self.spritesheet_xml.iteritems()}

class AnimationXML(object):
  def __init__(self, xml_tree):
    self.xml_tree = xml_tree
    
  def __getattribute__(self, item):
    if item == "__dict__": return super(AnimationXML, self).__getattribute__("__dict__")
    if item in self.__dict__: return super(AnimationXML, self).__getattribute__(item)
    if item in self.xml_tree.__dict__: return getattr(self.xml_tree, item)
    return self.xml_tree.attrib[item]
  
  def __getitem__(self, item):
    if isinstance(item, int):
      return AnimationXML(self.xml_tree.getchildren()[item])
    rtn = [AnimationXML(i) for i in self.xml_tree.getchildren() if i.tag == item]
    if rtn == []: return
    if len(rtn) == 1: return rtn[0]
    return rtn
  
  def __contains__(self, value):
    return value in [i.tag for i in self.xml_tree.getchildren()]
  
  
  def __repr__(self):
    return self.tag+":\t"+str(self.xml_tree.attrib)+"\t["+", ".join([e.tag for e in self.xml_tree.getchildren()])+"]"

class AnimationFrame(object):
  hashes = {}
  
  def __init__(self, frame_xml, layer_id, parent):
    self.hash = hash(((tuple(frame_xml.xml_tree.attrib.items()), tuple(parent.spritesheet_xml.items()))))
    #print self.hash
    if self.hash in AnimationFrame.hashes:
      self.__dict__ = AnimationFrame.hashes[self.hash]
    else:
      self.attributes = {k:ast.literal_eval(v) for k,v in frame_xml.xml_tree.attrib.iteritems()}
      self.parent = parent
      self.layer_id = layer_id
      self.transparent_colour = parent.transparent_colour
      self.setup_frame()
      AnimationFrame.hashes[self.hash] = self.__dict__
  
  def setup_frame(self):
    pygame = self.parent.get_pygame()
    self.spritesheet = self.parent.spritesheets[self.parent.layers[self.layer_id][1]]
    self.layer_name = self.parent.layers[self.layer_id][0]
    if self.attributes["Visible"]:
      self.surf = self.spritesheet.subsurface(((self.attributes["XCrop"]*2,
                                                   self.attributes["YCrop"]*2),
                                                  (self.attributes["Width"]*2,
                                                   self.attributes["Height"]*2))).copy()      
      self.surf.set_colorkey(self.transparent_colour)
      scale = self.attributes["XScale"], self.attributes["YScale"]
      if (  self.attributes["RedTint"],
            self.attributes["GreenTint"],
            self.attributes["BlueTint"],
            self.attributes["AlphaTint"],
            scale) != \
         (255, 255, 255, 255, (100,100)):
        self.surf = self.surf.convert_alpha()
        self.surf.fill((self.attributes["RedTint"],
                        self.attributes["GreenTint"],
                        self.attributes["BlueTint"],
                        self.attributes["AlphaTint"]), None, pygame.BLEND_RGBA_MULT)
      if scale != (100, 100):
        self.surf = pygame.transform.smoothscale(self.surf,
                                             [abs(int(i[1]/100.0*i[0])) for i in zip(scale, self.surf.get_size())])
        if -1 in map(cmp, scale, (0,0)):
          self.surf = pygame.transform.flip(self.surf, scale[0]<0, scale[1]<0)
    else:
      self.surf = self.spritesheet.subsurface((0,0,0,0))
    self.blit_pos = (self.attributes["XPosition"]*2-self.surf.get_width()/2,
                     self.attributes["YPosition"]*2-self.surf.get_height()/2)
    