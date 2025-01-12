from starlette.middleware.base import BaseHTTPMiddleware

from wastory.database.connection import SESSION, reset_session, start_default_session


class DefaultSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tokens = start_default_session()
        try:
            response = await call_next(request)
        except Exception as e:
            raise e
        else:
            await SESSION.commit()
        finally:
            await SESSION.close()
            reset_session(tokens)
        return response