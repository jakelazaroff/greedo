import tornado.ioloop
import tornado.web
import tornado.options

import app
import settings

HANDLERS = [
	(r'/?', app.app_index),

	(r'/data/(\w+)/?', app.app_data),
	(r'/graph/(\w+)/?', app.app_graph),

	(r'/(greedo.js)', app.app_file),
	(r'/(greedo.css)', app.app_file),
]

if __name__ == '__main__':
	application = tornado.web.Application(HANDLERS, **{
		'debug' : settings.debug,
	})

	application.listen(int(settings.port), **{
		'xheaders' : settings.xheaders,
	})

	tornado.options.options.log_file_prefix = settings.log_prefix
	tornado.options.parse_command_line()
	tornado.ioloop.IOLoop.instance().start()
