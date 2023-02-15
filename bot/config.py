import json
import os.path
from collections import defaultdict
from typing import TypedDict, Dict


class VoiceClearConfig(TypedDict):
    enabled_channels: list[int]


class GuildConfig(TypedDict):
    voice_clear: VoiceClearConfig


def _get_default_config() -> GuildConfig:
    return GuildConfig(
        voice_clear=VoiceClearConfig(enabled_channels=[])
    )


class Config:
    _per_guild_configs: Dict[int, GuildConfig]

    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            config_file = open(self.path, "w")
            json.dump(dict(), config_file)
            config_file.close()

        with open(self.path, "r") as config_file:
            self._per_guild_configs = defaultdict(_get_default_config, {int(k): v for k, v in json.load(config_file).items()})

    def get_config(self, guild_id: int) -> GuildConfig:
        return self._per_guild_configs[guild_id]

    def persist(self):
        with open(self.path, "w") as config_file:
            json.dump(self._per_guild_configs, config_file)
