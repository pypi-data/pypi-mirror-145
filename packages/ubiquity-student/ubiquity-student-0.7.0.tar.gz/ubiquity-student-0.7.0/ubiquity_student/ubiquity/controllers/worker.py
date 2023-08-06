"""Module managing the worker"""
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

from enum import unique, IntEnum
from json import loads
from os.path import join, abspath, isfile, dirname
from time import strftime, localtime
from typing import List

import requests
from PySide2.QtCore import QObject, QFileSystemWatcher

from ..model import Model


@unique
class StatusCode(IntEnum):
    """Enum class for status codes"""
    OK = 200
    CREATED = 201


def _get_current_time() -> str:
    """
    Function returning the current time
    :return: The current time
    """
    return strftime("%H:%M:%S", localtime())


class Worker(QObject):
    """Class managing the worker"""
    def __init__(self, model: Model) -> None:
        super().__init__()
        self._model = model
        self._file_paths = self._get_file_paths()
        self.file_system_watcher = QFileSystemWatcher(self._file_paths + self._get_directory_paths())
        self._delete_files_not_exist()
        self._post_all()
        self._set_progress()

    def _get_file_paths(self) -> List[str]:
        """
        Method getting the server file paths
        :return: The list of file paths
        """
        response = requests.get(self._model.url_api_file_paths())
        content = loads(response.content)
        return [join(self._model.directory, file['file_path']) for file in content]

    def _get_file_paths_not_exist(self) -> List[str]:
        """
        Method returning the file paths not exist
        :return: The list of file paths not exist
        """
        return [file_path for file_path in self._file_paths if file_path not in self.file_system_watcher.files()]

    def _get_directory_paths(self) -> List[str]:
        """
        Method returning the directory paths
        :return: The list of directory paths
        """
        return list({self._get_directory(file_path) for file_path in self._file_paths})

    @staticmethod
    def _get_directory(file_path: str) -> str:
        """
        Method returning The directory of the file
        :param file_path: A file path
        :return: The directory of the file
        """
        return dirname(abspath(file_path))

    def add_new_files_in_directory(self, path: str) -> None:
        """
        Method adding and sending the created files to follow
        :param path: The directory path
        """
        for file_path in self._get_file_paths_not_exist():
            if self._get_directory(file_path) == path and isfile(file_path):
                self.file_system_watcher.addPath(file_path)
                self._post(file_path)

    def _delete_files_not_exist(self) -> None:
        """Method deleting and sending the not exist files to follow"""
        for file_path in self._get_file_paths_not_exist():
            if not isfile(file_path):
                self._delete(file_path)

    def _set_progress(self) -> None:
        response = requests.get(self._model.url_api_get_progress())
        self.progress = loads(response.content)

    def _post(self, path: str) -> None:
        """
        Method sending a file by the path
        :param path: The file path
        """
        self.file_system_watcher.removePath(path)
        self.file_system_watcher.addPath(path)
        try:
            with open(path, "r", encoding='utf8') as file:
                data = {'code': file.read()}
            response = requests.post(self._model.url_api_action_file(path[len(self._model.directory):]), data=data)
            if response.status_code in [StatusCode.OK, StatusCode.CREATED]:
                if response.status_code == StatusCode.CREATED:
                    print(f'File {path} created successfully at {_get_current_time()}')
                if response.status_code == StatusCode.OK:
                    print(f'File {path} updated successfully at {_get_current_time()}')
        except UnicodeDecodeError:
            pass

    def _post_all(self) -> None:
        """Method sending all files to follow"""
        for path in self.file_system_watcher.files():
            self._post(path)

    def _delete(self, path: str) -> None:
        """
        Method deleting a file by the path
        :param path: The file path
        """
        self.file_system_watcher.removePath(path)
        response = requests.delete(self._model.url_api_action_file(path[len(self._model.directory):]))
        if response.status_code == StatusCode.OK:
            print(f'File {path} deleted successfully at {_get_current_time()}')

    def post_or_delete(self, path: str) -> None:
        """
        Method sending or deleting a file by the path
        :param path: The file path
        """
        if isfile(path):
            self._post(path)
        else:
            self._delete(path)
        self._set_progress()
