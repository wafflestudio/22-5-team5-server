import os

from pydantic_settings import BaseSettings

# TODO 환경 변수로 설정된 환경을 가져옵니다.
# 가능한 값은 "local", "test", "prod" 이며, 기본값은 "local" 입니다.
# 환경 변수는 어떻게 바꿀 수 있을까요?
ENV = os.getenv("ENV", "local")
assert ENV in ("local", "test", "prod")


class Settings(BaseSettings):
    # TODO property 데코레이터는 메서드를 필드처럼 사용할 수 있게 해줍니다.
    # 예컨데, SETTINGS.is_local() 대신 SETTINGS.is_local 으로 사용할 수 있습니다.
    @property
    def is_local(self) -> bool:
        return ENV == "local"

    @property
    def is_prod(self) -> bool:
        return ENV == "prod"

    @property
    def env_file(self) -> str:
        return f".env.{ENV}"


# TODO SETTINGS 는 런타임에 변경되지 않으므로 미리 초기화해둡니다.
SETTINGS = Settings()