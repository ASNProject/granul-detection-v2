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

import cv2
import os
import json
from core import constants

ASSETS_FOLDER = constants.ASSETS
JSON_FILE = os.path.join(ASSETS_FOLDER, constants.SETTING_FILE)


class HSVFilterController:
    def __init__(self):
        self.hsv_values = {
            constants.H_MIN: 0,
            constants.H_MAX: 179,
            constants.S_MIN: 0,
            constants.S_MAX: 255,
            constants.V_MIN: 0,
            constants.V_MAX: 255,
        }
        self.load_from_json()

    def load_from_json(self):
        """Ambil nilai HSV dari JSON"""
        if not os.path.exists(JSON_FILE):
            return
        try:
            with open(JSON_FILE, "r") as f:
                data = json.load(f)
            self.hsv_values = {
                constants.H_MIN: data.get("H_MIN", 0),
                constants.H_MAX: data.get("H_MAX", 179),
                constants.S_MIN: data.get("S_MIN", 0),
                constants.S_MAX: data.get("S_MAX", 255),
                constants.V_MIN: data.get("V_MIN", 0),
                constants.V_MAX: data.get("V_MAX", 255),
            }
        except Exception as e:
            print(f"[WARN] Gagal load HSV dari JSON: {e}")

    def save_to_json(self):
        """Update nilai HSV ke file JSON"""
        try:
            with open(JSON_FILE, "r") as f:
                data = json.load(f)

            data.update({
                "H_MIN": self.hsv_values[constants.H_MIN],
                "H_MAX": self.hsv_values[constants.H_MAX],
                "S_MIN": self.hsv_values[constants.S_MIN],
                "S_MAX": self.hsv_values[constants.S_MAX],
                "V_MIN": self.hsv_values[constants.V_MIN],
                "V_MAX": self.hsv_values[constants.V_MAX],
            })

            with open(JSON_FILE, "w") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f"[ERROR] Gagal menyimpan HSV ke JSON: {e}")

    def update_hsv(self, hsv_values, auto_save=False):
        """Perbarui nilai HSV"""
        self.hsv_values.update(hsv_values)
        if auto_save:
            self.save_to_json()

    def apply_filter(self, frame):
        if frame is None:
            return None
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = (
            self.hsv_values[constants.H_MIN],
            self.hsv_values[constants.S_MIN],
            self.hsv_values[constants.V_MIN],
        )
        upper = (
            self.hsv_values[constants.H_MAX],
            self.hsv_values[constants.S_MAX],
            self.hsv_values[constants.V_MAX],
        )
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        return result
