from app import create_app
from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    application = create_app()

    http_server = WSGIServer(('', 5000), application)
    http_server.serve_forever()
