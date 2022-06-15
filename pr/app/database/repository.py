from abc import ABC, abstractmethod


class Repository(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def save(self, obj):
        pass
    
    @abstractmethod
    def update(self, obj):
        pass
    