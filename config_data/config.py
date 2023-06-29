from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class TCSClient:
    token: str   


@dataclass
class Config:
    tcs_client: TCSClient
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('FIGI_BOT_TOKEN')),
                  tcs_client=TCSClient(token=env('TCS_TOKEN')))
                                    