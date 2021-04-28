from flask_restful import Resource

from .models import Message as MessageModel
from .requests_parser import post_message_parser, get_message_parser, delete_message_parser


# ------------------------------------------------------------------------------------------------------

class Message(Resource):
    def post(self):
        args = post_message_parser.parse_args()
        try:
            message = MessageModel.create_message(**args)
            message = message.to_json()
            del message["read"]
            message["status"] = "sent"
            return message, 201
        except Exception as e:
            return {"status": "failed"}, 400

    def get(self):
        args = get_message_parser.parse_args()
        # convert read to boolean
        if isinstance(args["read"], str):
            read = args["read"].lower()
            args["read"] = True if read == "true" else False
        return [message.to_json() for message in MessageModel.filter_message(**args)], 200


# ------------------------------------------------------------------------------------------------------
class ReadMessage(Resource):
    def get(self, receiver):
        return MessageModel.read_one_message(receiver=receiver), 200


# ------------------------------------------------------------------------------------------------------
class DeleteMessage(Resource):

    def delete(self, party):
        args = delete_message_parser.parse_args()
        message = MessageModel.get_by_id(args["id"])
        if message and (party in [message.sender, message.receiver, ]):
            message.delete()
            message = message.to_json()
            return message, 200
        return {"status": "cannot delete message"}, 403
