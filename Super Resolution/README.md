# Super Resolution Image Enhancement System  
AI-Powered Image Upscaling using Real-ESRGAN

## Overview
This project is a web-based application that enhances low-resolution or blurry images using **Real-ESRGAN**, a state-of-the-art deep learning model for super-resolution.  
The system allows users to upload an image, process it, and view the **before vs after** results.

##  Features
- 4× Image Super Resolution
- Real-ESRGAN deep learning model
- Automatic enhancement of textures, edges, and colors
- Web-based interface (Flask / Streamlit)
- Side-by-side comparison viewer
- Supports JPG/PNG images

## Technology Used
- **Python**
- **Real-ESRGAN**
- **PyTorch**
- **OpenCV**
- **Flask or Streamlit**
- **HTML/CSS (Frontend UI)**

project/
│── models/ # Real-ESRGAN pre-trained models
│── static/ # CSS, images, UI assets
│── templates/ # Web interface HTML files
│── uploads/ # User uploaded images
│── outputs/ # Enhanced images
│── app.py # Main Flask/Streamlit application
│── requirements.txt # Dependencies
│── README.md # Project documentation

```bash
git clone https://github.com/yourname/super-resolution

pip install -r requirements.txt

3. Download Real-ESRGAN model

Download the official Real-ESRGAN model and place it inside the models/ folder.

4. Run the application
python app.py