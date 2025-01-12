from wastory.database.connection import SESSION, reset_session, start_new_session_if_not_exists


from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
RT = TypeVar("RT")


def transactional(f: Callable[P, Awaitable[RT]]) -> Callable[P, Awaitable[RT]]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        tokens = start_new_session_if_not_exists()
        # 이미 현재 태스크에서 생성된 세션이 있는 경우 tokens 는 None
        if tokens is None:
            return await f(*args, **kwargs)
        try:
            ret = await f(*args, **kwargs)
        except Exception as e:
            await SESSION.rollback()
            raise e
        else:
            await SESSION.commit()
        finally:
            await SESSION.close()
            reset_session(tokens)
        return ret
    return wrapper