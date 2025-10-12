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
from core import config, constants
import shutil
from tkinter import filedialog, messagebox

# Fungsi helper umum
def format_text(text: str) -> str:
    """Format text agar huruf pertama kapital"""
    return text.strip().capitalize()

# Load JSON File
def load_json(default_data):
    try:
        with open(config.JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        save_json(default_data)
        return default_data

# Save JSON File
def save_json(data):
    with open(config.JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Download Template Datasets
def download_file(src_path, default_name=None):
    """Download file dari src_path ke lokasi yang dipilih user"""
    if not os.path.exists(src_path):
        messagebox.showerror("Error", f"File tidak ditemukan: {src_path}")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=os.path.splitext(src_path)[1],
        filetypes=[(constants.DATASETS, constants.EXCEL_FORMAT)],
        initialfile=default_name or os.path.basename(src_path),
        title="Simpan file sebagai..."
    )
    if save_path:
        shutil.copy(src_path, save_path)
        messagebox.showinfo("Sukses", f"File berhasil di-download ke:\n{save_path}")

# Upload Tamplate Datasets
def upload_file(dest_folder, rename_as=None):
    """Upload file ke folder tujuan, bisa ganti nama"""
    file_path = filedialog.askopenfilename(
        filetypes=[(constants.DATASETS, constants.EXCEL_FORMAT)],
        title="Pilih file Excel untuk di-upload"
    )
    if file_path:
        filename = rename_as if rename_as else os.path.basename(file_path)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy(file_path, dest_path)
        messagebox.showinfo("Sukses", f"File berhasil di-upload:\n{dest_path}")
        return dest_path
    return None