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
from controllers.camera_controller import CameraController
from controllers.detection_controller import DetectionController
from core import constants

class HomePage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.root = root

        # ====== MAIN CONTENT ======
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        main_frame.columnconfigure(0, weight=8)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # Frame kiri (kamera)
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")

        self.camera_label = tk.Label(left_frame, bg="black", width=100, height=100)
        self.camera_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.camera_controller = CameraController(self.camera_label, left_frame)
        self.after(1000, self.camera_controller.start_camera)
        self.protocol = getattr(self.root, "on_close", lambda: None)

        # Frame kanan
        right_frame = tk.Frame(main_frame, pady=10, padx=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Konten kanan
        tk.Label(right_frame, text=constants.DEGREE, font=("Arial", 12)).pack(anchor="w")
        self.sudut_entry = tk.Entry(right_frame, font=("Arial", 12), state="readonly")
        self.sudut_entry.pack(fill="x", pady=(0, 10))

        tk.Label(right_frame, text=constants.TIME, font=("Arial", 12)).pack(anchor="w")
        self.waktu_entry = tk.Entry(right_frame, font=("Arial", 12), state="readonly")
        self.waktu_entry.pack(fill="x", pady=(0, 10))

        tk.Label(right_frame, text=constants.GRANUL_QUALITY, font=("Arial", 12)).pack(anchor="w")
        self.kualitas_label = tk.Label(right_frame, text=constants.NO_DETECTION, font=("Arial", 14, "bold"), fg="darkblue")
        self.kualitas_label.pack(anchor="center", pady=(5, 20))

        right_frame.pack_propagate(False)
        spacer = tk.Frame(right_frame)
        spacer.pack(expand=True, fill="both")

        self.det_controller = DetectionController(self)
        mulai_btn = tk.Button(right_frame, text=constants.START, font=("Arial", 14, "bold"),
                              padx=10, pady=5, fg="black", bg="white",
                              command=self.det_controller.on_mulai_click)
        mulai_btn.pack(side="bottom", fill="x", pady=(10, 0))
