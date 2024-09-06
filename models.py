from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Leader(Base):
    __tablename__ = 'leaders'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    bio = Column(String(500))
    projects = relationship('Project', back_populates='leader', lazy='dynamic')
    collaborators = relationship('Collaborator', back_populates='leader', lazy='dynamic')
    contents = relationship('Content', back_populates='leader', lazy='dynamic')

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    leader_id = Column(Integer, ForeignKey('leaders.id'))
    leader = relationship('Leader', back_populates='projects')

class Collaborator(Base):
    __tablename__ = 'collaborators'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100))
    leader_id = Column(Integer, ForeignKey('leaders.id'))
    leader = relationship('Leader', back_populates='collaborators')

class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # 'free' or 'paid'
    url = Column(String(200))
    leader_id = Column(Integer, ForeignKey('leaders.id'))
    leader = relationship('Leader', back_populates='contents')
