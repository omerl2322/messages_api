from flask_restful import reqparse

post_message_parser = reqparse.RequestParser(bundle_errors=True,)
post_message_arguments = ["sender", "receiver", "subject", "message", ]

for arg in post_message_arguments:
    post_message_parser.add_argument(
        arg, dest=arg,
        location='json', required=True,
        trim=True, help=f"{arg} is required",
    )

# ------------------------------------------------------------------------------------------------------
get_message_parser = reqparse.RequestParser(bundle_errors=True,)
get_message_parser.add_argument(
    "receiver", dest="receiver",
    location='args', required=True,
    trim=True, help="receiver should be provided",
)

get_message_parser.add_argument(
    "read", dest="read",
    location='args', required=False, default=False
)

# ------------------------------------------------------------------------------------------------------

delete_message_parser = reqparse.RequestParser(bundle_errors=True,)
delete_message_parser.add_argument(
    "id", dest="id",
    location='args', required=True,
    type=int,
    trim=True, help="id of message to delete is required",
)

