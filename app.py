import tornado.web
import MySQLdb
import MySQLdb.cursors
import json
import datetime
import decimal
import re

import settings

def app_read_template(template):
	f = open('%s/%s.sql' % (settings.sql_dir, template), 'r')
	q = f.read()
	f.close()

	return q

def app_fill_template(q, args):
	phs = re.findall(r'{{\w+}}', q)

	vals = []

	for ph in phs:
		q = q.replace(ph, '%s')
		ph = ph.translate(None, '{}')
		vals.append(args[ph])

	return q, vals

def app_json_serial(obj):
	if isinstance(obj, (datetime.datetime, datetime.date)):
		return obj.isoformat()

	elif isinstance(obj, decimal.Decimal):
		return float(obj)

	raise TypeError ("Type %s not serializable" % type(obj))

def app_query(q, vals):

	conn = MySQLdb.connect(host=settings.mysql_host, user=settings.mysql_user,
		passwd=settings.mysql_password, db=settings.mysql_db, cursorclass=MySQLdb.cursors.DictCursor)

	cur = conn.cursor()
	cur.execute(q, vals)

	j = json.dumps(cur.fetchall(), default=app_json_serial)

	cur.close()
	conn.close()

	return j

def app_execute_template(template, args):
	q = app_read_template(template)
	q, vals = app_fill_template(q, args)
	j = app_query(q, vals)

	return j

class app_data(tornado.web.RequestHandler):
	def get(self, template):
		j = app_execute_template(template, self.request.arguments)

		self.set_header('Content-Type', 'application/json')
		self.write(j)

class app_graph(tornado.web.RequestHandler):
	def get(self, template):
		j = app_execute_template(template, self.request.arguments)

		self.render('%s/%s.html' % (settings.template_dir, template), data=j)

class app_file(tornado.web.RequestHandler):
	def get(self, file_name):
		f = open(file_name, 'r')
		body = f.read()
		f.close()

		self.set_header('Content-Type', 'application/javascript')
		self.write(body)
