from SuppleTime.pr.app.database.repository import Repository
from SuppleTime.pr.app.models.user import User
from SuppleTime.pr.app.database.exceptions import NotFoundException
import sqlalchemy


class UserRepository(Repository):
    def get(self, id: int):
        try:
            return self.session.query(User).filter_by(id=id).one()
        except sqlalchemy.exc.NoResultFound as exc:
            raise NotFoundException(exc)


    def list(self):
        return self.session.query(User).all()


    def save(self, obj):
        self.session.add(obj)


    def update(self, obj):
        pass
