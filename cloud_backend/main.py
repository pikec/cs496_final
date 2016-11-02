#!/usr/bin/env python
#
#Candis Pike
#API assignment CS496S'16
#code ideas adapted from lecture 
#
import webapp2

class URIHandler(webapp2.RequestHandler):

  # return a list of urls available at this api
  def get(self):

    API_URLS = {
		'POST /users',
		'GET /users',
		'GET /users/{user id}',
		'PUT /users/{user id}',
		'DELETE /users/{user id}',
		'POST /projects',
		'GET /projects',
		'GET /projects/{project id}',
		'GET /projects/{user id}',
		'PUT /projects/{project id}',
		'DELETE /projects/{project id}'
	}
    
    for url in sorted(API_URLS):
      self.response.write(url + '<br/>')