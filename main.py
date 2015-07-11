#Import modules
import pygame
import sys, os

import assets.config.config_manager
import assets.events.event_manager
import assets.font.font_manager
import assets.ui.subscription_manager
import assets.ui.screen
#import random
#random.seed(10)

CAPTION = "Mystery Dungeon"

class Main(object):
  def __init__(self):
    self.args = sys.argv
  
  def init_config_manager(self):
    self.config_manager = assets.config.config_manager.ConfigManager()
    self.fps_limit = self.config_manager["video_config","fps_limit"]
    self.show_fps = self.config_manager["video_config", "show_fps"]
    if not self.show_fps:
      self.blit_fps = lambda: None
  
  def init_event_manager(self):
    self.event_manager = assets.events.event_manager.EventManager()
    self.event_manager.add_events()
  
  def init_screen(self):
    pygame.init()
    self.screen = assets.ui.screen.Screen(pygame.display.set_mode(*self.config_manager.get_screen_properties()))
    pygame.display.set_caption(CAPTION)
    self.clock = pygame.time.Clock()
    self.screen.blit_all()
  
  def init_font_manager(self):
    self.fonts = assets.font.font_manager.FontManager()
    self.fonts.register_font("fps", "verdana", 12)
  
  def init_subscription_manager(self):
    self.subscription_manager = assets.ui.subscription_manager.SubscriptionManager()
    
  def run(self):
    while 1:
      self.event_manager.parse_events(pygame.event.get())
      self.subscription_manager.run_subscription()
      self.clock.tick(self.fps_limit)
      self.blit_fps()
      self.update_screen()

  def blit_fps(self):
    try:
      count = int(self.clock.get_fps())
    except OverflowError:
      count = "Infinate?"
    fps = self.fonts["fps"].render("FPS: %s" %(count), True, (255,255,255))
    self.screen.blit(fps, (10, 30))

  def update_screen(self):
    #pygame.display.update(self.screen.blit_rects_old)
    pygame.display.update(self.screen.blit_rects)
    self.screen.blit_rects_old = self.screen.blit_rects
    self.screen.blit_rects = [] 

def main():
  global main_class
  main_class = Main()
  main_class.init_config_manager()
  main_class.init_event_manager()
  main_class.init_screen()
  main_class.init_font_manager()
  main_class.init_subscription_manager()
  main_class.run()


if __name__ == "__main__":
  os.environ['SDL_VIDEO_CENTERED'] = '1'
  if "debug" in sys.argv:
    try: import cProfile as profile
    except ImportError: import profile
    profile.run('main()')
  else:
    main()