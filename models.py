from peewee import *
import os
from playhouse.db_url import connect

# Conectarse usando la DATABASE_URL
db = connect(os.environ.get('DATABASE_URL', 'sqlite:///default.db'))

class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    title = CharField()
    done = BooleanField(default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }
