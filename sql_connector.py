from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


db = create_engine('mysql://3010user:sysc3010@localhost/BLAB_db');
base = declarative_base(bind=db)

class Item_Lookup(base):
	__tablename__ = 'food_item_lookup'

	tag_hashcode = Column(String(64), primary_key = True)
	item_name = Column(String(40))
	expiry = Column(Integer)

	def __repr(self):
		return "<item_lookup(tag_hashcode='%s', item_name='%s', expiry='%i')>" % (self.tag_hashcode, self.item_name, self.expiry)

class db_hand:

	def __init__(self):
		Session = sessionmaker(bind=db)
		self.session = Session()

	def get_item(self, hash):
		for row in self.session.query(Item_Lookup).filter(Item_Lookup.tag_hashcode==hash):
			return (row.item_name, row.expiry)

	def put_item(self, hash, name, expiration):
		item = Item_Lookup(tag_hashcode=hash, item_name=name, expiry=expiration)
		self.session.add(item)
		self.session.commit()
		return True


def main():
	hand = db_hand()
	print(hand.get_item('ajk19a20'))

main()
