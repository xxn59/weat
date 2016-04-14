from app import db, models

users = models.User.query.all()
print 'users in the database:'
print users
raw_input()
