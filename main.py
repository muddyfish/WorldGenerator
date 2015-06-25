#Import modules
import pygame
import sys, os

import assets.config.config_manager
import assets.events.event_manager
import assets.ui.subscription_manager
import assets.ui.screen

CAPTION = "Dungeon"

class Main(object):
  def __init__(self):
    self.args = sys.argv
  
  def init_config_manager(self):
    self.config_manager = assets.config.config_manager.ConfigManager()
    self.fps_limit = self.config_manager["video_config","fps_limit"]
  
  def init_event_manager(self):
    self.event_manager = assets.events.event_manager.EventManager()
    self.event_manager.add_events()
  
  def init_screen(self):
    pygame.init()
    self.screen = assets.ui.screen.Screen(pygame.display.set_mode(*self.config_manager.get_screen_properties()))
    pygame.display.set_caption(CAPTION)
    self.clock = pygame.time.Clock()
    self.screen.blit_all()
    
  def init_subscription_manager(self):
    self.subscription_manager = assets.ui.subscription_manager.SubscriptionManager()
    
  def run(self):
    while 1:
      self.clock.tick(self.fps_limit)
      self.event_manager.parse_events(pygame.event.get())
      self.subscription_manager.run_subscription()
#      fps = self.fps_font.render("FPS: %d" %(int(self.clock.get_fps())), True, (255,255,255))
#      self.screen.blit(fps, (10, 30))
      self.update_screen()

  def update_screen(self):
    pygame.display.update(self.screen.blit_rects_old)
    pygame.display.update(self.screen.blit_rects)
    self.screen.blit_rects_old = self.screen.blit_rects
    self.screen.blit_rects = [] 

if __name__ == "__main__":
  os.environ['SDL_VIDEO_CENTERED'] = '1'
  if "debug" in sys.argv:
    try: import cProfile as profile
    except ImportError: import profile
    profile.run('main()')
  else:
    main_class = Main()
    main_class.init_config_manager()
    main_class.init_event_manager()
    main_class.init_screen()
    main_class.init_subscription_manager()
    main_class.run()
