import random
import shutil

from pydantic import UUID4
from sqlalchemy import select

from mealie.assets import users as users_assets
from mealie.schema.user.user import PrivateUser

from ..db.models.users import User
from .repository_generic import RepositoryGeneric


class RepositoryUsers(RepositoryGeneric[PrivateUser, User]):
    def update_password(self, id, password: str):
        entry = self._query_one(match_value=id)
        entry.update_password(password)
        self.session.commit()

        return self.schema.from_orm(entry)

    def create(self, user: PrivateUser | dict):  # type: ignore
        new_user = super().create(user)

        # Select Random Image
        all_images = [
            users_assets.img_random_1,
            users_assets.img_random_2,
            users_assets.img_random_3,
        ]
        random_image = random.choice(all_images)
        shutil.copy(random_image, new_user.directory() / "profile.webp")

        return new_user

    def delete(self, value: str | UUID4, match_key: str | None = None) -> User:
        entry = super().delete(value, match_key)
        # Delete the user's directory
        shutil.rmtree(PrivateUser.get_directory(value))
        return entry

    def get_by_username(self, username: str) -> PrivateUser | None:
        stmt = select(User).filter(User.username == username)
        dbuser = self.session.execute(stmt).scalars().one_or_none()
        return None if dbuser is None else self.schema.from_orm(dbuser)

    def get_locked_users(self) -> list[PrivateUser]:
        stmt = select(User).filter(User.locked_at != None)  # noqa E711
        results = self.session.execute(stmt).scalars().all()
        return [self.schema.from_orm(x) for x in results]
