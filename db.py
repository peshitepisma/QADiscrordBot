import functools
from misc.addition import get_full_path
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, exc


def session(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.update_session()
    return wrapper


def catch_except(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.NoResultFound:
            return None
    return wrapper


class Database:
    __Base = declarative_base()

    class Tests(__Base):
        __tablename__ = 'Tests'
        id = Column(Integer, primary_key=True)
        input = Column(String(250), default='')
        output = Column(String(250), nullable=False)
        task_id = Column(Integer, ForeignKey("Tasks.id"))

    class Tasks(__Base):
        __tablename__ = 'Tasks'
        id = Column(Integer, primary_key=True)
        name = Column(String(20), nullable=False, unique=True)
        description = Column(String(300), nullable=False)
        tests = relationship("Tests", cascade="all, delete, delete-orphan")

    def __init__(self):
        self.engine = create_engine(f'sqlite:///{get_full_path("database.db")}', echo=False)
        self.session = sessionmaker(bind=self.engine)()

    def create(self):
        self.__Base.metadata.create_all(self.engine)

    @catch_except
    def get_task_by_name(self, name: str):
        return self.session.query(self.Tasks).filter(self.Tasks.name == name.lower().capitalize()).one()

    def get_tasks(self):
        return self.session.query(self.Tasks).order_by(self.Tasks.id)

    @session
    def delete_task(self, task):
        self.session.delete(task)

    @session
    def delete_all_tasks(self):
        self.session.query(self.Tasks).delete()
        self.session.query(self.Tests).delete()

    @session
    def create_task(self, name: str, desciprtion: str):
        task = self.Tasks(name=name.lower().capitalize(), description=desciprtion)
        self.session.add(task)

    @session
    def add_test_for_task(self, task, input: str, output: str):
        test = self.Tests(task_id=task.id, input=input.strip(), output=output.strip())
        self.session.add(test)

    def update_session(self):
        self.session.commit()
