"""Module managing the web window"""
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

from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView


class UiWebWindow(QWebEngineView):
    """Class managing the view elements"""
    def __init__(self, url: str) -> None:
        super().__init__()
        self.load_url(url)
        self.setZoomFactor(0.80)

    def do_refresh(self) -> None:
        """Method using a JavaScript function in the web view"""
        try:
            self.page().runJavaScript("makeRequest()")
        except ReferenceError:
            pass

    def load_url(self, url: str) -> None:
        """Method loading the web view url"""
        self.load(QUrl(url))
