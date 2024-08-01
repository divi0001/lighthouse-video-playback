# LightLight Project

LightLight is a project designed to display videos on a "lighthouse"-style display in Kiel. This project allows users to either play videos from local files or download and play videos from YouTube, displaying them on a 28x14 LED grid.

## Requirements

- Python 3.10+
- OpenCV (`cv2`)
- Pyghthouse (`pyghthouse`)
- pytubefix

Since youtube changes frequently, pytubefix is used instead of pytube directly, because YoouTube updates made pytube directly not work properly.

## Installation

1. **Install the required packages**:
    ```bash
    pip install opencv-python pyghthouse pytubefix
    ```

2. **Put your username and API-token into `login.py`**:
    ```python
    # login.py
    username = 'your_username'
    token = 'your_api_token'
    ```
