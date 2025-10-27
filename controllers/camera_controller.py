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

import platform
import cv2
from PIL import Image, ImageTk
from core import constants
import os
import json
import numpy as np
from controllers.shape_detector_controller import ShapeDetector

ASSETS_FOLDER = constants.ASSETS
JSON_FILE = os.path.join(ASSETS_FOLDER, constants.SETTING_FILE)

class CameraController:
    def __init__(self, target_label, target_frame):
        """
        target_label: tk.Label tempat menampilkan kamera
        target_frame: tk.Frame untuk mendapatkan ukuran
        """
        self.target_label = target_label
        self.target_frame = target_frame
        self.cap = None
        self.running = False
        self.apply_overlay = True  
    
    def start_camera(self):
        """Mulai loop kamera setelah GUI siap"""
        if self.cap is None or not self.cap.isOpened():
            system = platform.system()

            # Pilih backend kamera sesuai OS
            if system == "Windows":
                self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            elif system == "Darwin":  # macOS
                self.cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
            else:  # Linux
                self.cap = cv2.VideoCapture(1)

        if not self.cap.isOpened():
            self.target_label.config(text="Kamera tidak ditemukan", fg="white", bg="black")
            return
        
        self.running = True
        self.target_label.after(200, self.update_camera_frame)
    
    def update_camera_frame(self):
        """Ambil frame dari kamera"""
        if not self.running or not self.cap or not self.cap.isOpened():
            return

        # Ambil frame dari kamera
        ret, frame = self.cap.read()
        config = self.load_json_config(JSON_FILE)
        if not ret:
            self.target_label.after(100, self.update_camera_frame)
            return
        
        if config.get("APPLY_OVERLAY", True):
            if self.apply_overlay:
                if config:
                    lower_hsv = np.array([
                        config.get("H_MIN", 0),
                        config.get("S_MIN", 0),
                        config.get("V_MIN", 0)
                    ])
                    upper_hsv = np.array([
                        config.get("H_MAX", 179),
                        config.get("S_MAX", 255),
                        config.get("V_MAX", 255)
                    ])
                    frame = ShapeDetector.detect_largest_triangle_overlay(frame, lower_hsv, upper_hsv)

        # Konversi warna BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Dapatkan ukuran frame target
        self.target_frame.update_idletasks()
        width = self.target_frame.winfo_width() 
        height = self.target_frame.winfo_height()

        # Jika ukuran belum siap, tunggu dulu
        if width < 200 or height < 200:
            self.target_label.after(200, self.update_camera_frame)
            return

        # Resize frame sesuai area
        frame = cv2.resize(frame, (width, height))

        # Konversi ke format yang bisa ditampilkan Tkinter
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        self.target_label.imgtk = img
        self.target_label.config(image=img, text="")

        # Loop update
        if self.running:
            self.target_label.after(30, self.update_camera_frame)

    def stop_camera(self):
        """Hentikan kamera dengan aman"""
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.target_label.config(image="")

    @staticmethod
    def load_json_config(path):
        """Baca file JSON untuk konfigurasi HSV"""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Gagal load konfigurasi dari {path}: {e}")
            return {}

    def update_hsv(self, hsv_values):
        """Method dummy agar tidak error ketika dipanggil dari SettingsPage.
        Tidak menyimpan apa pun karena CameraController hanya membaca konfigurasi dari JSON."""
        pass