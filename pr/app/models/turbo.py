from flask_socketio import SocketIO, join_room



class Turbo():
    def __init__(self, app=None, debug=True):
        self.socket = SocketIO(engineio_logger=True, logger=True, cors_allowed_origins='*')
        self.user_id_callback = self.default_user_id
        self.clients = []
        self.debug = debug
        if app:
            self.init_app(app)

    
    def init_app(self, app):
        with app.app_context():
            @self.socket.on("connect")
            def connect():
                room = self.user_id_callback()
                join_room(room)
                # send("Yes", to=room)
                if self.debug:
                    self.socket.emit("mess", f"You are in room {room}", room=room)
            self.socket.init_app(app)
            app.context_processor(self.context_processor)


    def context_processor(self):
        return {'turbo': self.turbo}

    
    def turbo(self): 
        return """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>
        <script type="text/javascript" charset="utf-8">
            function replaceTargetWith( targetID, html ){
                var i, tmp, elm, last, target = document.getElementById(targetID);
                tmp = document.createElement('div');
                tmp.innerHTML = html;
                i = tmp.childNodes.length;
                last = target;
                while(i--){
                    target.parentNode.insertBefore((elm = tmp.childNodes[i]), last);
                    last = elm;
                }
                target.parentNode.removeChild(target);
            }

            var socket = io();

            socket.on('connect', function() {
                console.log("Yeeees");
            });

            socket.on('replace', function(data) {
                console.log(data)
                replaceTargetWith(data.target, data.content);
            });

            socket.on('mess', function (data) {console.log(data)})
        </script>
        """


    def default_user_id(self):
        return 0


    def user_id(self, f):
        self.user_id_callback = f
        return f

    def replace(self, content: str, target: str, to):
        self.socket.emit("replace", {"target": target, "content": content}, to=to)

turbo = Turbo()