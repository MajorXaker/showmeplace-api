import graphene
from alchql.fields import FilterConnectionField

from gql.gql_types.category import CategoryType
from gql.gql_types.place import PlaceType
from gql.gql_types.user import UserType
from gql.mutations.add_place import MutationAddPlace
from gql.mutations.add_user import MutationAddUser
from gql.mutations.change_coin_value import MutationChangeCoinValue
from gql.mutations.update_user import MutationEditUser


class Query(graphene.ObjectType):
    select_users = FilterConnectionField(UserType)
    select_places = FilterConnectionField(PlaceType)
    select_category = FilterConnectionField(CategoryType)


class Mutation(graphene.ObjectType):
    add_user = MutationAddUser.Field()
    edit_user = MutationEditUser.Field()
    add_place = MutationAddPlace.Field()
    change_coin_value = MutationChangeCoinValue.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query)
