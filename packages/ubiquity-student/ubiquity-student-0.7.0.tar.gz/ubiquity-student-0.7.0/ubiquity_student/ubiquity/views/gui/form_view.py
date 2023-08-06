"""Module managing the form window"""
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

from typing import List, Any, Optional, Tuple

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLineEdit, QLabel, QPushButton, QWidget, QComboBox, QDialog, QListWidget, \
    QListWidgetItem

from ..utils import LabelEnum


def create_grid_layout(elements: List[List[Any]]) -> QGridLayout:
    """
    Function returning a grid layout
    :param elements: A list of item list
    :return: The grid layout with the elements
    """
    grid_layout = QGridLayout()
    for row, line in enumerate(elements):
        column = 0
        for element in line:
            column_size = 1
            if isinstance(element, list):
                column_size = element[1]
                grid_layout.addWidget(element[0], row, column, 1, column_size)
            elif element:
                grid_layout.addWidget(element, row, column)
            column += column_size
    return grid_layout


def get_label(label: LabelEnum = None, align: Qt.AlignmentFlag = Qt.AlignLeft, style: Optional[str] = None) -> QLabel:
    """
    Function returning a label
    :param label: The text to print
    :param align: The label alignment
    :param style: the label style
    :return: The label
    """
    label = QLabel(label.value if label else '')
    label.setAlignment(align)
    if style:
        label.setStyleSheet(style)
    return label


class UiFormWindow(QWidget):
    """Class managing the view elements"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, model):
        super().__init__()
        self.setMinimumSize(600, 200)

        self.choice_dialog = ChoiceDialog()
        self.new_or_not_dialog = NewOrNotDialog()

        # Error message label
        self.error_message = get_label(align=Qt.AlignCenter, style="color: red;")

        # Form fields
        self.line_edit_server, self.label_server = UiFormWindow.get_line_edit_with_label(LabelEnum.SERVER, model.server)
        self.line_edit_student_key, self.label_student_key = UiFormWindow.get_line_edit_with_label(
            LabelEnum.STUDENT_KEY, model.student_key)
        self.line_edit_group_key, self.label_group_key = UiFormWindow.get_line_edit_with_label(
            LabelEnum.GROUP_KEY, model.group_key)
        self.line_edit_directory, self.label_directory = UiFormWindow.get_line_edit_with_label(
            LabelEnum.DIRECTORY, model.directory)

        # Directory button
        self.directory_button = QPushButton(LabelEnum.SEARCH.value)

        # Submit button
        self.submit_button = QPushButton(LabelEnum.ACCESS_GROUP.value)

        self.combo_box_prefix_server = QComboBox()
        self.combo_box_prefix_server.addItem("https://")
        self.combo_box_prefix_server.addItem("http://")
        self.combo_box_prefix_server.setCurrentText(model.prefix_server)

        self.setLayout(create_grid_layout([
            [[self.error_message, 4]],
            [self.label_server, self.combo_box_prefix_server, self.line_edit_server],
            [self.label_student_key, [self.line_edit_student_key, 2]],
            [self.label_group_key, [self.line_edit_group_key, 2]],
            [self.label_directory, [self.line_edit_directory, 2], self.directory_button],
            [None, [self.submit_button, 2]],
        ]))

    @staticmethod
    def get_line_edit_with_label(label: LabelEnum, value: str,
                                 align: Qt.AlignmentFlag = Qt.AlignRight | Qt.AlignVCenter,
                                 style: Optional[str] = None) -> Tuple[QLineEdit, QLabel]:
        """
        Function returning a line edit and a label
        :param label: The text to print
        :param value: The input value
        :param align: The label alignment
        :param style: the label style
        :return: The line edit and the label
        """
        line_edit = QLineEdit(value)
        return line_edit, get_label(label, align, style)

    def line_edit_error(self, server: str = None, student_key: str = None,
                        group_key: str = None, directory: str = None) -> None:
        """
        Method changing the input fields label styles
        :param server: The server style
        :param student_key: The student_key style
        :param group_key: The group_key style
        :param directory: The directory style
        """
        self.label_server.setStyleSheet(server)
        self.label_student_key.setStyleSheet(student_key)
        self.label_group_key.setStyleSheet(group_key)
        self.label_directory.setStyleSheet(directory)

    def labels_style_default(self) -> None:
        """
        Method removing the input fields label styles
        """
        self.label_server.setStyleSheet(None)
        self.label_student_key.setStyleSheet(None)
        self.label_group_key.setStyleSheet(None)
        self.label_directory.setStyleSheet(None)


class ChoiceDialog(QDialog):
    """Class managing the choice dialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(LabelEnum.CHOICE.value)
        self.setWindowModality(Qt.ApplicationModal)

        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(500)

        self.btn_valid = QPushButton(LabelEnum.OPEN.value)

        self.setLayout(create_grid_layout([
            [[self.list_widget, 4]],
            [None, [self.btn_valid, 2]]
        ]))

    def get_data(self) -> Optional[Any]:
        """
        Method returning the current data
        :return: The current data
        """
        if self.list_widget.currentItem():
            return self.list_widget.currentItem().data(Qt.UserRole)
        return None

    def init_list(self, config: Any) -> None:
        """
        Method for init the list values
        :param config: All configs save
        """
        self.list_widget.clear()
        number = 0
        for key in config.configs:
            if key != config.DEFAULT:
                number += 1
                config_values = config.configs[key]
                field = f'{number} - {config_values[config.NAME]} - {config_values[config.DIRECTORY]}'
                item = QListWidgetItem(field)
                item.setData(Qt.UserRole, config_values)
                self.list_widget.addItem(item)


class NewOrNotDialog(QDialog):
    """Class managing the choice dialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(LabelEnum.WARNING.value)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(self.minimumSize())

        self.label = get_label(LabelEnum.DIRECTORY_CHANGED, align=Qt.AlignCenter)

        self.btn_restore = QPushButton(LabelEnum.RESTORE.value)
        self.btn_reset = QPushButton(LabelEnum.RESET.value)
        self.btn_cancel = QPushButton(LabelEnum.CANCEL.value)

        self.reset = False
        self.restore = False

        self.setLayout(create_grid_layout([
            [[self.label, 3]],
            [self.btn_restore, self.btn_reset, self.btn_cancel]
        ]))
