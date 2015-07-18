#!/usr/bin/env python

class Databin(object):
    def __getattribute__(self, attr):
        try:
            return super(Databin, self).__getattribute__(attr)
        except AttributeError:
            db = Databin()
            super(Databin, self).__setattr__(attr, db)
            return db

    def __setattr__(self, name, value):
        super(Databin, self).__setattr__(name, value)