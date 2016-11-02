#!/usr/bin/env python
#
#Candis Pike
#API assignment CS496S'16
#code ideas adapted from lecture 
import webapp2
from google.appengine.ext import ndb
import db_models
import json
import datetime

class ProjectHandler(webapp2.RequestHandler):
	def post(self):
		token = self.request.get('token')
		if not token:
			self.response.set_status(404, "Token not found.")
			self.response.write(self.response.status)
			return
		tk = int(token)	
		kq = [x.token for x in db_models.User.query(db_models.User.token==tk).fetch()]
		
		if not kq:
			self.response.set_status(404, "Token not valid.")
			self.response.write(self.response.status)
			return	
			
		#create a new project - must be json format
		#Post Body:
		#user = reference to user 
		#title required
		#description
		#commisioned true or false
		#whom 
		#estimated
		
		#check for proper data format
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
			#create a project record
		title = self.request.get('title', default_value=None)
		description = self.request.get('descr', default_value=None)
		whom = self.request.get('whom', default_value = None)
		user = self.request.get('user', default_value = None)
		comm = self.request.get('comm', default_value = 'False')
		new_project = db_models.Projects()
		
		#check if title provided
		if title:
			new_project.title = title
	
		else:
			self.response.set_status(400,"Invalid Request. Title required.")
			self.response.write(self.response.status)
			return
		
		#check for user
		if user:
			new_project.user = ndb.Key(db_models.User, int(user))
	
		else:
			self.response.set_status(400,"Invalid Request. Project must be associated with a user.")
			self.response.write(self.response.status)
			return
			
		new_project.description = description
		new_project.commisioned = comm
		new_project.whom = whom
		key = new_project.put()
		out = new_project.to_dict()
		self.response.set_status(201, "New project created.")
		#self.response.write(self.response.status)
		self.response.write(json.dumps(out))		
		return
	
	#get list of project id's 	
	def get(self):
		token = self.request.get('token')
		if not token:
			self.response.set_status(404, "Token not found.")
			self.response.write(self.response.status)
			return
		tk = int(token)	
		kq = [x.token for x in db_models.User.query(db_models.User.token==tk).fetch()]
		
		if not kq:
			self.response.set_status(404, "Token not valid.")
			self.response.write(self.response.status)
			return	
		
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
		q = db_models.Projects.query()
		keys = q.fetch(keys_only=True)
		if not keys:
			self.response.set_status(400, "No projects to list.")
			self.response.write(self.response.status)
			return
		else:	
			results = {'keys': [x.id() for x in keys]}
			self.response.set_status(200)
			#self.response.write(self.response.status)	
			self.response.write(json.dumps(results))
			return

class OtherProjectHandler(webapp2.RequestHandler):
	#get project by pid
	def get(self, **kwargs):
		token = self.request.get('token')
		if not token:
			self.response.set_status(404, "Token not found.")
			self.response.write(self.response.status)
			return
			
		tk = int(token)	
		kq = [x.token for x in db_models.User.query(db_models.User.token==tk).fetch()]
		if not kq:
			self.response.set_status(404, "Token not valid.")
			self.response.write(self.response.status)
			return	
			
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
		results = db_models.Projects.get_by_id(int(kwargs['pid']))
	
		#check if its by user id
		if not results:
			key = ndb.Key(db_models.User, int(kwargs['pid']))
			getKey=key.get()
			if getKey:       
				#get projects
				list = db_models.Projects.query(db_models.Projects.user == key).fetch(keys_only=True)
				title = db_models.Projects.query(db_models.Projects.user == key).fetch()
				out ={'project_id': [x.id() for x in list], 'title': [x.title for x in title]}
				self.response.set_status(200)
				#self.response.write(self.response.status)	
				self.response.write(json.dumps(out))
				return
			else:
				self.response.set_status(404, "User or Project not found.")
				self.response.write(self.response.status)	
				return
							
		else:	
			out = results.to_dict()
			self.response.set_status(200)
			#self.response.write(self.response.status)	
			self.response.write(json.dumps(out))
		return
	
	#update project by pid
	def put (self, **kwargs):
		token = self.request.get('token')
		if not token:
			self.response.set_status(404, "Token not found.")
			self.response.write(self.response.status)
			return
			
		tk = int(token)	
		kq = [x.token for x in db_models.User.query(db_models.User.token==tk).fetch()]
		if not kq:
			self.response.set_status(404, "Token not valid.")
			self.response.write(self.response.status)
			return	
			
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
		
		#check for id
		if 'pid' not in kwargs:
			self.response.set_status(400, "Invalid request. PID required.")
			self.response.write(self.response.status)
			return 
			
		results = db_models.Projects.get_by_id(int(kwargs['pid']))	
		
		#check that id was valid
		if not results:
			self.response.set_status(404, "Project not found.")
			self.response.write(self.response.status)	
			return
			
		title = self.request.get('title')
		self.response.write(title)
		description = self.request.get('descr')
		self.response.write(description)
		whom = self.request.get('whom')
		self.response.write(whom)
		user = self.request.get('user')
		comm = self.request.get('comm')
		self.response.write(comm)
		
		#cannot change user throw error if there is a change
		if user:
			self.response.set_status(403, "User cannot be changed.")
			self.response.write(self.response.status)	
			return
		
		if title:
			results.title = title 
		if description:
			results.description = description
		if whom: 
			results.whom = whom
		if comm: 
			results.commisioned = comm
			
		results.put()
		out = results.to_dict()
		self.response.set_status(200, "Project updated.")
		#self.response.write(self.response.status)
		self.response.write(json.dumps(out))	
		return
	
	#delete project with pid
	def delete(self, **kwargs):
		token = self.request.get('token')
		if not token:
			self.response.set_status(404, "Token not found.")
			self.response.write(self.response.status)
			return
			
		tk = int(token)	
		kq = [x.token for x in db_models.User.query(db_models.User.token==tk).fetch()]
		if not kq:
			self.response.set_status(404, "Token not valid.")
			self.response.write(self.response.status)
			return	
			
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
		
		#check for id
		if 'pid' not in kwargs:
			self.response.set_status(400, "Invalid request. PID required.")
			self.response.write(self.response.status)
			return 
		
		results = db_models.Projects.get_by_id(int(kwargs['pid']))	
		
		#check that id was valid
		if not results:
			self.response.set_status(404, "Project not found.")
			self.response.write(self.response.status)	
			return
		
		results.key.delete()
		
		#check if record deleted
		check =  db_models.Projects.get_by_id(int(kwargs['pid']))

		if check: 
			self.response.set_status(500, "Server error. Project not deleted.")
			self.response.write(self.response.status)
		
		else:
			self.response.set_status(200, "Project has been deleted.")
			#self.response.write(self.response.status)
		return