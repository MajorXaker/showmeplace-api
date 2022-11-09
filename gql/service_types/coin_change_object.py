from graphene import ObjectType, String, Int


class CoinChange(ObjectType):
    change_amount = Int()
    coins = Int()
