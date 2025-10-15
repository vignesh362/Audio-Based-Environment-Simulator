Audio-Based Environment Simulator
Helping the Blind Safely Recognize and Navigate Surroundings Using Real-Time Audio Cues

Overview
Navigating daily life and identifying surroundings is a significant challenge for blind people, often resulting in injuries. This solution provides a real-time audio-based environment simulation. Nearby objects are identified via computer vision and relayed through synthesized speech, equipping users with better context for safe navigation and independent living.​

Features
Object Detection: Uses deep learning (Mask R-CNN and Caffe SSD) models to identify common objects in the environment.​

Real-Time Audio Alerts: Detected objects and their positions (left, front, right) are read out via text-to-speech (using espeak).​

Camera Integration: Captures live video and analyzes each frame for immediate feedback.

Modular Architecture: Components for detection, client-server communication, and audio output are decoupled.

Multi-Model Support: Supports both Mask R-CNN for robust detection and Caffe-based SSD for lightweight deployment.

Repository Structure
text
.
├── LMNTECH_ABES.pptx           # Presentation slides about the project[2]
├── README.md                   # Project description and credits
├── ada.py                      # Main detection module using Mask R-CNN[4]
├── client.py                   # Socket server handling audio output[5]
├── contributers picture.jpeg   # Team photo[6]
├── detection.py                # Alternative detection module using Caffe SSD[7]
Requirements
Python 3.x

OpenCV

imutils

numpy

Matterport Mask R-CNN library

espeak-ng (for text-to-speech)

Pre-trained weights for Mask R-CNN and class label files (COCO dataset)

(Optional) Caffe model and prototxt files for alternative detection

Installation
Clone the repository:

bash
git clone https://github.com/vignesh362/Audio-Based-Environment-Simulator.git
cd Audio-Based-Environment-Simulator
Install required Python packages:

bash
pip install -r requirements.txt
(You might need to manually install the Mask R-CNN library and OpenCV if not included)

Install espeak-ng for text-to-speech:

bash
sudo apt-get install espeak-ng
Download weights & labels:

Place the Mask R-CNN COCO weights (mask_rcnn_coco.h5) and labels (coco_labels.txt) in the repository root.

For alternative detection, place the Caffe SSD model (.caffemodel) and prototxt.

Usage
1. Run the Audio Server
Start the socket server for audio output:

bash
python client.py
This will wait for object data and announce detected objects and their positions.

2. Run the Detection Script
Option A: Mask R-CNN Detection (Recommended for accuracy)
bash
python ada.py --weights mask_rcnn_coco.h5 --labels coco_labels.txt
Analyzes camerastream (cv2.VideoCapture('http://192.168.43.81:8081')).

For each detected object: sends info to the audio server.​

Option B: Caffe SSD Detection (Faster, less accurate)
bash
python detection.py --prototxt deploy.prototxt --model deploy.caffemodel --confidence 0.2
Uses a different model structure but also detects and labels surrounding objects.​

3. Hearing the Audio Cues
As the detection modules process frames, objects close to the user will be announced with positions (e.g., "person is at the left").

Example Workflow
Blind user is walking with camera (PiCam/webcam/mobile stream).

Detection script analyzes video and identifies "person" to the left, "car" to the front.

Sends this info to client.py, which uses espeak-ng to say "person is at the left," "car is at the front".
