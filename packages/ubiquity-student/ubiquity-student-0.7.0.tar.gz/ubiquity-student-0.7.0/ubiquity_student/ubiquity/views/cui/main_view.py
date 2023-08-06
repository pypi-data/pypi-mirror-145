"""Module managing the console application views"""
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
import sys
from typing import Any

from PySide2.QtCore import Slot

from .form_view import FormView
from ..utils import is_success_run, LabelEnum, print_message, print_value, get_color_value, get_percent_value
from ...controllers.main_controller import Returns


class MainView:
    """Class managing the main view"""
    def __init__(self, model: Any, main_controller: Any, has_form: bool, has_color: bool) -> None:
        super().__init__()
        self._model = model
        self._model.error_changed.connect(self.on_error_change)

        self._main_controller = main_controller
        self._ui = FormView(model, has_color)
        self._has_color = has_color
        self.has_form = has_form
        self._ui.form_values(self.has_form)
        if self.has_form:
            while not self.submit():
                pass
        else:
            if not self.submit():
                sys.exit(0)

    def _file_changed(self, path: str) -> None:
        """
        Method on a modified file
        :param path: The file path
        """
        self._main_controller.worker.post_or_delete(path)
        self._show_progress()

    def _directory_changed(self, path: str) -> None:
        """
        Method on a modified directory
        :param path: The directory path
        """
        self._main_controller.worker.add_new_files_in_directory(path)

    def _show_progress(self):
        progress = self._main_controller.worker.progress['progress']
        average_progress = self._main_controller.worker.progress['average_progress']
        missing_files = self._main_controller.worker.progress['missing_files']
        code_files = self._main_controller.worker.progress['code_files']
        print_message(LabelEnum.PROGRESS_INFORMATION, end=' ')
        print_message(LabelEnum.PROGRESS, end=' ')
        print_value(get_percent_value(progress), color=get_color_value(self._has_color, progress), end=' ; ')
        print_message(LabelEnum.AVERAGE_PROGRESS, end=' ')
        print_value(get_percent_value(average_progress), color=get_color_value(self._has_color, average_progress),
                    end=' ; ')
        if missing_files > 0:
            print_message(LabelEnum.MISSING_FILES, end=' ')
            print_value(missing_files, end=' ; ')
        print_message(LabelEnum.FILES, enter=1, start=' '*3, end=' ')
        print_value(len(code_files))
        for file_path in code_files:
            print_value(file_path, start=' '*6, end=' :\n')
            max_len_code_block_name = len(max(code_files[file_path], key=len))
            for code_block in code_files[file_path]:
                print_value(code_block, start=' '*9, end=' '*(max_len_code_block_name-len(code_block)) + " : ")
                for key in code_files[file_path][code_block]:
                    value = code_files[file_path][code_block][key]
                    if key == 'progress':
                        print_message(LabelEnum.PROGRESS, end=' ')
                    else:
                        print_message(LabelEnum.AVERAGE, end=' ')
                    print_value(get_percent_value(value), color=get_color_value(self._has_color, value), end=' ; ')
                print()
        print()

    def submit(self) -> bool:
        """
        Method of action on the validation
        return True if submit is ok, False if not
        """
        self._main_controller.change_prefix_server(self._ui.prefix_server)
        self._main_controller.change_server(self._ui.server)
        self._main_controller.change_student_key(self._ui.student_key)
        self._main_controller.change_group_key(self._ui.group_key)
        self._main_controller.change_directory(self._ui.directory)
        response = self._main_controller.submit()
        if response == Returns.CHOICE:
            choice = self._ui.choice()
            if choice == '1':
                self._main_controller.extract_zip(False)
                response = Returns.OK
            elif choice == '2':
                self._main_controller.extract_zip()
                response = Returns.OK
            else:
                self._ui.cancel_choice(self.has_form)
        if response == Returns.OK:
            is_success_run(self._has_color)
            self._main_controller.run()
            self._show_progress()
            self._main_controller.worker.file_system_watcher.fileChanged.connect(self._file_changed)
            self._main_controller.worker.file_system_watcher.directoryChanged.connect(self._directory_changed)
            return True
        return False

    @Slot(object)
    def on_error_change(self, value: Any) -> None:
        """
        Method displaying the error message
        :param value: The error message
        """
        self._ui.error_values(value, self.has_form)
