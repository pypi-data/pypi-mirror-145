"""Module managing the configurations"""
#      ubiquity
#      Copyright (C) 2022  INSA Rouen Normandie - CIP
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from json import dumps, load, JSONDecodeError
from os.path import join, expanduser, isfile

from ..model import Model


def _get_config_file(config_file_name: str) -> str:
    """
    Function returning the config file path
    :param config_file_name: The config file name
    :return: The config file path
    """
    return join(expanduser("~"), config_file_name)


def _get_key(model: Model) -> str:
    """
    Function returning the config key
    :param model: The model
    :return: the config key
    """
    return f'{model.group_key}_{model.student_key}'


class Config:
    """Class managing the configurations"""
    _CONFIG_FILE_NAME = '.ubiquity'
    PREFIX_SERVER = 'prefix_server'
    SERVER = 'server'
    STUDENT_KEY = 'student_key'
    GROUP_KEY = 'group_key'
    NAME = 'name'
    DIRECTORY = 'directory'
    DEFAULT = 'default'

    def __init__(self) -> None:
        self.path_config_file = _get_config_file(Config._CONFIG_FILE_NAME)
        if self._check_has_not_config():
            self._write_config_file({})
        self.configs = self._read_config_file()

    def _check_has_not_config(self) -> bool:
        """
        Method checking if the config file not exist
        :return: True if the config file not exist, False if exist
        """
        return not isfile(self.path_config_file)

    def _read_config_file(self) -> dict:
        """
        Method returning the config file content
        :return: The config file content
        """
        with open(self.path_config_file, encoding="utf-8") as config_file:
            try:
                configs = load(config_file)
            except JSONDecodeError:
                configs = {}
        config_file.close()
        return configs

    def _default_config(self, prefix_server: str, server: str, student_key: str) -> None:
        """
        Method setting the default config
        :param prefix_server: The prefix server
        :param server: The server url
        :param student_key: The student key
        """
        self.configs[Config.DEFAULT] = {}
        self.configs[Config.DEFAULT][Config.PREFIX_SERVER] = prefix_server
        self.configs[Config.DEFAULT][Config.SERVER] = server
        self.configs[Config.DEFAULT][Config.STUDENT_KEY] = student_key

    def add_config(self, model: Model) -> None:
        """
        Method adding a config; Or updating if exist
        :param model: The model
        """
        self._default_config(model.prefix_server, model.server, model.student_key)
        key = _get_key(model)
        self.configs[key] = {}
        self.configs[key][Config.NAME] = model.name
        self.configs[key][Config.PREFIX_SERVER] = model.prefix_server
        self.configs[key][Config.SERVER] = model.server
        self.configs[key][Config.STUDENT_KEY] = model.student_key
        self.configs[key][Config.GROUP_KEY] = model.group_key
        self.configs[key][Config.DIRECTORY] = model.directory
        self._write_config_file(self.configs)

    def remove_config(self, model: Model) -> None:
        """
        Method removing a config by a group key
        :param model: The model
        """
        self.configs.pop(_get_key(model))
        self._write_config_file(self.configs)

    def check_is_config(self, model: Model) -> bool:
        """
        Method checking if config exist
        :param model: The model
        :return: True if the values exist in the config file. False if not
        """
        key = _get_key(model)
        if key in self.configs:
            config = self.configs[key]
            if config[Config.PREFIX_SERVER] == model.prefix_server and config[Config.SERVER] == model.server and \
                    config[Config.STUDENT_KEY] == model.student_key and config[Config.DIRECTORY] == model.directory:
                return True
        return False

    def check_directory(self, model: Model) -> bool:
        """
        Method checking if directory exist and if is in the config file
        :param model: The model
        :return: True if the directory is valid. False if not
        """
        key = _get_key(model)
        if key in self.configs:
            return self.configs[key][Config.DIRECTORY] == model.directory
        return False

    def _write_config_file(self, configs: dict) -> None:
        """
        Method writing the config file
        :param configs: The configs
        """
        with open(self.path_config_file, 'w+', encoding='utf8') as config_file:
            config_file.write(dumps(configs))
        config_file.close()
