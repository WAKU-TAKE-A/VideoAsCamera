# VideoAsCamera

A Python utility class to simulate a live network camera (RTSP/IP camera) using a local video file. It is designed for testing and debugging image processing applications without needing a physical camera.

## Features

- **Threaded Capture**: Reading and timing are handled in a background thread for smooth performance.
- **Accurate FPS Control**: Maintains the video's original frame rate or a user-defined fallback.
- **Looping with Range**: Loop specific sections of a video by defining start (`st`) and end (`en`) timestamps in seconds.
- **Debug View**: Optional real-time display with customizable width and downsampled FPS to minimize CPU overhead.
- **Thread-Safe**: Uses threading locks to ensure frame integrity during retrieval.
- **Clean Shutdown**: Methods to release resources and close windows properly.

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)

```bash
pip install opencv-python

Usage
from video_as_camera import VideoAsCamera
import cv2

# Initialize: Loop from 5.0s to 15.0s with a debug display at 5 FPS
cam = VideoAsCamera(
    path="your_video.mp4",
    st=5.0,
    en=15.0,
    display=True,
    display_width=640,
    display_fps=5
)

cam.start()

try:
    while True:
        frame = cam.get_frame()
        if frame is not None:
            # Your image processing logic here
            # e.g., result = model.predict(frame)
            pass
        
except KeyboardInterrupt:
    print("Stopping...")

finally:
    cam.stop()
```

## API Reference

### `VideoAsCamera(...)` (Constructor)
Initializes the camera simulator.

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `path` | string | (Required) | Path to the video file. |
| `default_fps` | float | `30.0` | Fallback FPS if file metadata is unreadable. |
| `st` | float | `0` | Start time in seconds. |
| `en` | float | `None` | End time in seconds (None = end of file). |
| `display` | bool | `False` | Whether to show a debug window. |
| `display_width`| int | `640` | Width of the debug window. |
| `display_fps` | int | `10` | Refresh rate of the debug window. |

### Methods

| Method | Return Type | Description |
| :--- | :--- | :--- |
| `start()` | `None` | Starts the background thread and begins video playback. |
| `get_frame()` | `ndarray` or `None` | Returns the latest frame as a NumPy array (OpenCV format). Returns `None` if no frame is available yet. |
| `stop()` | `None` | Stops the background thread, releases the video file, and closes any debug windows. |


