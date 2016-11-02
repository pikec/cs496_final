#!/usr/bin/env python
#
#Candis Pike
#API assignment CS496S'16
#code ideas adapted from lecture 

from google.appengine.ext import ndb

#necessary to transfer keys to JSON data
class Model(ndb.Model):
  def to_dict(self):
    d = super(Model, self).to_dict()
    d['key'] = self.key.id()
    return d

class User(ndb.Model):
	name = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	token = ndb.IntegerProperty(required=True)
	
class Projects (ndb.Model):
		user = ndb.KeyProperty(kind=User, required=True)
		title = ndb.StringProperty(required=True)
		description = ndb.StringProperty(required=False)
		commisioned = ndb.StringProperty(required=False)
		whom = ndb.StringProperty(required=False)
			
		def to_dict(self):
			d = super(Projects, self).to_dict()
			d['user'] = self.key.id()
			return d