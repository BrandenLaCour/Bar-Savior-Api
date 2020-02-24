from peewee import *

from flask_login import UserMixin
from playhouse.db_url import connect

DATABASE = SqliteDatabase('bar-savior.sqlite')


class Company(Model):
    name = CharField()
    address= CharField()

    class Meta():
        database = DATABASE


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    admin = BooleanField(default=False)
    master = BooleanField(default=False)
    position = CharField()
    companyId = ForeignKeyField(Company, backref='users')

    class Meta():
        database = DATABASE


def intialize():
    DATABASE.connect()
    
    DATABASE.create_tables([User, Company], safe=True)
    print('connected to database if didnt already exist')

    DATABASE.close()