from waitress import serve

from SuppleTime.pr.app import create_app


app = create_app()

if __name__ == "__main__":
    serve(app, host='0.0.0.0') #123123
#tolya loh hehehe
