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

import cv2
import numpy as np

class ShapeDetector:
    @staticmethod
    def detect_largest_triangle_overlay(frame, lower_hsv, upper_hsv):
        """Deteksi segitiga terbesar berdasarkan warna (overlay di frame asli)"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        largest_triangle = None

        for contour in contours:
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 3 and cv2.contourArea(contour) > 500:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    largest_triangle = approx

        result = frame.copy()

        if largest_triangle is not None:
            x, y, w, h = cv2.boundingRect(largest_triangle)
            cv2.drawContours(result, [largest_triangle], 0, (0, 255, 0), 2)
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if w != 0:
                angle_radians = np.arctan(h / w)
                angle_degrees = np.degrees(angle_radians)
            else:
                angle_degrees = 0

            cv2.putText(result, f"Tinggi: {h}px", (x, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(result, f"Panjang: {w}px", (x, y - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(result, f"Sudut: {angle_degrees:.2f}°", (x, y - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(result, "Granul", (x, y - 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return result
