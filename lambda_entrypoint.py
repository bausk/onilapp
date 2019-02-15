from application import app


app.config['requests_pathname_prefix'] = '/dev' + app.config['requests_pathname_prefix']
application = app.server
