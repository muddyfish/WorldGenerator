from ai_event_handler import AiEventHandler

class collide_wall(AiEventHandler):
  def __init__(self):
    self.listeners = []
    self.listener_funcs = []
  
  def add_listener(self, entity, on_called):
    self.listeners.append(entity)
    self.listener_funcs.append(on_called)
    
  def is_called(self, entity):
    if entity not in self.listeners: return False
    self.listener_funcs[self.listeners.index(entity)]()