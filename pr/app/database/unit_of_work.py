from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    def __init__(self, repository):
        self.repository = repository
        self.session = repository.session

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    def __next__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()


class AlchemyUnitOfWork(UnitOfWork):
    def begin(self):
        self.session.begin()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
