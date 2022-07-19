from waitress import serve

from SuppleTime.pr.app import create_app


socket, app = create_app()

if __name__ == "__main__":
    socket.run(app)
    # serve(app, host='0.0.0.0') #123123
#tolya loh hehehe
