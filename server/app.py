from flask import Flask, request, make_response, jsonify
# request docs -> https://tedboy.github.io/flask/generated/generated/flask.Request.html
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['POST', 'GET'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        # dict_messages = []
        # for message in messages:
        #     dict_messages.append(message.to_dict())
        dict_messages = [message.to_dict() for message in messages]

        response = make_response(dict_messages, 200)
        return response
    elif request.method == 'POST':
        data = request.get_json()

        message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(message)
        db.session.commit()

        response = make_response(message.to_dict(), 201)
        return response


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        response = make_response(message.to_dict(), 200)
        return response
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_dict = {
            "message": "Message delete"
        }

        response = make_response(response_dict, 200)
        return response
    elif request.method == 'GET':
        response = make_response(message.to_dict())
        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
