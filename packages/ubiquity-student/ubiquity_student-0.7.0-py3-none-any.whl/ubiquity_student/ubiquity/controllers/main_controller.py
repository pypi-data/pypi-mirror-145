"""Module managing the application controller"""
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
from enum import unique, Enum, auto
from io import BytesIO
from json import loads
from json.decoder import JSONDecodeError
from os.path import exists
from typing import Optional, Any
from zipfile import ZipFile

import requests
from PySide2.QtCore import QObject, Slot

from .config_file import Config
from .worker import Worker, StatusCode
from .. import __version__
from ..model import Model
from ..views.utils import print_message, LabelEnum, ErrorMessage


@unique
class Returns(Enum):
    """Enum class for returns on submit method"""
    CHOICE = auto()
    OK = auto()
    ERROR = auto()


class MainController(QObject):
    """Class managing the main controller"""
    def __init__(self, config: Config, model: Model) -> None:
        super().__init__()
        self._model = model
        self.worker = None
        self.config = config
        self.is_new_project = False

    @Slot(str)
    def change_prefix_server(self, value: str) -> None:
        """
        Method changing the prefix server state
        :param value: The new value
        """
        self._model.prefix_server = value

    @Slot(str)
    def change_server(self, value: str) -> None:
        """
        Method changing the server state
        :param value: The new value
        """
        self._model.server = value

    @Slot(str)
    def change_student_key(self, value: str) -> None:
        """
        Method changing the student key state
        :param value: The new value
        """
        self._model.student_key = value

    @Slot(str)
    def change_group_key(self, value: str) -> None:
        """
        Method changing the group key state
        :param value: The new value
        """
        self._model.group_key = value

    @Slot(str)
    def change_directory(self, value: str) -> None:
        """
        Method changing the directory state
        :param value: The new value
        """
        self._model.directory = value

    @Slot(object)
    def change_error(self, value: Any) -> None:
        """
        Method changing the error state
        :param value: The new value
        """
        self._model.error = value

    def init_values(self) -> None:
        """Method initializing the state values"""
        if Config.DEFAULT in self.config.configs:
            self.change_prefix_server(self.config.configs[Config.DEFAULT][Config.PREFIX_SERVER])
            self.change_server(self.config.configs[Config.DEFAULT][Config.SERVER])
            self.change_student_key(self.config.configs[Config.DEFAULT][Config.STUDENT_KEY])

    def _check_values(self) -> Optional[ErrorMessage]:
        """
        Method verifying if the state values are valid
        :return: True if the values are valid, False if not
        """
        error = self._check_values_not_empty()
        if error is None:
            error = self._check_connection()
        if error is None:
            error = self._check_directory()
        if isinstance(error, ErrorMessage):
            self.change_error(error)
            return error
        return None

    def _check_values_not_empty(self) -> Optional[ErrorMessage]:
        """
        Method verifying if the state values are not empty
        :return: None if the values are valid, Error if not
        """
        if "" in [self._model.server, self._model.student_key, self._model.group_key, self._model.directory]:
            return ErrorMessage.EMPTY_FIELD
        return None

    def _check_version(self) -> Optional[ErrorMessage]:
        """
        Method verifying if the client version is OK
        :return: None if the client version is OK, Error if not
        """
        response = requests.get(self._model.url_api_check_version())
        try:
            content = loads(response.content)
            self._model.client_version_min = content['version_min']
            if content['version_min'] <= __version__:
                return None
        except JSONDecodeError:
            return None
        return ErrorMessage.VERSION

    def _check_connection(self) -> Optional[ErrorMessage]:
        """
        Method verifying if the connection is OK
        :return: None if the status code is OK, Error if not
        """
        try:
            response = self._check_version()
            if response:
                return response
            response = requests.get(self._model.url_api_connection_check())
            if response.status_code != StatusCode.OK:
                if self.config.check_is_config(self._model):
                    return ErrorMessage.CONFIG_DELETED
                return ErrorMessage.INVALID_KEYS
            content = loads(response.content)
            self._model.name = content['name']
            self.is_new_project = content['is_new']
        except requests.exceptions.RequestException:
            return ErrorMessage.CONNECTION_FAILED
        return None

    def _check_directory(self) -> Optional[ErrorMessage]:
        """
        Method verifying if the directory exits
        :return: None if exists, Error if not
        """
        if not exists(self._model.directory):
            return ErrorMessage.DIRECTORY_DOES_NOT_EXIST
        return None

    def extract_zip(self, new: bool = True) -> None:
        """
        Extract a zip file to the working directory
        :param new: True if is a new project, False if restore
        """
        url = self._model.url_api_get_student_environment() if new else \
            self._model.url_api_restore_student_environment()
        response = requests.get(url)
        with ZipFile(BytesIO(response.content)) as zip_file:
            print_message(LabelEnum.STUDENT_ENVIRONMENT_RECOVERED)
            for names in zip_file.namelist():
                zip_file.extract(names, self._model.directory)
        print_message(LabelEnum.EXTRACT_ZIP_COMPLETED, 1)

    def _check_is_new(self) -> bool:
        """
        Method checking if is a new project
        :return: True if is a new project, False if not
        """
        return not self.config.check_is_config(self._model)

    def _add_config(self) -> None:
        """Method adding a config"""
        self.config.add_config(self._model)

    def update_with_config(self, config: dict) -> None:
        """
        Method updating the model with the config values
        :param config: The config
        """
        self._model.prefix_server = config[Config.PREFIX_SERVER]
        self._model.server = config[Config.SERVER]
        self._model.student_key = config[Config.STUDENT_KEY]
        self._model.group_key = config[Config.GROUP_KEY]
        self._model.directory = config[Config.DIRECTORY]
        self._model.error = ''

    def run(self) -> None:
        """Method running the worker and add values in the config file"""
        self._add_config()
        self.worker = Worker(self._model)

    def submit(self) -> Returns:
        """
        Method verifying the values and run the worker
        :return: The status of the return on the form validation
        """
        error = self._check_values()
        if not isinstance(error, ErrorMessage):
            if self.is_new_project:
                self.extract_zip()
            elif not self.config.check_directory(self._model):
                return Returns.CHOICE
            return Returns.OK
        if error is not ErrorMessage.VERSION and error is not ErrorMessage.CONNECTION_FAILED and \
                self.config.check_is_config(self._model):
            self.config.remove_config(self._model)
        return Returns.ERROR
