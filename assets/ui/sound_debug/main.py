#!/usr/bin/env python

from ..ui import UI

class SoundDebug(UI):
  def __init__(self):
    super(SoundDebug, self).__init__()
    self.config_manager = self.get_main().config_manager
    self.mixer = self.get_pygame().mixer
    path = self.config_manager.get_path(self.config_manager.parse_path("assets.sound"), "Intro.wav")
    print path
    sound = self.mixer.Sound(path)
    sound.play()
    sound.set_volume(1)
    
  def draw(self):
    self.screen.fill((0,0,0))
    
  def run(self):
    pass