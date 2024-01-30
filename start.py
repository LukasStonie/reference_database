import app
application = app.create_app()

if __name__ == '__main__':
    application.run(port=5533, debug=True)
