import os
from peewee import *
import datetime

from flask_login import UserMixin
from playhouse.db_url import connect

DATABASE = SqliteDatabase('bar-savior.sqlite')

if 'ON_HEROKU' in os.environ: 
                             
  DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
  DATABASE = SqliteDatabase('bar-savior.sqlite')

class Company(Model):
    name = CharField()
    address= CharField()

    class Meta():
        database = DATABASE


class Member(UserMixin, Model):
    username = CharField()
    password = CharField()
    email = CharField(unique=True)
    admin = BooleanField(default=False)
    master = BooleanField(default=False)
    position = CharField()
    active = BooleanField(default=True)
    company = ForeignKeyField(Company, backref='members')

    class Meta():
        database = DATABASE

class Room(Model):
    name= CharField()
    date= DateTimeField(default=datetime.datetime.now)
    company = ForeignKeyField(Company, backref='rooms')
    active= BooleanField(default=True)
    class Meta():
        database= DATABASE

class Task(Model):
    name= CharField()
    day= CharField(null=True)
    active= BooleanField(default=True)
    date= SmallIntegerField(default=0)
    frequency= CharField(default='daily')
    imgReq = BooleanField(default='false')
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
        #status = (okay, attention, urgent)
        user = ForeignKeyField(Member, backref='logs')
        resolvedId = SmallIntegerField(null=True)
        #above should be users Id that resolved it
        imageId = CharField(null=True)
        dateAdded = DateTimeField(default=datetime.datetime.now)
        urgent = BooleanField(default=False)
        class Meta():
            database = DATABASE
        


def initialize():
    DATABASE.connect()
    
    DATABASE.create_tables([Member, Company, Room, Task, Log], safe=True)
    print('connected to database if didnt already exist')

    DATABASE.close()