from flask import Flask, render_template, Response
from services.camera import gen_frames
from services.face_services import load_encodings_cache

from api.register import register_bp
from api.identify import identify_bp
from api.students import students_bp
from api.auth import auth_bp
from api.session import session_bp

app = Flask(__name__)
app.secret_key = "hackathon-secret"

# Register API blueprints
app.register_blueprint(register_bp, url_prefix="/api")
app.register_blueprint(identify_bp, url_prefix="/api")
app.register_blueprint(students_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")  
app.register_blueprint(session_bp, url_prefix="/api") 


@app.route("/video_feed")
def video_feed():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    load_encodings_cache()
    app.run(host="0.0.0.0", port=5000, threaded=True)

