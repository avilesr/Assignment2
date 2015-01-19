import webapp2
import os
import jinja2
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class FillForm(ndb.Model):
	name = ndb.StringProperty()
	email = ndb.StringProperty()
	month = ndb.StringProperty()
	day = ndb.StringProperty()
	gender = ndb.StringProperty()
	cheetos = ndb.StringProperty()
	doritos = ndb.StringProperty()
	fritos = ndb.StringProperty()
	sunchips = ndb.StringProperty()

class ViewEntrys(webapp2.RequestHandler):

	def get(self):
		entrys_query = FillForm.query().order(FillForm.name)
		entrys = entrys_query.fetch(100)

		template_values = {
			'entrys': entrys,
		}

		template = JINJA_ENVIRONMENT.get_template('view.html')
		self.response.write(template.render(template_values))

class AddEntrys(webapp2.RequestHandler):
	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.write(template.render())

class EditEntrys(webapp2.RequestHandler):

	def post(self):
		#check_key = ndb.Key(self.request.get('key'))
		#check = entry_key.get()
		entry = FillForm.get_by_id(int(self.request.get('id')))
		
		template_values = {
			'entry': entry,
		}
		
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))

class Entry(webapp2.RequestHandler):

	def post(self):
		
		action = self.request.get('action')
		id = int(self.request.get('id'))

		if action == "add":
			entry = FillForm()
			entry.name = self.request.get('name')
			entry.email = self.request.get('email')
			entry.month = self.request.get('month')
			entry.day = self.request.get('day')
			entry.gender = self.request.get('gender')
			entry.cheetos = self.request.get('cheetos')
			entry.doritos = self.request.get('doritos')
			entry.fritos = self.request.get('fritos')
			entry.sunchips = self.request.get('sunchips')
			entry.put()
			self.redirect('/add')
		elif action == "edit":
			#entry = entry_key.get()
			food_boxes = []
			entry = FillForm.get_by_id(id)
			entry.name = self.request.get('name')
			entry.email = self.request.get('email')
			entry.month = self.request.get('month')
			entry.day = self.request.get('day')
			entry.gender = self.request.get('gender','checked')
			entry.cheetos = self.request.get('cheetos')
			entry.doritos = self.request.get('doritos')
			entry.fritos = self.request.get('fritos')
			entry.sunchips = self.request.get('sunchips')
			#entry.checked = self.request.get('checked')			
			entry.put()
			self.redirect('/view')
		elif action == "delete":
			entry = FillForm.get_by_id(id)
			entry.key.delete()
			self.redirect('/view')

application = webapp2.WSGIApplication([
	('/', ViewEntrys),
	('/view', ViewEntrys),
	('/add', AddEntrys),
	('/edit', EditEntrys),
	('/enter', Entry),
], debug=True)