import graphene
from alchql.fields import FilterConnectionField

from gql.gql_types.select_users import SelectUsers
from gql.mutations.add_user import MutationAddUser
from gql.mutations.change_coin_value import MutationChangeCoinValue


class Query(graphene.ObjectType):
    users = FilterConnectionField(SelectUsers)


class Mutation(graphene.ObjectType):
    add_user = MutationAddUser.Field()
    change_coin_value = MutationChangeCoinValue.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query)
