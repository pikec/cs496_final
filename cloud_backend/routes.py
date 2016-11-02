import webapp2

config = {'default-group':'base-data'}

app = webapp2.WSGIApplication([], debug=True, config=config)

app.router.add(webapp2.Route(r'/', 'main.URIHandler'))
app.router.add(webapp2.Route(r'/users/login', 'users.LogHandler'))
app.router.add(webapp2.Route(r'/users', 'users.UserHandler'))
app.router.add(webapp2.Route(r'/users/<id:[0-9]+>', 'users.OtherUserHandler'))
app.router.add(webapp2.Route(r'/projects', 'projects.ProjectHandler'))
app.router.add(webapp2.Route(r'/projects/<pid:[0-9]+>', 'projects.OtherProjectHandler'))
app.router.add(webapp2.Route(r'/projects/<id:[0-9]+>', 'projects.ProjectHandler'))

