import graphene


class CountableConnectionCreator:
    @classmethod
    def create_type(cls, connection_name, **kwargs):
        class CountableConnection(graphene.relay.Connection):
            count = graphene.Int()
            total_count = graphene.Int()

            class Meta:
                name = connection_name
                node = kwargs["node"]

            @staticmethod
            def resolve_count(root, info, **args):
                return len(root.edges)

        return CountableConnection
