from pr.app import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    serve(app, host='0.0.0.0') #123123
#tolya loh hehehe
