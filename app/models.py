from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    pass

class Application(Base):
    pass

class Company(Base):
    pass

class Offer(Base):
    pass

class Note(Base):
    pass

class Document(Base):
    pass

class Job(Base):
    pass