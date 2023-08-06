"""Module model managing the application states"""
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
from typing import Optional, List

from PySide2.QtCore import QObject, Signal


class Model(QObject):
    """Class managing the states"""
    prefix_server_changed = Signal(str)
    server_changed = Signal(str)
    student_key_changed = Signal(str)
    group_key_changed = Signal(str)
    directory_changed = Signal(str)
    error_changed = Signal(object)

    def __init__(self, values: List[Optional[str]]) -> None:
        super().__init__()
        self._name = ''
        self._error = ''
        self._inputs = ['', '', '', '', '', '']
        self._set_values(values)
        self._client_version_min = None

    def _set_values(self, values: List[Optional[str]]) -> None:
        if values[0]:
            for start in ['https://', 'http://']:
                if values[0].startswith(start):
                    self.prefix_server = start
            self.server = values[0][len(self.prefix_server):] if self.prefix_server != '' else values[0]

        self.student_key = values[1] if values[1] else ''
        self.group_key = values[2] if values[2] else ''
        self.directory = values[3] if values[3] else ''

    @property
    def name(self) -> str:
        """Get the name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name"""
        self._name = value

    @property
    def prefix_server(self) -> str:
        """Get the url server"""
        return self._inputs[0]

    @prefix_server.setter
    def prefix_server(self, value: str) -> None:
        """Set the url server"""
        self._inputs[0] = value
        self.prefix_server_changed.emit(value)

    @property
    def server(self) -> str:
        """Get the url server"""
        return self._inputs[1]

    @server.setter
    def server(self, value: str) -> None:
        """Set the url server"""
        self._inputs[1] = value
        self.server_changed.emit(value)

    @property
    def student_key(self) -> str:
        """Get the student key"""
        return self._inputs[2]

    @student_key.setter
    def student_key(self, value: str) -> None:
        """Set the student key"""
        self._inputs[2] = value
        self.student_key_changed.emit(value)

    @property
    def group_key(self) -> str:
        """Get the group key"""
        return self._inputs[3]

    @group_key.setter
    def group_key(self, value: str) -> None:
        """Set the group key"""
        self._inputs[3] = value
        self.group_key_changed.emit(value)

    @property
    def directory(self) -> str:
        """Get the directory"""
        return self._inputs[4]

    @directory.setter
    def directory(self, value: str) -> None:
        """Set the directory"""
        self._inputs[4] = value
        self.directory_changed.emit(value)

    @property
    def error(self) -> str:
        """Get the error"""
        return self._error

    @error.setter
    def error(self, value: str) -> None:
        """Set the error"""
        self._error = value
        self.error_changed.emit(value)

    @property
    def client_version_min(self) -> str:
        """Get the client version min"""
        return self._client_version_min

    @client_version_min.setter
    def client_version_min(self, value: str) -> None:
        """Set the client version min"""
        self._client_version_min = value

    def _url_api_server(self) -> str:
        return f'{self.prefix_server}{self.server}/api'

    def url_api_check_version(self) -> str:
        """
        Method returning the url for the connection verification to the api
        :return: The string url
        """
        return f'{self._url_api_server()}/check/version'

    def url_api_connection_check(self) -> str:
        """
        Method returning the url for the connection verification to the api
        :return: The string url
        """
        return f'{self._url_api_server()}/check/{self.student_key}/{self.group_key}'

    def url_api_get_student_environment(self) -> str:
        """
        Method returning the url for get student environment
        :return: The string url
        """
        return f'{self._url_api_server()}/{self.student_key}/{self.group_key}'

    def url_api_restore_student_environment(self) -> str:
        """
        Method returning the url for get student environment restored
        :return: The string url
        """
        return f'{self._url_api_server()}/restore/{self.student_key}/{self.group_key}'

    def url_api_get_progress(self) -> str:
        """
        Method returning the url for get the progress
        :return: The string url
        """
        return f'{self._url_api_server()}/progress/{self.student_key}/{self.group_key}'

    def url_api_file_paths(self) -> str:
        """
        Method returning the url for get path files to follow
        :return: The string url
        """
        return f'{self._url_api_server()}/{self.group_key}'

    def url_api_action_file(self, file_name: str) -> str:
        """
        Method returning the url for the file's action
        :return: The string url
        """
        if len(file_name) > 0 and file_name[0] == '/':
            file_name = file_name[1:]
        return f'{self._url_api_server()}/{self.student_key}/{self.group_key}/code_file/{file_name}'

    def url_web_view(self) -> str:
        """
        Method returning the url for the web view
        :return: The string url
        """
        return f'{self.prefix_server}{self.server}/client/{self.student_key}/{self.group_key}'
