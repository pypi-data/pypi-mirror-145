#!/usr/bin/python3
"""Module managing the application"""
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
import argparse
import os.path
import signal
import sys
from typing import Optional, List

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from .controllers.config_file import Config
from .controllers.main_controller import MainController
from .model import Model
from .views.gui.main_view import MainView as GuiMainView
from .views.cui.main_view import MainView as CuiMainView

from . import __version__


def _get_kwargs_value(kwargs, key, default):
    try:
        return kwargs[key]
    except KeyError:
        return default


class App(QApplication):
    """Class managing the application"""

    VERSION = __version__
    LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/ubiquity_icon.png")

    def __init__(self, sys_argv, config, values: List[Optional[str]], **kwargs):
        super().__init__(sys_argv)
        self.model = Model(values)
        self.main_controller = MainController(config, self.model)

        has_form = _get_kwargs_value(kwargs, 'has_form', True)
        gui = _get_kwargs_value(kwargs, 'gui', True)
        has_color = _get_kwargs_value(kwargs, 'has_color', True)

        if gui:
            self._gui_view(has_form, has_color)
        else:
            self._cui_view(has_form, has_color)

    def _gui_view(self, has_form: bool, has_color: bool) -> None:
        self.main_view = GuiMainView(self.model, self.main_controller, has_form, has_color)
        self.logo = QIcon(App.LOGO)
        self.setWindowIcon(self.logo)
        self.show_view()

    def _cui_view(self, has_form: bool, has_color: bool) -> None:
        self.main_view = CuiMainView(self.model, self.main_controller, has_form, has_color)

    def show_view(self) -> None:
        """Method showing the main view"""
        self.main_view.show()

    def exec(self) -> int:
        """
        Method running the application
        :return: The return code
        """
        return self.exec_()


def _check_int(value):
    try:
        int_value = int(value)
    except ValueError as no_int:
        raise argparse.ArgumentTypeError(f"invalid int value: {repr(value)}") from no_int
    if int_value <= 0:
        raise argparse.ArgumentTypeError(f"invalid positive int value: {repr(value)}")
    return int_value


def _get_arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False, usage='%(prog)s [options]',
                                     description='Ubiquity-student allows the follow-up of computer science courses')

    parser.add_argument("-V", "--version", action="store_true", dest='version',
                        help="print the Ubiquity-student version number and exit")

    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    mutually_exclusive_group.add_argument("-l", "--list", action="store_true", dest='list',
                                          help="print the configuration list and exit")
    mutually_exclusive_group.add_argument("--load", type=_check_int, dest='id',
                                          help="load and run a configuration")

    parser.add_argument("--no-gui", action="store_true", dest='is_console', default=False,
                        help="do not display the graphic user interface")
    parser.add_argument("--no-color", action="store_true", dest='has_not_color', default=False,
                        help="do not display colors on the console")

    group = parser.add_argument_group('input field', 'If all values are defined, no form will be proposed')

    group.add_argument("-s", "--server", type=str, dest='server',
                       help="define a value for the server field")

    group.add_argument("-u", "--student-key", type=str, dest='student_key',
                       help="define a value for the student key field")

    group.add_argument("-g", "--group-key", type=str, dest='group_key',
                       help="define a value for the group key field")

    group.add_argument("-d", "--directory", type=str, dest='directory',
                       help="define a value for the directory field")
    return parser


def _get_args_values(args: argparse.Namespace):
    return [args.server, args.student_key, args.group_key, args.directory]


def _display_version():
    print('Ubiquity-student ' + __version__)
    sys.exit(0)


def _get_list_config(config: Config, values):
    configs = config.configs.copy()
    configs.pop('default')
    servers = {}
    for number, key in enumerate(configs, 1):
        config_values = configs[key]
        config_server = config_values[config.PREFIX_SERVER] + config_values[config.SERVER]
        is_server_in_list = not values[0] or values[0] == config_server
        is_student_key_in_list = not values[1] or values[1] == config_values[config.STUDENT_KEY]
        is_group_key_in_list = not values[2] or values[2] == config_values[config.GROUP_KEY]
        is_directory_in_list = not values[3] or values[3] == config_values[config.DIRECTORY]
        if is_server_in_list and is_student_key_in_list and is_group_key_in_list and is_directory_in_list:
            if config_server not in servers:
                servers[config_server] = {}
            if config_values[config.STUDENT_KEY] not in servers[config_server]:
                servers[config_server][config_values[config.STUDENT_KEY]] = {}
            servers[config_server][config_values[config.STUDENT_KEY]][config_values[config.GROUP_KEY]] = {
                'number': str(number),
                'name': config_values[config.NAME],
                'directory': config_values[config.DIRECTORY]
            }

    return servers


def _display_list_config(servers: dict):
    if len(servers) == 0:
        print('No practical work')
        sys.exit(0)
    for server in servers:
        print('Server: ' + server)
        for student_key in servers[server]:
            print(' ' * 3 + 'Student key: ' + student_key)
            for group_key in servers[server][student_key]:
                print(' ' * 6 + '|' + '-' * 3 + '(' + servers[server][student_key][group_key]['number'] + ') ' +
                      'Group key: ' + group_key)
                print(' ' * 6 + '|' + ' ' * 3 + 'Name: ' + servers[server][student_key][group_key]['name'])
                print(' ' * 6 + '|' + ' ' * 3 + 'Directory: ' + servers[server][student_key][group_key]['directory'])
        print()
    sys.exit(0)


def _get_id_values(config: Config, config_id: int):
    configs = config.configs.copy()
    configs.pop('default')
    key_list = list(configs)
    if len(key_list) > config_id:
        config_values = configs[list(configs)[config_id]]
        config_server = config_values[config.PREFIX_SERVER] + config_values[config.SERVER]
        return [config_server,
                config_values[config.STUDENT_KEY],
                config_values[config.GROUP_KEY],
                config_values[config.DIRECTORY]]
    print(f'No practical work with the id {config_id + 1}')
    sys.exit(0)


def main() -> None:
    """Main function"""
    arg_parser = _get_arg_parser()
    args = arg_parser.parse_args()
    if args.version:
        _display_version()

    config = Config()
    values = _get_args_values(args)

    if args.list:
        servers = _get_list_config(config, values)
        _display_list_config(servers)
    if args.id:
        if args.server:
            arg_parser.error('argument -s/--server: not allowed with argument --load')
        if args.student_key:
            arg_parser.error('argument -u/--student_key: not allowed with argument --load')
        if args.group_key:
            arg_parser.error('argument -g/--group_key: not allowed with argument --load')
        if args.directory:
            arg_parser.error('argument -d/--directory: not allowed with argument --load')
        values = _get_id_values(config, args.id - 1)

    signal.signal(signal.SIGINT, signal.SIG_DFL)  # SIGINT => Ctrl + C
    app = App(sys.argv, config, values, has_form=None in values,
              gui=not args.is_console, has_color=not args.has_not_color)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
