# coding=utf-8
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

Base = declarative_base()
engine = create_engine('postgresql+psycopg2:///kansalaisrajoite', echo=False)
plugin = sqlalchemy.Plugin(engine, None, keyword='db')


vote_table = Table('vote', Base.metadata,
	Column('restriction_id', Integer, ForeignKey('restriction.id')),
	Column('user_id', Integer, ForeignKey('user.id'))
)

class Restriction(Base):
	__tablename__ = 'restriction'
	
	id = Column(Integer, primary_key=True)
	created = Column(DateTime, server_default=func.current_timestamp())
	modified = Column(DateTime, server_default=func.current_timestamp())
	title = Column(String)
	contents = Column(String)
	arguments = Column(String)
	approved = Column(Boolean, server_default='FALSE')
	
	approver_id = Column(Integer, ForeignKey('user.id'))
	approver = relationship('User', foreign_keys=approver_id)
	
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship('User', foreign_keys=user_id)
	
	voters = relationship('User', secondary=vote_table, backref='restrictions')
	
	def __repr__(self):
		return '<Restriction: %s>' % self.otsikko
	
	def toDict(self, full=False):
		ret = {}
		ret['id'] = self.id
		ret['created'] = self.created
		ret['votes'] = len(self.voters)
		ret['title'] = self.title
		ret['contents'] = self.contents
		ret['arguments'] = self.arguments
		ret['user'] = self.user.toDict()
		ret['approved'] = self.approved
		if full:
			ret['approver'] = self.approver.toDict()
			ret['modified'] = self.modified
		return ret

class User(Base):
	__tablename__ = 'user'
	
	id = Column(Integer, primary_key=True)
	email = Column(String)
	name = Column(String)
	password = Column(String)
	city = Column(String)
	admin = Column(Boolean, server_default='FALSE')
	registered = Column(DateTime, server_default=func.current_timestamp())
	
	def __repr__(self):
		return '<User: %s>' % self.email
	
	def toDict(self, full=False):
		ret = {}
		ret['name'] = self.name
		ret['city'] = self.city
		if full:
			ret['id'] = self.id
			ret['email'] = self.email
			ret['registered'] = self.registered
			ret['admin'] = self.admin
		return ret