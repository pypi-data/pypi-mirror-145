"""module allowing the creation of a pypi package"""
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
import os

from setuptools import setup
from ubiquity_student.ubiquity import __version__

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'), "r", encoding="utf8") as readme:
    long_description = readme.read()

setup(name='ubiquity-student',
      version=__version__,
      packages=[
            'ubiquity_student',
            'ubiquity_student.ubiquity',
            'ubiquity_student.ubiquity.controllers',
            'ubiquity_student.ubiquity.views',
            'ubiquity_student.ubiquity.views.gui',
            'ubiquity_student.ubiquity.views.cui',
      ],
      classifiers=[
          'Topic :: Education',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Intended Audience :: Education',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Natural Language :: French',

      ],
      url='https://gitlab.insa-rouen.fr/cip/ubiquity',
      download_url='https://gitlab.insa-rouen.fr/cip/ubiquity/-/tags',
      project_urls={
          'Documentation': 'https://gitlab.insa-rouen.fr/cip/ubiquity/-/wikis/home',
          'Bug Tracker': 'https://gitlab.insa-rouen.fr/cip/ubiquity/-/issues',
      },
      description='Ubiquity permet le suivi de TP de développement informatique',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
            'PySide2==5.15.2.1',
            'requests==2.27.1'
      ],
      package_data={
          'ubiquity_student': [
              'ubiquity/images/ubiquity_icon.png',
              'ubiquity/locale/fr/LC_MESSAGES/ubiquity-student.mo'
          ]
      },
      entry_points={
          "console_scripts": [
              'ubiquity-student = ubiquity_student.ubiquity.ubiquity_student:main'
          ]
      },
      python_requires=">=3.6, <3.11",
      )
