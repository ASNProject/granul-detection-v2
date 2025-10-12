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

class FooterController:
    """Controller untuk mengatur teks berjalan di footer"""

    def __init__(self, canvas, footer_item, view):
        """
        canvas: tk.Canvas tempat teks berjalan
        footer_item: ID teks yang dibuat dengan create_text()
        view: instance MainView untuk akses ke lebar window
        """
        self.canvas = canvas
        self.footer_item = footer_item
        self.view = view

    def run_footer_text(self):
        """Animasi teks berjalan horizontal"""
        self.canvas.move(self.footer_item, -2, 0)
        x1, y1, x2, y2 = self.canvas.bbox(self.footer_item)
        if x2 < 0:
            # Jika teks keluar layar kiri → reset ke kanan
            self.canvas.move(self.footer_item, self.view.winfo_width() - x1, 0)
        self.view.after(30, self.run_footer_text)