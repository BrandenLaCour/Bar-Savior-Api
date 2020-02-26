from peewee import *
import datetime

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
    company = ForeignKeyField(Company, backref='users')

    class Meta():
        database = DATABASE

class Room(Model):
    name= CharField()
    date= DateTimeField(default=datetime.datetime.now)
    company = ForeignKeyField(Company, backref='rooms')

    class Meta():
        database= DATABASE

class Task(Model):
    name= CharField()
    day= CharField(null=True)
    active= BooleanField(default='true')
    date= SmallIntegerField(default=0)
    frequency= CharField(default='daily')
    ##maybe above custom field in the future (daily, weekly, monthly)
    shift = CharField(default='both')
    ##maybe above custom field in the future (both, day, night)
    room= ForeignKeyField(Room, backref='tasks')


    class Meta():
        database = DATABASE


class Log(Model):
        task=ForeignKeyField(Task, backref='logs')
        notes = CharField(null=True)
        status = CharField(default='completed')
        #status = (completed, needs attention, urgent)
        user = ForeignKeyField(User, backref='logs')
        resolvedId = SmallIntegerField(null=True)
        #above should be users Id that resolved it
        imageUrl = CharField(null=True)
        dateAdded = DateTimeField(default=datetime.datetime.now)

        class Meta():
            database = DATABASE
        


def intialize():
    DATABASE.connect()
    
    DATABASE.create_tables([User, Company, Room, Task, Log], safe=True)
    print('connected to database if didnt already exist')

    DATABASE.close()