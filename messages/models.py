from datetime import datetime

from app import db, app


# ------------------------------------------------------------------------------------------------------
def save(obj):
    db.session.add(obj)
    db.session.commit()


# ------------------------------------------------------------------------------------------------------
def delete(obj):
    db.session.delete(obj)
    db.session.commit()


# ------------------------------------------------------------------------------------------------------
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, index=True)
    sender = db.Column(db.String, nullable=False)
    receiver = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    read = db.Column(db.Boolean, default=False)

    @classmethod
    def create_message(cls, sender, receiver, subject, message, creation_date=None):
        sender = sender.lower()
        receiver = receiver.lower()
        message = cls(sender=sender, receiver=receiver, subject=subject,
                      message=message, creation_date=creation_date)
        save(message)
        return message

    @classmethod
    def read_one_message(cls, receiver):
        # get one unread message
        message = cls.query.filter_by(receiver=receiver, read=False).first()

        if not message:
            # return empty json if none
            return {}

        # mark as read and save
        message.read = True
        save(message)
        return message.to_json()

    @classmethod
    def filter_message(cls, *args, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def to_json(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "creation_date": f"{self.creation_date}",
            "read": self.read,
            "subject": self.subject,
            "message": self.message,
        }

    def delete(self):
        delete(self)

    def __repr__(self):
        return self.to_json()


# ------------------------------------------------------------------------------------------------------
with app.app_context():
    db.create_all()
