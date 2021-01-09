from models import User, Place, RedNode

'''
# TEST
places = Place.query.all()
rednodes = RedNode.query.all()
users = User.query.all()
for u in users:
    db.session.delete(u)
for p in places:
    db.session.delete(p)
for r in rednodes:
    db.session.delete(r)
u = User(cf="DAUIDAIWUDH", username="Test", positive=False)
db.session.add(u)
u = User.query.get(1)
p = Place(id=u.id, start=4000000, lat=5555555, long=3333333, finish=6000000, placeId='"Roma"')
p2 = Place(id=u.id, start=4000001, lat=5555555, long=3333333, finish=6000000, placeId='"Roma"')
db.session.add(p)
db.session.add(p2)
r = RedNode(prob=0.6, start=4000001, lat=5555555, long=3333333, finish=6000001, placeId='"Roma"')
db.session.add(r)
db.session.commit()

g = Place.query.get((1, 4000000))
print(g)
'''