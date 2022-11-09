import random
import re
from datetime import date, datetime, timedelta
from typing import TypedDict

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import User, Category, Place


class SecretExtraData(TypedDict):
    food_suggestion: str
    time_suggestion: str
    company_suggestion: str
    music_suggestion: str
    extra_suggestion: str


class Creator:
    places_ids = dict()

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name="TestUser", coins: int = 0):
        ext_id = str(int(datetime.utcnow().timestamp() * 1000))
        user = (
            await self.session.execute(
                sa.insert(User)
                .values(
                    {
                        User.name: name,
                        User.external_id_type: "META",
                        User.external_id: ext_id,
                        User.coins: coins,
                    }
                )
                .returning(User.id)
            )
        ).fetchone()
        return user.id

    async def create_category(self, category_name, secret_mark: bool = False):
        category = (
            await self.session.execute(
                (
                    sa.insert(Category)
                    .values(
                        {
                            Category.name: category_name,
                            Category.mark: "secret" if secret_mark else None,
                        }
                    )
                    .returning(Category.id)
                )
            )
        ).fetchone()
        return category.id

    async def create_place(
        self,
        name: str = "TestPlace",
        description: str = None,
        category_id: int = 1,
        owner_id: int = 1,
        latitude: float = None,
        longitude: float = None,
        address: str = None,
        secret_extra_data: SecretExtraData = None,
    ):
        if not latitude:
            latitude = random.randint(-90, 90)
        if not longitude:
            longitude = random.randint(-90, 90)

        if secret_extra_data:
            secret_data_id = (
                await self.session.execute(sa.insert(SecretExtraData))
            ).scalar()
        place_id = (
            await self.session.execute(
                sa.insert(Place)
                .values(
                    {
                        Place.name: name,
                        Place.description: description,
                        Place.category_id: category_id,
                        Place.coordinate_longitude: latitude,
                        Place.coordinate_latitude: longitude,
                        Place.owner_id: owner_id,
                        Place.address: address,
                    }
                )
                .returning(Place.id)
            )
        ).scalar()

        return place_id

    async def prepare_places_for_tests(self):
        if self.places_ids:
            return self.places_ids

        secret_place_id = "todo"

    async def create_follow(self):
        pass

    async def create_visit(self):
        pass

    async def upload_image(self):
        pass

    async def open_secret_place(self):
        pass
