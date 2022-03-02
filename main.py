from app import create_app

if __name__ == '__main__':
    application = create_app()

    from werkzeug.serving import run_simple

    run_simple('0.0.0.0', 8088, application, use_reloader=True, use_debugger=True)
