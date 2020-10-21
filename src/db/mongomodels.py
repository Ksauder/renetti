from mongoengine import *
from discord import User as DUser

class User(Document):
    meta = {
        'collection': 'users'
    }
    discord_id = IntField(max_length=255, required=True, primary_key=True)
    bot = BooleanField(required=True)
    name = StringField(max_length=255, required=True)
    nicknames = ListField(field=StringField, required=True)
    discriminator = StringField(max_length=255, required=True)
    date_joined = DateTimeField(required=True)
    date_left = DateTimeField()

    def from_user(self, d_user_obj):
        assert isinstance(d_user_obj, DUser)
        ret = None
        self.discord_id = d_user_obj.id
        user = self.objects(discord_id__exact=self.discord_id).get()
        if user:
            ret = self.update_user(user, d_user_obj)
        else:
            self.nicknames.append(d_user_obj.display_name)
            self.name = str(d_user_obj.name)

        return ret

    def update_user(self, user, d_user_obj):
        assert user.id == d_user_obj.id
        if d_user_obj.display_name not in user.nicknames:
            user.nicknames.append(d_user_obj.display_name)
        if user.name != d_user_obj.name:
            user.name = d_user_obj.name




class FeatureRequest(Document):
    meta = {
        'collection': 'feature_reqs'
    }
    author = ReferenceField(document_type=User, required=True)
    status = StringField(max_length=255, required=True) # probably a enum field
    body = StringField(max_length=1000, required=True)
    tags = ListField(field=StringField(max_length=30), max_length=20)


class Pin(Document):
    meta = {
        'collection': 'pins'
    }
    author = ReferenceField(document_type=User, required=True)
    body = StringField(max_length=1000, required=True)
