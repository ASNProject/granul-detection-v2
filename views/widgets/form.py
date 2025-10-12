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

import tkinter as tk
from .create_rounded_entry import create_rounded_entry

class FormBuilder:
    def __init__(self, parent, data, fields=None):
        """
        parent : parent widget
        data : dictionary berisi data JSON
        fields : list urutan field yang ingin ditampilkan
        """
        self.parent = parent
        self.data = data
        self.fields = fields or list(data.keys())
        self.entries = {}
        self.build_form()

    def build_form(self):
        self.form_frame = tk.Frame(self.parent)
        self.form_frame.pack(padx=20, pady=1, fill="both", expand=True)

        for i, key in enumerate(self.fields):
            value = self.data.get(key, "")
            lbl = tk.Label(self.form_frame, text=key.capitalize(), anchor="w", width=10)
            lbl.grid(row=i, column=0, sticky="w")

            entry_frame, entry = create_rounded_entry(self.form_frame, width=15)
            entry_frame.grid(row=i, column=1, sticky="ew")

            entry.insert(0, str(value))
            self.entries[key] = entry
        
    def get_form_data(self):
        for key, entry in self.entries.items():
            self.data[key] = entry.get()
        return self.data