# FastGrading
A step-by-step, from-scratch Optical Mark Recognition (OMR) project in Python using OpenCV — works on scanned images and realtime webcam scans.



## Introduction  
**FatGrading** is a step-by-step Optical Mark Recognition (OMR) system built from scratch using **Python + OpenCV**.  
It automatically detects, extracts, and grades MCQ answer sheets from:

- 🎥 **Realtime webcam feed**  

This project explains each major step of the pipeline — from preprocessing to contour detection to bubble recognition — making it ideal for learners and real-world automation use cases.

---

#  Features  
- **Image-based OMR** – Upload any scanned/photographed MCQ sheet.  
- **Realtime Webcam Grading** – Automatically detect and score answers live.  
- **Bubble Detection** – Identifies filled vs. unfilled options reliably.  
- **Answer Comparison** – Compares detected answers with the answer key.  
- **Score Calculation** – Generates instant results.  
- **From Scratch Implementation** – Every step explained clearly for beginners.  
- **Result Visualization** – Shows detected contours, bubbles, and grading overlays.

---

# Tech Stack  
- **Python 3.x**  
- **OpenCV** – image processing, contour detection, thresholding  
- **NumPy** – numerical operations  
- **Imutils** – helper functions  
- **Webcam Module (OpenCV VideoCapture)** – real-time OMR  

---
# Results
-**I saved the output from a garde sheet i hade then integrated the webcam feature to scan sheets in realtime
![Image-based OMR Result](output.jpg)
![Webcam OMR Result](webcam.jpg)



# 📁 Project Structure  

Add template designer for custom sheets
