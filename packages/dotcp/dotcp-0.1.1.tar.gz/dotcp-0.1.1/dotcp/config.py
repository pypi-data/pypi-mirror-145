import os
from getpass import getuser
from pathlib import PosixPath
from typing import List, Optional

_XDG_CONFIG_HOME = os.getenv("XDG_CONFIG_HOME")

_CONFIG_HOME_PATHS: List[PosixPath] = (
    [PosixPath(_XDG_CONFIG_HOME)] if _XDG_CONFIG_HOME else []
)
_CONFIG_HOME_PATHS.extend(
    [
        PosixPath(PosixPath.home().joinpath(".config")),
        PosixPath(f"/home/{getuser()}/.config"),
        PosixPath("~/.config").expanduser(),
    ]
)


class Config:
    def __init__(
        self,
        overwrite_config_path: Optional[PosixPath] = None,
        overwrite_config_home_path: Optional[PosixPath] = None,
    ):
        if overwrite_config_home_path:
            self.config_home = overwrite_config_home_path.expanduser()
            if not self.config_home.exists():
                raise ValueError(
                    f"provided config home ({overwrite_config_home_path}) does not exist"
                )
        else:
            self.config_home = self.find_config_home()

        if overwrite_config_path:
            self.path = overwrite_config_path.expanduser()
        else:
            self.path = self.config_home.joinpath("dotcp", "config")
        if not self.path.exists():
            raise ValueError(f"dotcp's config ({self.path}) does not exist")

    def find_config_home(self):
        for path in _CONFIG_HOME_PATHS:
            if path.exists():
                return path
        raise RuntimeError(
            "could not detect config home path. Please provide it manually using `--config-home` option or setting $XDG_CONFIG_HOME enviroment variable"
        )

    def get_targets(self):
        targets = []
        with open(self.path, encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                target = PosixPath(self.config_home.joinpath(line))
                if not target.exists():
                    raise RuntimeError(
                        f"target {target} provided in the config does not exist"
                    )
                targets.append(target)
        return targets
