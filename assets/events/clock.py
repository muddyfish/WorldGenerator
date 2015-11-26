#!/usr/bin/env python

import time, __main__

class Clock(object):
    def __init__(self):
        self.no_ticks = 0
        self.time_methods = {"time": time.time,
                             "clock": time.clock}
        self.config_manager = __main__.main_class.config_manager
        self.timer = self.config_manager["video_config"]["timer"]
        self.get_time = self.time_methods[self.timer]
        self.time = self.old_time = self.start_time = self.get_time()
    
    def tick(self):
        self.no_ticks += 1
        self.old_time = self.time
        self.time = self.get_time()
        self.d_time = self.time - self.old_time
        return self.d_time