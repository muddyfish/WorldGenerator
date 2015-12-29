#!/usr/bin/env python

from ..npc_base import NPC

class NPCHostile(NPC):
  must_kill = True
  no_respawn = True