import cv2
import time
import threading

class VideoAsCamera:
    def __init__(self, path, default_fps=30.0, st=0, en=None, display=False, display_width=640, display_fps=10):
        self.cap = cv2.VideoCapture(path)
        
        # 1. Setup FPS
        file_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fps = file_fps if file_fps > 0 else default_fps
        self.frame_time = 1.0 / self.fps

        # 2. Setup Loop Range (Seconds to Milliseconds)
        self.start_ms = st * 1000.0
        if en is not None:
            self.end_ms = en * 1000.0
        else:
            total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.end_ms = (total_frames / self.fps) * 1000.0

        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.start_ms)

        # 3. Setup Display and Resizing
        self.show_display = display
        self.display_width = display_width
        self.display_interval = 1.0 / display_fps if display_fps > 0 else 0.1
        self.last_display_time = 0
        self.window_name = f"Debug View: {path}"

        self.latest_frame = None
        self.running = True
        self._lock = threading.Lock()

    def start(self):
        # Set daemon=True so the thread exits when the main program stops
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        next_time = time.perf_counter()
        
        while self.running:
            ret, frame = self.cap.read()
            
            # Check loop range
            current_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            if not ret or current_ms >= self.end_ms:
                self.cap.set(cv2.CAP_PROP_POS_MSEC, self.start_ms)
                continue

            with self._lock:
                self.latest_frame = frame

            # Handle debug display (downsampling)
            if self.show_display:
                now = time.perf_counter()
                if now - self.last_display_time >= self.display_interval:
                    self._render_debug_view(frame)
                    self.last_display_time = now

            # Control capture FPS
            next_time += self.frame_time
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Reset if the process is falling behind
                next_time = time.perf_counter()

    def _render_debug_view(self, frame):
        """Scale and show frame for debugging"""
        h, w = frame.shape[:2]
        ratio = self.display_width / w
        dst_size = (self.display_width, int(h * ratio))
        
        # INTER_NEAREST is used for the lowest CPU overhead
        resized = cv2.resize(frame, dst_size, interpolation=cv2.INTER_NEAREST)
        
        cv2.imshow(self.window_name, resized)
        # cv2.waitKey is required to update the window
        cv2.waitKey(1)

    def get_frame(self):
        with self._lock:
            if self.latest_frame is None:
                return None
            # Return a copy to prevent modification by other threads
            return self.latest_frame.copy()

    def stop(self):
        """Stop the loop and release resources"""
        self.running = False
        time.sleep(0.2)
        if self.cap.isOpened():
            self.cap.release()
        if self.show_display:
            try:
                cv2.destroyWindow(self.window_name)
            except:
                pass
