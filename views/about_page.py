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
from core import constants

class AboutPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        # Judul
        tk.Label(
            self,
            text=constants.ABOUT,
            font=("Arial", 18, "bold")
        ).pack(anchor="nw", padx=10, pady=(10, 5))

        # Frame teks
        text_frame = tk.Frame(self, bg="white")
        text_frame.pack(fill="both", expand=True, padx=10, pady=(5, 20))

        # Gunakan Label (bukan Text) agar ringan dan stabil
        description = (
            "   Aplikasi Klasifikasi Kualitas Granul merupakan sistem berbasis Machine Learning "
            "yang dirancang untuk mengidentifikasi dan mengklasifikasikan kualitas granul "
            "berdasarkan parameter sudut diam dan waktu pengujian."
            "Aplikasi ini berfungsi untuk membantu proses analisis dalam penentuan kualitas "
            "granul secara otomatis dan akurat, yang sebelumnya dilakukan secara manual."
            "Sistem ini dikembangkan sebagai hasil kolaborasi penelitian antara Program "
            "Magister Magister Teknik Elektro dan Fakultas Farmasi Universitas Ahmad Dahlan (UAD). "
            "Tujuannya adalah untuk mengintegrasikan kecerdasan buatan dalam bidang farmasi, "
            "khususnya dalam pengendalian mutu bahan granul."
            "Dengan menggunakan model pembelajaran mesin, aplikasi mampu mendeteksi dan "
            "mengklasifikasikan kualitas granul menjadi beberapa kategori berdasarkan data "
            "yang diperoleh dari hasil pengukuran sudut diam serta durasi waktu pengujian."
        )

        description_label = tk.Label(
            text_frame,
            text=description,
            font=("Arial", 12),
            justify="left",
            wraplength=700,   
            anchor="nw"
        )
        description_label.pack(anchor="nw", fill="both", expand=True)

        # Copyright
        tk.Label(
            self,
            text="© 2025 Universitas Ahmad Dahlan (UAD)\n"
                 "Magister Teknik Elektro & Fakultas Farmasi",
            font=("Arial", 10, "italic"),
            fg="gray"
        ).pack(anchor="se", padx=10, pady=10)