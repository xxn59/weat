from app import db, models

u = models.User(nickname='john', email='john@email.com')
db.session.add(u)
u = models.User(nickname='allen', email='allen@email.com')
db.session.add(u)
u = models.User(nickname='michael', email='michael@email.com')
db.session.add(u)
db.session.commit()
users = models.User.query.all()
print 'users in the database:'
print users
raw_input()
