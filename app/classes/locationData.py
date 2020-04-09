from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField, EmbeddedDocumentField, DateTimeField, DateField, EmailField, URLField, ListField, CASCADE, ImageField
import datetime as d
from app.classes.data import User


class LocationData(Document):
    author = ReferenceField(User,reverse_delete_rule=CASCADE)
    name = StringField()
    desc = StringField()
    createdate = DateTimeField(default=d.datetime.utcnow)
    image = ImageField()
    longitude = IntField()
    latitude = IntField()