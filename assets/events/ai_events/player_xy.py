from ai_event_handler import AiEventHandler

class player_xy(AiEventHandler):
  def __init__(self):
    self.listeners = []
    self.listener_funcs = []
  
  def add_listener(self, entity, on_called):
    self.listeners.append(entity)
    self.listener_funcs.append(on_called)
    
  def is_called(self, entity):
    if entity not in self.listeners: return False
    player_rect, entity_rect = entity.get_player().rect, entity.rect
    if player_rect.left<entity_rect.centerx<player_rect.right:
      if player_rect.centery<entity_rect.centery:
        self.listener_funcs[self.listeners.index(entity)](0)
      else:
        self.listener_funcs[self.listeners.index(entity)](1)
    if  player_rect.top<entity_rect.centery<player_rect.bottom:
      if player_rect.centerx<entity_rect.centerx:
        self.listener_funcs[self.listeners.index(entity)](2)
      else:
        self.listener_funcs[self.listeners.index(entity)](3)