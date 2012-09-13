#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import cgi
import re,string

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.template import Context,Template,loader
from django import forms

from google.appengine.ext import db

def getvname(string):
	p = re.compile('VNAME.*=(.*)')
	m = p.search(string)
	return m.group(1)

def getsigid(string):
	p = re.compile('SIGID.*=(.*)')
	m = p.search(string)
	return m.group(1)



class cprldb(db.Model):
	user = db.StringProperty()
	cprlstring = db.TextProperty()
	submitdate = db.DateTimeProperty(auto_now=True)
	vname= db.StringProperty()
	sigid =  db.IntegerProperty()
	category = db.StringProperty()


class myForm(forms.Form):
	user=forms.CharField()
	cprlstring=forms.CharField(widget=forms.Textarea(attrs={'cols':80,'rows':20}))


class MainHandler(webapp2.RequestHandler):
	def get(self):
		form=myForm()
		cprls = cprldb.all()
		cprls.order('-submitdate')
		t=loader.get_template('index.html')
		c=Context({"my_name":"CPRL List","cprls":cprls,'form':form})
		self.response.out.write(t.render(c))

class OutputHandler(webapp2.RequestHandler):
	def get(self):
		cprls = cprldb.all()
		t=loader.get_template('output.html')
		c=Context({"cprls":cprls,"re":"\r\n"})
		self.response.headers.add_header('content-disposition', 'attachment', filename='comm.sig')
		self.response.out.write(t.render(c))

class AddHandler(webapp2.RequestHandler):
	def post(self):
		user = self.request.get("user")
		cprlstring=self.request.get("cprlstring")
		self.response.out.write(cprlstring)
		cprl = cprldb(category="default")
		cprl.cprlstring = cprlstring
		cprl.user = user
		cprl.vname = string.strip(getvname(cprlstring))
		cprl.sigid = int(getsigid(cprlstring))
		cprl.put()
		self.redirect('/')
		#t=loader.get_template('add.html')
		#c=Context({"my_name":"CPRL List"})
		#self.response.out.write(t.render(c))	
	
class EditHandler(webapp2.RequestHandler):
	def get(self,id):
		cprl=cprldb.get_by_id(int(id))
		data={
		'cprlstring':cprl.cprlstring,
		'user':cprl.user,
		}
		form=myForm(data)
		t=loader.get_template('edit.html')
		c=Context({"my_name":"Fileset Board",'form':form,'id':int(id)})
		self.response.out.write(t.render(c))
	def post(self,id):
		cprlstring = self.request.get('cprlstring')
		user=self.request.get('user')
		cprl = cprldb.get_by_id(int(id))
		cprl.cprlstring = cprlstring
		cprl.user = user 
		cprl.vname = string.strip(getvname(cprlstring))
		cprl.sigid = int(getsigid(cprlstring))
		cprl.put()
		self.redirect('/')


		


app = webapp2.WSGIApplication([
	(r'/', MainHandler),
	(r'/add',AddHandler),
	(r'/output',OutputHandler),
	(r'/edit/(\d+)', EditHandler),
	], debug=True)
