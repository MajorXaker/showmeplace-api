from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id
import sqlalchemy as sa

class AuthChecker():

    class NotAuthorisedException(ConnectionRefusedError):
        pass
        # raise ConnectionRefusedError("Unathorised connection")

    @classmethod
    def check_auth_request(cls,info):
        for header in info.context.request.headers.raw:
            if header[0] == b'user_auth':
                active_user = header[1]
                user_id = decode_gql_id(active_user)[1]
                return user_id
        raise cls.NotAuthorisedException('Unathorised connection')

    def check_auth_mutation(self,session:AsyncSession, info):
        id = self.check_auth_request(info)
        await session.execute()