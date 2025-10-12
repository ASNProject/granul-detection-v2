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
from tkinter import messagebox
from core import utils, config, constants
from views.widgets import form
import os

ASSETS_FOLDER = constants.ASSETS
JSON_FILE = os.path.join(ASSETS_FOLDER, constants.SETTING_FILE)
EXCEL_FILE = os.path.join(ASSETS_FOLDER, constants.DATASET_FILE)

class SettingsPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        # Label judul di kiri atas
        tk.Label(
            self,
            text=constants.SETTING,
            font=("Arial", 18, "bold")
        ).pack(anchor="nw", padx=10, pady=(10, 5))

        self.data = utils.load_json(config.DEFAULT_JSON)

        self.form = form.FormBuilder(self, self.data, fields=config.FORM_FIELDS)

        # Tombol simpan
        btn_save = tk.Button(self, text=constants.SAVE, command=self.save_data, bg="white", fg="black", padx=10, pady=5)
        btn_save.pack(pady=10)

        # ===== Container untuk file + button =====
        self.file_container = tk.Frame(self)
        self.file_container.pack(fill="x", padx=10, pady=10)

        self.filename_label = tk.Label(self.file_container, text=f"{constants.DATASETS}: {os.path.basename(EXCEL_FILE)}", anchor="w")
        self.filename_label.pack(side="left")

        btn_frame = tk.Frame(self.file_container)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text=f"{constants.DOWNLOAD} {constants.DATASETS}", bg="white", fg="black",
                  padx=10, pady=5, command=self.download_excel).pack(side="left", padx=5)

        tk.Button(btn_frame, text=f"{constants.UPLOAD} {constants.DATASETS}", bg="white", fg="black",
                  padx=10, pady=5, command=self.upload_excel).pack(side="left", padx=5)

    def save_data(self):
        update_data = self.form.get_form_data()
        # Konfirmasi data
        confirm = messagebox.askyesno("Konfirmasi", "Apakah anda yakin ingin menyimpan perubahan?")

        if confirm:
            utils.save_json(update_data)
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")

    def download_excel(self):
        utils.download_file(EXCEL_FILE, default_name=constants.DATASET_FILE)

    def upload_excel(self):
        uploaded_path = utils.upload_file(ASSETS_FOLDER, rename_as=constants.DATASET_FILE)
        if uploaded_path:
            self.filename_label.config(text=f"{constants.DATASETS}: {os.path.basename(uploaded_path)}")