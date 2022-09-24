import datetime

from models.db_models import Place
from models.enums import SecretPlacesFilterEnum, DecayingPlacesFilterEnum
from sqlalchemy import func as f

def secrets_filter(v: SecretPlacesFilterEnum):
    result = {
        SecretPlacesFilterEnum.ALL: Place.category_id,
        SecretPlacesFilterEnum.SECRET: Place.category_id == 11,
        SecretPlacesFilterEnum.REGULAR: Place.category_id != 11,
    }[v]
    return result

def decaying_filter(v: DecayingPlacesFilterEnum):
    result = {
        DecayingPlacesFilterEnum.ALL: f.coalesce(Place.active_due_date, 0),
        DecayingPlacesFilterEnum.DECAYING: Place.active_due_date > datetime.datetime.now(),
        DecayingPlacesFilterEnum.DECAYED: Place.active_due_date > datetime.datetime.now(),
        DecayingPlacesFilterEnum.REGULAR: Place.active_due_date.is_(None),
    }[v]
    return result
