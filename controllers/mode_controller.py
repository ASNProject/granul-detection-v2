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

import json
import os
from core import constants

ASSETS_FOLDER = constants.ASSETS
JSON_FILE = os.path.join(ASSETS_FOLDER, constants.SETTING_FILE)

class ModeController:
    def __init__(self):
        self.data = self._load_json()

    def _load_json(self):
        """Load JSON settings"""
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        else:
            # Default jika belum ada
            return {
                "PORT": "COM7",
                "BAUDRATE": "9600",
                "H_MIN": 0,
                "H_MAX": 179,
                "S_MIN": 101,
                "S_MAX": 255,
                "V_MIN": 188,
                "V_MAX": 255,
                "MODE": "mode1"
            }

    def get_mode(self):
        """Ambil mode saat ini dari JSON"""
        return self.data.get("MODE", "mode1")

    def save_mode(self, mode):
        """Simpan mode ke JSON"""
        self.data["MODE"] = mode
        with open(JSON_FILE, "w") as f:
            json.dump(self.data, f, indent=4)
