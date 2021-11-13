from misc.addition import get_full_path
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine


class Database:
    __Base = declarative_base()

    # tables
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
        tests = relationship("Tests", cascade="all, delete, delete-orphan")

    def __init__(self):
        self.engine = create_engine(f'sqlite:///{get_full_path("database.db")}', echo=False)
        self.session = sessionmaker(bind=self.engine)()

    def create(self):
        self.__Base.metadata.create_all(self.engine)

    def get_task_by_name(self, name: str):
        return self.session.query(self.Tasks).filter(self.Tasks.name == name.lower().capitalize()).one()

    def delete_task(self, name: str):
        self.session.delete(self.get_task_by_name(name))
        self.session.commit()

    def delete_all_tasks(self):
        self.session.query(self.Tasks).delete()
        self.session.query(self.Tests).delete()
        self.session.commit()

    def create_task(self, name: str):
        task = self.Tasks(name=name.lower().capitalize())
        self.session.add(task)
        self.session.commit()

    def add_test_for_task(self, task_name, input: str, output: str):
        task = self.get_task_by_name(task_name)
        test = self.Tests(task_id=task.id, input=input, output=output)
        self.session.add(test)
        self.session.commit()

    def update_session(self):
        self.session.commit()

    # # get
    # @property
    # def get_authors(self) -> list[Users]:
    #     return list(self.session.query(self.Author).order_by(self.Author.id))
    #
    # def get_authors_by_id(self, key: int):
    #     try:
    #         return self.session.query(self.Author).filter(self.Author.id == key).one()
    #     except exc.NoResultFound:
    #         return None
    #
    # def get_users_by_id(self, key: int):
    #     try:
    #         return self.session.query(self.Users).filter(self.Users.vk_id == key).one()
    #     except exc.NoResultFound:
    #         return False
    #
    # def get_user_selected_author(self, user: Union[int, Users]):
    #     if isinstance(user, int):
    #         user = self.get_users_by_id(user)
    #     return user.selected_author.author_id
    #
    # # create
    # def create_user_if_not_exists(self, key) -> Users:
    #     user = self.get_users_by_id(key)
    #     if not user:
    #         user = self.Users(vk_id=key, state_id=0)
    #         self.session.add(user)
    #         self.session.commit()
    #     return user
    #
    # # set
    # def set_user_state(self, user: Union[int, Users], state_id) -> None:
    #     if isinstance(user, int):
    #         user = self.get_users_by_id(user)
    #     user.state_id = state_id
    #     self.session.commit()
    #
    # def set_user_selected_author(self, user: Union[int, Users], selected: int) -> None:
    #     if isinstance(user, int):
    #         user = self.get_users_by_id(user)
    #     if user.selected_author:
    #         user.selected_author.author_id = selected
    #         self.session.add(user)
    #     else:
    #         selected = self.SelectedAuthor(user_id=user.id, author_id=selected)
    #         self.session.add(selected)
    #     self.session.commit()
