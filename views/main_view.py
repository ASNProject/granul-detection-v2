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
from tkinter import ttk
from core import config
from controllers.navigation_controller import NavigationController
from controllers.footer_controller import FooterController
from views.home_page import HomePage
from views.settings_page import SettingsPage
from views.about_page import AboutPage
from core import constants

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        # ====== CONFIGURATION ======
        self.title(config.APP_TITLE)
        # TODO: Uncomment if you want to use config
        self.geometry(config.WINDOW_SIZE)
        self.nav_controller = NavigationController(self)

        # ======= NAVBAR =======
        navbar = tk.Frame(self, height=50)
        navbar.pack(fill="x")

        title_label = tk.Label(navbar, text=config.APP_NAME_LOGO, font=("Arial", 24, "bold"), fg="orange")
        title_label.pack(side="left", padx=15)

        # Buttons
        tk.Button(navbar, text=constants.ABOUT, bg="white", command=self.nav_controller.go_about).pack(side="right", padx=5)
        tk.Button(navbar, text=constants.SETTING, bg="white", command=self.nav_controller.go_setting).pack(side="right", padx=5)
        tk.Button(navbar, text=constants.HOME, bg="white", command=self.nav_controller.go_home).pack(side="right", padx=5)


        # ======= MAIN CONTENT ======
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Inisialisasi halaman
        self.pages = {
            constants.HOME_PAGES: HomePage(self.content_frame, self),
            constants.SETTING_PAGES: SettingsPage(self.content_frame, self),
            constants.ABOUT_PAGES: AboutPage(self.content_frame, self),
        }

        # Tampilkan halaman beranda pertama kali
        self.show_page(constants.HOME_PAGES)  

        # ======= FOOTER =======
        self.update_idletasks()  

        self.footer_canvas = tk.Canvas(self, height=25, bg="black", highlightthickness=0)
        self.footer_canvas.pack(side="bottom", fill="x")

        self.footer_text = config.FOOTER_TEXT
        self.footer_item = self.footer_canvas.create_text(
            self.footer_canvas.winfo_reqwidth(),
            12,
            text=self.footer_text,
            font=("Arial", 10),
            anchor="w",
            fill="white"
        )

        # Jalankan animasi footer dari controller
        self.footer_controller = FooterController(self.footer_canvas, self.footer_item, self)
        self.after(100, self.footer_controller.run_footer_text)

    # ====== FUNCTION ======
    def on_close(self):
        """Pastikan kamera berhenti sebelum exit"""
        self.camera_controller.stop_camera()
        self.destroy()

    def show_page(self, page_name: str):
        """Menampilkan halaman berdasarkan nama"""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)
    
        