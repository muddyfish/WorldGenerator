#Import modules
import pygame
import sys, os

import assets.config.config_manager
import assets.events.event_manager
import assets.events.ai_event_manager
import assets.font.font_manager
import assets.ui.subscription_manager
import assets.ui.screen
import assets.ui.keyboard_injector
import assets.entity.entity_manager
import assets.databin

#import random
#random.seed(10)

CAPTION = "Mystery Dungeon"

class Main(object):
  def __init__(self):
    self.args = sys.argv
    self.debug = "debug" in self.args
  
  def init_databin(self):
    self.databin = assets.databin.Databin()
  
  def init_config_manager(self):
    self.config_manager = assets.config.config_manager.ConfigManager()
    self.fps_limit = self.config_manager["video_config","fps_limit"]
    self.show_fps = self.config_manager["video_config", "show_fps"]
    if not self.show_fps:
      self.blit_fps = lambda: None
  
  def init_screen(self):
    pygame.init()
    self.screen = assets.ui.screen.Screen(pygame.display.set_mode(*self.config_manager.get_screen_properties()), pygame)
    pygame.display.set_caption(CAPTION)
    if self.config_manager["video_config"]["screen_properties"]["fullscreen"]:
      pygame.mouse.set_visible(False)
    self.screen.blit(self.screen.old_im_load(os.path.join("assets", "loading.png")), (0,0))
    self.update_screen()
    self.clock = pygame.time.Clock()
    
  def init_event_manager(self):
    self.event_manager = assets.events.event_manager.EventManager()
    self.event_manager.add_events()
    
  def init_keyboard_injector(self):
    self.keyboard_injector = assets.ui.keyboard_injector.KeyboardInjector()
  
  def init_ai_event_manager(self):
    self.ai_event_manager = assets.events.ai_event_manager.AiEventManager()
    self.ai_event_manager.add_events()
  
  def init_entity_manager(self):
    self.entity_manager = assets.entity.entity_manager.EntityManager()
  
  def init_font_manager(self):
    self.fonts = assets.font.font_manager.FontManager()
    self.fonts.register_font("fps", "verdana", 12)
  
  def init_subscription_manager(self):
    debug("Creating subscription manager...")
    self.subscription_manager = assets.ui.subscription_manager.SubscriptionManager()
    debug("Loading subscription...")
    self.subscription_manager.load_subscription()
    
  def run(self):
    while 1:
      self.keyboard_injector.run()
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
    self.screen.blit(fps, (10, 30))#, no_scale = True)

  def update_screen(self):
    pygame.display.update(self.screen.blit_rects_old)
    pygame.display.update(self.screen.blit_rects)
    self.screen.blit_rects_old = self.screen.blit_rects
    self.screen.blit_rects = []

def debug(txt):
  if "debug" in sys.argv:
    print txt

def main():
  global main_class
  debug("Creating main...")
  main_class = Main()
  debug("Initialising databin...")
  main_class.init_databin()
  debug("Initialising config manager...")
  main_class.init_config_manager()
  debug("Initialising screen...")
  main_class.init_screen()
  debug("Initialising event manager...")
  main_class.init_event_manager()
  debug("Initialising keyboard injector...")
  main_class.init_keyboard_injector()
  debug("Initialising ai event manager...")
  main_class.init_ai_event_manager()
  debug("Initialising entity manager...")
  main_class.init_entity_manager()
  debug("Initialising font manager...")
  main_class.init_font_manager()
  debug("Initialising subscription manager...")
  main_class.init_subscription_manager()
  debug("Starting the mainloop...")
  main_class.run()


if __name__ == "__main__":
  os.environ['SDL_VIDEO_CENTERED'] = '1'
  if "debug" in sys.argv:
    try: import cProfile as profile
    except ImportError: import profile
    profile.run('main()')
  else:
    main()