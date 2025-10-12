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

class DetectionController:
    """Controller untuk deteksi kualitas granul"""
    def __init__(self, view):
        """
        view: instance dari MainView agar bisa mengakses komponen UI
        """
        self.view = view

    def on_mulai_click(self):
        """Contoh simulasi deteksi — update nilai di UI"""
        # Sudut
        self.view.sudut_entry.config(state="normal")
        self.view.sudut_entry.delete(0, "end")
        self.view.sudut_entry.insert(0, "45°")
        self.view.sudut_entry.config(state="readonly")

        # Waktu
        self.view.waktu_entry.config(state="normal")
        self.view.waktu_entry.delete(0, "end")
        self.view.waktu_entry.insert(0, "12:30:55")
        self.view.waktu_entry.config(state="readonly")

        # Kualitas granul
        self.view.kualitas_label.config(text="Baik", fg="green")
