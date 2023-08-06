""" Control global path settings for labctrl """

from __future__ import annotations

from pathlib import Path

import yaml

from labctrl.logger import logger

SETTINGSPATH = Path(__file__).resolve().parent / "settings.yml"


class Settings:
    """ 
    Context manager for settings
    How to use:
    
    with Settings() as settings:
        print(settings.settings)  # to get a list of all available settings
        settings.<setting1> = <value1>
        settings.<setting2> = <value2>
        ...

    The logger will also print all available settings after initializing Settings().
    """

    _settings: set[str] = {"configpath", "datapath", "resourcepath"}

    def __init__(self) -> None:
        """ """

        if SETTINGSPATH.exists():
            with open(SETTINGSPATH, "r") as config:
                settings = yaml.safe_load(config)
        else:
            settings = dict.fromkeys(Settings._settings)

        for name, value in settings.items():
            setattr(self, name, value)
            logger.info(f"Found labctrl setting '{name}' = '{value}'.")
            if value is None:
                logger.info(f"Please set {name} as it is currently set to '{value}'.")

    def __enter__(self) -> Settings:
        """ """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """ """
        settings = {k: v for k, v in self.__dict__.items() if k in self.settings}
        with open(SETTINGSPATH, "w+") as config:
            yaml.safe_dump(settings, config)

    @property
    def settings(self) -> list[str]:
        """ """
        return sorted(Settings._settings)
