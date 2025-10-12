# Copyright 2025 ariefsetyonugroho
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from core import constants

class NavigationController:
    """Controller untuk navigasi antar halaman"""
    def __init__(self, main_view):
        self.main_view = main_view

    def go_home(self):
        self.main_view.show_page(constants.HOME_PAGES)

    def go_setting(self):
        self.main_view.show_page(constants.SETTING_PAGES)

    def go_about(self):
        self.main_view.show_page(constants.ABOUT_PAGES)
