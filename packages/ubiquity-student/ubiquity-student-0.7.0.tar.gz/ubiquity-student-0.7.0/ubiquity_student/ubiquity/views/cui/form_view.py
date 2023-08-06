"""Module managing the form console"""
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
from ..utils import ConsoleColor, print_message, LabelEnum, ErrorMessage


def _request_value(label_input: LabelEnum, space: int = 0) -> str:
    """
    Function displaying an input field and requesting value
    :param label_input: The label
    :param space: The number of spaces
    :return: The input value
    """
    print(label_input.value.rjust(space) + " :", end=' ')
    return input()


def _input_value(label_input: LabelEnum, value: str, space: int = 0) -> None:
    """
    Function displaying an input field
    :param label_input: The label
    :param value: The value
    :param space: The number of spaces
    """
    print(label_input.value.rjust(space) + " : " + value)


class FormView:
    """Class managing the form view"""
    def __init__(self, model, has_color: bool = True):
        self._has_color = has_color
        has_server = not model.server == ''
        has_student_key = not model.student_key == ''
        has_group_key = not model.group_key == ''
        has_directory = not model.directory == ''

        self.input_list = {
            LabelEnum.SERVER: {
                'has': has_server,
                'value': None if not has_server else model.prefix_server + model.server
            },
            LabelEnum.STUDENT_KEY: {
                'has': has_student_key,
                'value': None if not has_student_key else model.student_key
            },
            LabelEnum.GROUP_KEY: {
                'has': has_group_key,
                'value': None if not has_group_key else model.group_key
            },
            LabelEnum.DIRECTORY: {
                'has': has_directory,
                'value': None if not has_directory else model.directory
            }
        }

    @property
    def prefix_server(self) -> str:
        """
        Property returning the prefix server
        :return: The prefix server
        """
        for start in ['https://', 'http://']:
            if self.input_list[LabelEnum.SERVER]['value'].startswith(start):
                return start
        return ''

    @property
    def server(self) -> str:
        """
        Property returning the server
        :return: The server
        """
        for start in ['https://', 'http://']:
            if self.input_list[LabelEnum.SERVER]['value'].startswith(start):
                return self.input_list[LabelEnum.SERVER]['value'][len(start):]
        return self.input_list[LabelEnum.SERVER]['value']

    @property
    def student_key(self) -> str:
        """
        Property returning the student key
        :return: The student key
        """
        return self.input_list[LabelEnum.STUDENT_KEY]['value']

    @property
    def group_key(self) -> str:
        """
        Property returning the group key
        :return: The group key
        """
        return self.input_list[LabelEnum.GROUP_KEY]['value']

    @property
    def directory(self) -> str:
        """
        Property returning the directory
        :return: The directory
        """
        return self.input_list[LabelEnum.DIRECTORY]['value']

    def _display_or_request_value(self, label: LabelEnum, spaces_number: int) -> None:
        """
        Method displaying or requesting a value
        :param label: The label
        :param spaces_number: The number of spaces
        """
        if self.input_list[label]['has']:
            _input_value(label, self.input_list[label]['value'], spaces_number)
        else:
            self.input_list[label]['value'] = _request_value(label, spaces_number)

    def request_values(self, has_form: bool) -> None:
        """
        Method requesting the values
        :param has_form: If there has form or not
        """
        if has_form:
            print_message(LabelEnum.INFORMATION_REQUEST)
        else:
            print_message(LabelEnum.INFORMATION_DISPLAY)
        spaces_number = LabelEnum.spaces_number()

        self._display_or_request_value(LabelEnum.SERVER, spaces_number)
        self._display_or_request_value(LabelEnum.STUDENT_KEY, spaces_number)
        self._display_or_request_value(LabelEnum.GROUP_KEY, spaces_number)
        self._display_or_request_value(LabelEnum.DIRECTORY, spaces_number)

    def confirm_values(self) -> bool:
        """
        Method static requesting confirm values
        :return: True if is confirmed, False if not
        """
        confirm = _request_value(LabelEnum.CONFIRM)
        is_confirm = confirm in ['y', 'Y']
        if is_confirm:
            print_message(LabelEnum.IS_CONFIRM, 1)
        else:
            print_message(LabelEnum.IS_NOT_CONFIRM, 1, ConsoleColor.WARNING if self._has_color else None)
        return is_confirm

    def error_values(self, error: ErrorMessage, request_again: bool) -> None:
        """
        Methode displaying the error message and run the form
        :param error: The error message
        :param request_again: If request the form again or not
        """
        print_message(error, 1, ConsoleColor.ERROR if self._has_color else None)
        if request_again:
            self.form_values(request_again)

    def form_values(self, has_form: bool) -> None:
        """
        Methode run the form
        :param has_form: If there has form or not
        """
        self.request_values(has_form)
        if has_form and not self.confirm_values():
            self.form_values(has_form)

    @staticmethod
    def choice() -> str:
        """
        Method requesting the choice
        :return: The input value
        """
        return _request_value(LabelEnum.RESTORE_OR_RESET)

    def cancel_choice(self, request_again: bool) -> None:
        """
        Methode displaying the cancel message and run the form
        :param request_again: If request the form again or not
        """
        print_message(LabelEnum.CANCEL_CHOICE, 0, ConsoleColor.WARNING if self._has_color else None)
        if request_again:
            self.form_values(request_again)
