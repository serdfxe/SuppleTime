#models.Workspace
import sqlalchemy

from SuppleTime.pr.app.database.repository import Repository
from SuppleTime.pr.app.models.Workspace import *
from SuppleTime.pr.app.database.exceptions import NotFoundException


class WorkspacesRepository(Repository):
    def get(self,**kwargs):
        try:
            return self.session.query(Workspaces).filter_by(**kwargs).first()
        except sqlalchemy.exc.NoResultFound as exc:
            raise NotFoundException(exc)


    def list(self):
        return self.session.query(Workspaces).all()


    def save(self, obj):
        self.session.add(obj)


    def update(self, obj):
        pass


class TrackedTasksRepository(Repository):
    def get(self,**kwargs):
        try:
            return self.session.query(Tracked_tasks).filter_by(**kwargs).first()
        except sqlalchemy.exc.NoResultFound as exc:
            raise NotFoundException(exc)


    def list(self):
        return self.session.query(Tracked_tasks).all()


    def save(self, obj):
        self.session.add(obj)


    def update(self, obj):
        pass


class TrackersRepository(Repository):
    def get(self,**kwargs):
        try:
            return self.session.query(Trackers).filter_by(**kwargs).first()
        except sqlalchemy.exc.NoResultFound as exc:
            raise NotFoundException(exc)


    def list(self):
        return self.session.query(Trackers).all()


    def save(self, obj):
        self.session.add(obj)


    def update(self, obj):
        pass
