import random
import re
from datetime import date, datetime, timedelta

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import User, Category, Place


class Creator:
    places_ids = dict()

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name="TestUser", coins:int = 0):
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
        address: str = None
    ):
        if not latitude:
            latitude = random.randint(-90, 90)
        if not longitude:
            longitude = random.randint(-90, 90)
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

    # async def create_lot(
    #     self,
    #     *,
    #     sale_id: int,
    #     artwork_id: int,
    #     description_id: int,
    #     number: str = "1",
    #     status: m.lot.LotStatus = m.lot.LotStatus.UPCOMING,
    #     currency: str = Currency.USD,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     number = str(number)
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Lot)
    #             .values(
    #                 {
    #                     m.Lot.lot_num: number,
    #                     m.Lot.lot_num_number: int(re.sub(r"[^\d]", "", number)),
    #                     m.Lot.lot_num_alpha: re.sub(r"[\d]", "", number),
    #                     m.Lot.sale_id: sale_id,
    #                     m.Lot.auction_house_id: sa.select(
    #                         [m.Sale.auction_house_id]
    #                     ).where(m.Sale.id == sale_id),
    #                     m.Lot.artwork_id: artwork_id,
    #                     m.Lot.description_id: description_id,
    #                     m.Lot.status: status,
    #                     m.Lot.currency: currency,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Lot.raw_lot_id)
    #         )
    #     ).scalar()
    #
    # async def create_sale(
    #     self,
    #     *,
    #     name: str = None,
    #     is_online: bool = False,
    #     status: m.sale.SaleStatus = m.sale.SaleStatus.UPCOMING,
    #     start_datetime: datetime = None,
    #     end_datetime: datetime = None,
    #     auction_house_id: int = None,
    #     location: str = None,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     start_date = start_datetime or datetime.utcnow() + timedelta(days=5)
    #     end_date = end_datetime or start_date + timedelta(days=5)
    #     if not auction_house_id:
    #         auction_house_id = await self.create_auction_house(name="name")
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Sale)
    #             .values(
    #                 {
    #                     m.Sale.name: name or "test sale",
    #                     m.Sale.is_online: is_online,
    #                     m.Sale.status: status,
    #                     m.Sale.start_datetime: start_date,
    #                     m.Sale.end_datetime: end_date,
    #                     m.Sale.auction_house_id: auction_house_id,
    #                     m.Sale.location: location,
    #                     m.Sale.currency: Currency.USD,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Sale.id)
    #         )
    #     ).scalar()
    #
    # async def create_auction_house(self, *, name: str, data: dict = None) -> int:
    #     data = data or {}
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.AuctionHouse)
    #             .values(
    #                 {
    #                     m.AuctionHouse.name: name,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.AuctionHouse.id)
    #         )
    #     ).scalar()
    #
    # async def create_artist(
    #     self,
    #     *,
    #     name: str = "Picasso",
    #     xgboost_calculated: bool = True,
    #     cognito_user_id=None,
    #     photo_id=None,
    #     uid: str = None,
    #     slug: str = None,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     uid = uid or await get_uid_async(self.session, m.Artist)
    #     slug = slug or f"artist-{uid}"
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Artist)
    #             .values(
    #                 {
    #                     m.Artist.name: name,
    #                     m.Artist.xgboost_calculated: xgboost_calculated,
    #                     m.Artist.cognito_user_id: cognito_user_id,
    #                     m.Artist.photo_id: photo_id,
    #                     m.Artist.uid: uid,
    #                     m.Artist.slug: slug,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Artist.id)
    #         )
    #     ).scalar()
    #
    # async def create_description(
    #     self,
    #     *,
    #     name: str = None,
    #     artist_id: int = None,
    #     image_id: int = None,
    #     value_chart_image_id: int = None,
    #     image_vector_id: int = None,
    #     category_id: int = None,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     if not artist_id:
    #         artist_id = await self.create_artist()
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Description)
    #             .values(
    #                 {
    #                     m.Description.name: name,
    #                     m.Description.artist_id: artist_id,
    #                     m.Description.image_id: image_id,
    #                     m.Description.value_chart_image_id: value_chart_image_id,
    #                     m.Description.image_vector_id: image_vector_id,
    #                     m.Description.category_id: category_id,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Description.id)
    #         )
    #     ).scalar()
    #
    # async def create_user(
    #     self,
    #     *,
    #     cognito_subject_id: str = "cognito_id",
    #     preferred_currency: Currency = None,
    #     retool: bool = False,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     user_id = (
    #         await self.session.execute(
    #             sa.insert(m.User)
    #             .values(
    #                 {
    #                     m.User.cognito_subject_id: cognito_subject_id,
    #                     m.User.preferred_currency: preferred_currency,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.User.id)
    #         )
    #     ).scalar()
    #
    #     if retool:
    #         await self.add_user_to_retool(user_id)
    #
    #     return user_id
    #
    # async def create_artwork(
    #     self,
    #     *,
    #     description_id: int,
    #     currency: str = Currency.USD,
    #     uid: str = None,
    #     slug: str = None,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     uid = uid or await get_uid_async(self.session, m.Artwork)
    #     slug = slug or f"artwork-{uid}"
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Artwork)
    #             .values(
    #                 {
    #                     m.Artwork.description_id: description_id,
    #                     m.Artwork.uid: uid,
    #                     m.Artwork.slug: slug,
    #                     m.Artwork.currency: currency,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Artwork.id)
    #         )
    #     ).scalar()
    #
    # async def create_collectable(
    #     self,
    #     *,
    #     description_id: int,
    #     cognito_user_id: str,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     collectable_uid = await get_uid_async(self.session, m.Collectable)
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Collectable)
    #             .values(
    #                 {
    #                     m.Collectable.description_id: description_id,
    #                     m.Collectable.cognito_user_id: cognito_user_id,
    #                     m.Collectable.uid: collectable_uid,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Collectable.id)
    #         )
    #     ).scalar()
    #
    # async def create_image(
    #     self,
    #     *,
    #     s3_key: str = None,
    #     original_url: str = None,
    #     s3_presigned_url: str = None,
    #     thumbnail_s3_presigned_url: str = None,
    #     medium_s3_presigned_url: str = None,
    #     large_s3_presigned_url: str = None,
    #     data: dict = None,
    # ) -> int:
    #     data = data or {}
    #
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Image)
    #             .values(
    #                 {
    #                     m.Image.s3_key: s3_key,
    #                     m.Image.original_url: original_url,
    #                     m.Image.s3_presigned_url: s3_presigned_url,
    #                     m.Image.thumbnail_s3_presigned_url: thumbnail_s3_presigned_url,
    #                     m.Image.medium_s3_presigned_url: medium_s3_presigned_url,
    #                     m.Image.large_s3_presigned_url: large_s3_presigned_url,
    #                     **data,
    #                 }
    #             )
    #             .returning(m.Image.id)
    #         )
    #     ).scalar()
    #
    # async def create_retool_user(self, *, cognito_user_id: str = "cognito_id"):
    #     await self.session.execute(
    #         sa.insert(m.RetoolUser).values(
    #             {m.RetoolUser.cognito_user_id: cognito_user_id}
    #         )
    #     )
    #
    # async def calculate_sales(self):
    #     sales_data = (
    #         await self.session.execute(
    #             sa.select(
    #                 m.Sale.id,
    #                 sa.func.sum(m.Lot.premium_price_estimate_max_usd_zeroied).label(
    #                     "high_estimate_usd"
    #                 ),
    #                 sa.func.sum(m.Lot.premium_price_estimate_min_usd_zeroied).label(
    #                     "low_estimate_usd"
    #                 ),
    #                 sa.func.sum(m.Lot.premium_price_estimate_max).label(
    #                     "high_estimate"
    #                 ),
    #                 sa.func.sum(m.Lot.premium_price_estimate_min).label("low_estimate"),
    #                 sa.func.count(m.Lot.raw_lot_id.distinct()).label("lots_count"),
    #                 sa.func.sum(m.Lot.hammer_price_usd_zeroied).label(
    #                     "hammer_total_usd_zeroied"
    #                 ),
    #                 sa.func.sum(m.Lot.hammer_price_sold).label("hammer_total"),
    #                 sa.func.sum(m.Lot.premium_price_sold).label("premium_sold_total"),
    #                 sa.func.sum(m.Lot.premium_price_usd_zeroied).label(
    #                     "premium_sold_total_usd_zeroied"
    #                 ),
    #                 sa.funcfilter(
    #                     sa.func.count(m.Lot.raw_lot_id.distinct()),
    #                     sa.and_(
    #                         m.Lot.status == LotStatus.SOLD,
    #                         sa.func.coalesce(m.Lot.hammer_price_sold, 0)
    #                         < m.Lot.hammer_price_estimate_min,
    #                     ),
    #                 ).label("lots_count_sold_below_estimations"),
    #                 sa.funcfilter(
    #                     sa.func.count(m.Lot.raw_lot_id.distinct()),
    #                     sa.and_(
    #                         m.Lot.status == LotStatus.SOLD,
    #                         sa.func.coalesce(m.Lot.hammer_price_sold, 0)
    #                         > m.Lot.hammer_price_estimate_max,
    #                     ),
    #                 ).label("lots_count_sold_above_estimations"),
    #                 sa.funcfilter(
    #                     sa.func.count(m.Lot.raw_lot_id.distinct()),
    #                     sa.and_(
    #                         m.Lot.status == LotStatus.SOLD,
    #                         sa.func.coalesce(m.Lot.hammer_price_sold, 0)
    #                         < m.Lot.hammer_price_estimate_max,
    #                         sa.func.coalesce(m.Lot.hammer_price_sold, 0)
    #                         > m.Lot.hammer_price_estimate_min,
    #                     ),
    #                 ).label("lots_count_sold_within_estimations"),
    #                 sa.funcfilter(
    #                     sa.func.count(m.Lot.raw_lot_id.distinct()),
    #                     m.Lot.status != LotStatus.SOLD,
    #                 ).label("lots_count_not_sold"),
    #             )
    #             .select_from(sa.join(m.Sale, m.Lot, m.Sale.id == m.Lot.sale_id))
    #             .group_by(m.Sale.id)
    #             .order_by(m.Sale.id)
    #         )
    #     ).fetchall()
    #
    #     for sale in sales_data:
    #         data_to_update = {
    #             m.Sale.id.key: sale.id,
    #             m.Sale.hammer_high_estimate_usd_zeroied.key: sale.high_estimate_usd,
    #             m.Sale.hammer_high_estimate.key: sale.high_estimate,
    #             m.Sale.hammer_low_estimate_usd_zeroied.key: sale.low_estimate_usd,
    #             m.Sale.hammer_low_estimate.key: sale.low_estimate,
    #             m.Sale.lots_count.key: sale.lots_count,
    #             m.Sale.lots_count_not_sold.key: sale.lots_count_not_sold,
    #             m.Sale.lots_count_sold_above_estimations.key: sale.lots_count_sold_above_estimations,
    #             m.Sale.lots_count_sold_below_estimations.key: sale.lots_count_sold_below_estimations,
    #             m.Sale.lots_count_sold_within_estimations.key: sale.lots_count_sold_within_estimations,
    #             m.Sale.hammer_total_usd_zeroied.key: sale.hammer_total_usd_zeroied,
    #             m.Sale.hammer_total.key: sale.hammer_total,
    #             m.Sale.premium_sold_total.key: sale.premium_sold_total,
    #             m.Sale.premium_sold_total_usd_zeroied.key: sale.premium_sold_total_usd_zeroied,
    #         }
    #         await self.session.execute(
    #             sa.update(m.Sale).where(m.Sale.id == sale.id).values(data_to_update)
    #         )
    #
    # async def create_buyers_premium_rate(
    #     self,
    #     *,
    #     currency: Currency,
    #     auction_house_id: int,
    #     curr_date: date,
    #     rate_type: str,
    #     low_boundary: int,
    #     high_boundary: int,
    #     value: float,
    # ):
    #     await self.session.execute(
    #         sa.insert(m.BuyersPremiumRate).values(
    #             {
    #                 m.BuyersPremiumRate.currency: currency,
    #                 m.BuyersPremiumRate.auction_house_id: auction_house_id,
    #                 m.BuyersPremiumRate.date_start: curr_date,
    #                 m.BuyersPremiumRate.price_low_boundary: low_boundary,
    #                 m.BuyersPremiumRate.price_high_boundary: high_boundary,
    #                 m.BuyersPremiumRate.value: value,
    #                 m.BuyersPremiumRate.rate_type: rate_type,
    #             }
    #         )
    #     )
    #
    # async def create_currency(self, *, name: Currency):
    #     await self.session.execute(
    #         sa.insert(m.Currency).values(
    #             {
    #                 m.Currency.code: name,
    #                 m.Currency.name: name,
    #             }
    #         )
    #     )
    #
    # async def create_category(self, *, name="name", label="label") -> int:
    #     return (
    #         await self.session.execute(
    #             sa.insert(m.Category)
    #             .values(
    #                 {
    #                     m.Category.name: name,
    #                     m.Category.label: label,
    #                 }
    #             )
    #             .returning(m.Category.id)
    #         )
    #     ).scalar()
    #
    # async def add_user_to_retool(self, user_id: int):
    #     await self.session.execute(
    #         sa.insert(m.RetoolUser).values(
    #             {
    #                 m.RetoolUser.cognito_user_id: sa.select(m.User.cognito_subject_id)
    #                 .where(m.User.id == user_id)
    #                 .scalar_subquery()
    #             }
    #         )
    #     )
    #
    # async def create_artwork_share(
    #     self,
    #     *,
    #     artwork_ids: list[int],
    #     token: str,
    #     currency: str,
    # ) -> int:
    #     insert_result = await self.session.execute(
    #         sa.insert(m.ArtworkShare)
    #         .values(
    #             {
    #                 m.ArtworkShare.token: token,
    #                 m.ArtworkShare.preferred_currency: currency,
    #                 m.ArtworkShare.user_id: "placeholder",
    #             }
    #         )
    #         .returning(m.ArtworkShare.id)
    #     )
    #     artwork_share_id = insert_result.scalar()
    #     await self.session.execute(
    #         sa.insert(m.M2MArtworkArtworkShare).values(
    #             [
    #                 {
    #                     m.M2MArtworkArtworkShare.artwork_share_id: artwork_share_id,
    #                     m.M2MArtworkArtworkShare.artwork_id: artwork_id,
    #                 }
    #                 for artwork_id in artwork_ids
    #             ]
    #         )
    #     )
    #     return artwork_share_id
    #
    # async def create_m2m_description_image(self, description_id: int, image_id: int):
    #     await self.session.execute(
    #         sa.insert(m.M2MDescriptionImage).values(
    #             {
    #                 m.M2MDescriptionImage.description_id: description_id,
    #                 m.M2MDescriptionImage.image_id: image_id,
    #             }
    #         )
    #     )
    #
    # async def add_test_collectable_with_images(
    #     self, cognito_user_id: str, images_count: int = 2
    # ):
    #     artist_id = await self.create_artist()
    #     description_id = await self.create_description(artist_id=artist_id)
    #     for _ in range(images_count):
    #         image_id = await self.create_image()
    #         await self.create_m2m_description_image(description_id, image_id)
    #     collectable_id = await self.create_collectable(
    #         description_id=description_id, cognito_user_id=cognito_user_id
    #     )
    #     return collectable_id
