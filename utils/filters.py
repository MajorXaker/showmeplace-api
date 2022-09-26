import datetime

from sqlalchemy import func as f

from models.db_models import Place
from models.enums import SecretPlacesFilterEnum, DecayingPlacesFilterEnum


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
