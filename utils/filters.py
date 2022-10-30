import datetime

from sqlalchemy import func as f

from gql.gql_id import gql_decoder
# from gql.gql_types.place_type import CoordinateBox # TODO buggy!
from models.db_models import Place
from models.enums import SecretPlacesFilterEnum, DecayingPlacesFilterEnum
import sqlalchemy as sa

from utils.smp_exceptions import Exc, ExceptionGroupEnum, ExceptionReasonEnum


def secrets_filter(v: SecretPlacesFilterEnum):
    result = {
        SecretPlacesFilterEnum.ALL: True,
        SecretPlacesFilterEnum.SECRET: Place.category_id == 11,
        SecretPlacesFilterEnum.REGULAR: Place.category_id != 11,
    }[v]
    return result


def decaying_filter(v: DecayingPlacesFilterEnum):
    result = {
        DecayingPlacesFilterEnum.ALL: True,
        DecayingPlacesFilterEnum.DECAYING: Place.active_due_date
        > datetime.datetime.now(),
        DecayingPlacesFilterEnum.DECAYED: Place.active_due_date
        < datetime.datetime.now(),
        DecayingPlacesFilterEnum.REGULAR: Place.active_due_date.is_(None),
    }[v]
    return result


def box_coordinates_filter(v):
    # if any(
    #     [
    #         not hasattr(v, "sw_latitude"),
    #         not hasattr(v, "sw_longitude"),
    #         not hasattr(v, "ne_latitude"),
    #         not hasattr(v, "ne_longitude"),
    #     ]
    # ):
    #     Exc.value(
    #         message="Coordinate box incomplete",
    #         of_group=ExceptionGroupEnum.BAD_INPUT,
    #         reasons=ExceptionReasonEnum.MISSING_VALUE,
    #     )

    result = sa.and_(
        Place.coordinate_latitude.between(v.sw_latitude, v.ne_latitude),
        Place.coordinate_longitude.between(v.sw_longitude, v.ne_longitude),
    )
    return result

# @gql_decoder
# def filter_owner(v):
#     return Place.owner_id == v

# @gql_decoder
# def filter_visitor(v):
#     return Place.owner_id == v
