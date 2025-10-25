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
from controllers.camera_controller import CameraController
from controllers.hsv_filter_controller import HSVFilterController
from controllers.shape_detector_controller import ShapeDetector
import cv2
from PIL import Image, ImageTk
import os
import numpy as np

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

        # Main Content
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left: Form
        self.data = utils.load_json(config.DEFAULT_JSON)
        self.form = form.FormBuilder(
            content_frame, 
            self.data, 
            fields=config.FORM_FIELDS, 
            editable_fields=config.EDITABLE_FIELDS
        )
        self.form.form_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right: Camera Preview
        self._init_camera_section(content_frame)

        # Tombol simpan
        btn_save = tk.Button(
            self, 
            text=constants.SAVE, 
            command=self.save_data, 
            bg="white", 
            fg="black", 
            padx=10, 
            pady=5
        )
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
            # Simpan juga HSV terbaru
            hsv_values = {
                constants.H_MIN: self.h_min.get(),
                constants.H_MAX: self.h_max.get(),
                constants.S_MIN: self.s_min.get(),
                constants.S_MAX: self.s_max.get(),
                constants.V_MIN: self.v_min.get(),
                constants.V_MAX: self.v_max.get(),
            }
            self.hsv_controller.update_hsv(hsv_values, auto_save=True)
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")

    def download_excel(self):
        utils.download_file(EXCEL_FILE, default_name=constants.DATASET_FILE)

    def upload_excel(self):
        uploaded_path = utils.upload_file(ASSETS_FOLDER, rename_as=constants.DATASET_FILE)
        if uploaded_path:
            self.filename_label.config(text=f"{constants.DATASETS}: {os.path.basename(uploaded_path)}")

    def _init_camera_section(self, parent):
        camera_container = tk.Frame(parent)
        camera_container.pack(side="right", fill="both", padx=10, pady=10)

        # Camera preview
        self.camera_frame = tk.Frame(camera_container, width=320, height=180, bg="black")
        self.camera_frame.pack(side="right", fill="both", padx=(10, 0))
        self.camera_frame.pack_propagate(False)

        self.camera_label = tk.Label(self.camera_frame, bg="black", text="memuat kamera...")
        self.camera_label.pack(fill="both", expand=True)

        # Controller
        self.camera_controller = CameraController(self.camera_label, self.camera_frame)
        self.hsv_controller = HSVFilterController()

        # HSV Panel (setelah hsv_controller dibuat)
        self._init_hsv_panel(camera_container)

        self.after(500, self.camera_controller.start_camera)
        self.after(500, self._update_filtered_preview)


    def _init_hsv_panel(self, parent):
        hsv_frame = tk.LabelFrame(parent, text="Kalibrasi HSV", padx=10, pady=10)
        hsv_frame.pack(side="left", fill="y", padx=(0, 10))

        hsv = self.hsv_controller.hsv_values  # ambil dari JSON

        self.h_min = tk.Scale(hsv_frame, from_=0, to=179, orient=constants.HORIZONTAL, label=constants.HUE_MIN, command=self.update_hsv)
        self.h_max = tk.Scale(hsv_frame, from_=0, to=179, orient=constants.HORIZONTAL, label=constants.HUE_MAX, command=self.update_hsv)
        self.s_min = tk.Scale(hsv_frame, from_=0, to=255, orient=constants.HORIZONTAL, label=constants.SATURATION_MIN, command=self.update_hsv)
        self.s_max = tk.Scale(hsv_frame, from_=0, to=255, orient=constants.HORIZONTAL, label=constants.SATURATION_MAX, command=self.update_hsv)
        self.v_min = tk.Scale(hsv_frame, from_=0, to=255, orient=constants.HORIZONTAL, label=constants.VALUE_MIN, command=self.update_hsv)
        self.v_max = tk.Scale(hsv_frame, from_=0, to=255, orient=constants.HORIZONTAL, label=constants.VALUE_MAX, command=self.update_hsv)

        # Set nilai awal dari JSON
        self.h_min.set(hsv[constants.H_MIN])
        self.h_max.set(hsv[constants.H_MAX])
        self.s_min.set(hsv[constants.S_MIN])
        self.s_max.set(hsv[constants.S_MAX])
        self.v_min.set(hsv[constants.V_MIN])
        self.v_max.set(hsv[constants.V_MAX])

        # Layout grid
        self.h_min.grid(row=0, column=0, sticky="ew", pady=2, padx=5)
        self.h_max.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        self.s_min.grid(row=1, column=0, sticky="ew", pady=2, padx=5)
        self.s_max.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        self.v_min.grid(row=2, column=0, sticky="ew", pady=2, padx=5)
        self.v_max.grid(row=2, column=1, sticky="ew", pady=2, padx=5)


    def update_hsv(self, *args):
        """Update HSV values dengan debounce agar tidak flicker"""
        if hasattr(self, "_hsv_update_job"):
            self.after_cancel(self._hsv_update_job)

        # tunggu 150ms setelah user berhenti geser sebelum apply filter
        self._hsv_update_job = self.after(150, self._apply_hsv_values)

    def _apply_hsv_values(self):
        hsv_values = {
            constants.H_MIN: self.h_min.get(),
            constants.H_MAX: self.h_max.get(),
            constants.S_MIN: self.s_min.get(),
            constants.S_MAX: self.s_max.get(),
            constants.V_MIN: self.v_min.get(),
            constants.V_MAX: self.v_max.get(),
        }
        if hasattr(self, "camera_controller"):
            self.camera_controller.update_hsv(hsv_values)


    def _update_filtered_preview(self):
        """Tampilkan kamera normal dengan overlay segitiga hasil deteksi (tanpa mask hitam)"""
        if hasattr(self.camera_controller, "cap") and self.camera_controller.cap and self.camera_controller.cap.isOpened():
            ret, frame = self.camera_controller.cap.read()
            if ret:
                # Ambil batas HSV dari slider
                lower_hsv = np.array([self.h_min.get(), self.s_min.get(), self.v_min.get()])
                upper_hsv = np.array([self.h_max.get(), self.s_max.get(), self.v_max.get()])

                # Deteksi segitiga pada frame, tapi kembalikan hasil overlay (bukan mask)
                overlay_frame = ShapeDetector.detect_largest_triangle_overlay(frame, lower_hsv, upper_hsv)

                # Resize ke ukuran frame kamera
                width = self.camera_frame.winfo_width()
                height = self.camera_frame.winfo_height()
                overlay_frame = cv2.resize(overlay_frame, (width, height))

                # Konversi ke RGB untuk Tkinter
                rgb_img = cv2.cvtColor(overlay_frame, cv2.COLOR_BGR2RGB)
                imgtk = ImageTk.PhotoImage(image=Image.fromarray(rgb_img))
                self.camera_label.imgtk = imgtk
                self.camera_label.config(image=imgtk)

        # Perbarui tiap 80ms
        self.after(80, self._update_filtered_preview)



