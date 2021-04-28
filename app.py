import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from messages.views import Message, ReadMessage, DeleteMessage

# ------------------------------------------------------------------------------------------------------
load_dotenv()
# from messages import views
db = SQLAlchemy()


# ------------------------------------------------------------------------------------------------------
def create_app():
    def init_dependencies():
        db.init_app(app)

    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_dependencies()
    return app


app = create_app()
api = Api(app)
# ------------------------------------------------------------------------------------------------------

api.add_resource(Message, "/messages")
api.add_resource(ReadMessage, "/messages/<string:receiver>", )
api.add_resource(DeleteMessage, "/messages/<string:party>", )

if __name__ == "__main__":
    app.run(debug=True)
