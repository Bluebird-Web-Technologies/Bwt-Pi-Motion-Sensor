import tkinter as tk
from dataclasses import dataclass
import detectors


@dataclass
class Layout:
    root: tk.Tk
    frame: tk.Frame | None = None
    label: tk.Label | None = None
    background_color: str = "black"
    message: str = ""

    def setup(self):
        """Set up the frame and label."""

        self.frame = tk.Frame(self.root, bg=self.background_color)

        self.label = tk.Label(
            self.frame,
            text=self.message,
            font=("Helvetica", 24),
            bg=self.background_color,
            fg="white",
        )

        self.label.config(text=self.message, bg=self.background_color, fg="white")

        self.label.pack(expand=True)
        self.frame.pack(fill="both", expand=True)

    def show(self):
        """Show the layout frame."""
        if self.frame is not None:
            self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the layout frame"""
        if self.frame is not None:
            self.frame.pack_forget()


class LayoutControl:
    def __init__(
        self,
        root,
        base_layout: Layout,
        sensed_layout: Layout,
        detector: detectors.Detector,
    ):
        self.base_layout = base_layout
        self.sensed_layout = sensed_layout

        self.root = root
        self.root.title("Motion Sensor Display")

        self.base_layout.setup()
        self.sensed_layout.setup()

        self.detector = detector

        self.MOTION_SENSOR_INTERVAL = 10000
        self.MOTION_SENSOR_CHECK_RATE = 100
        self.SENSED_PAGE_TIME = 5000

    def set_sensed(self):
        self.base_layout.hide()
        self.sensed_layout.show()

        self.root.after(self.MOTION_SENSOR_INTERVAL, lambda: self.set_base())

    def set_base(self):
        self.sensed_layout.hide()
        self.base_layout.show()

    def check(self):
        delay: int = self.MOTION_SENSOR_CHECK_RATE
        if self.detector.check_for_change():
            self.set_sensed()
            delay = self.SENSED_PAGE_TIME
        else:
            self.set_base()

        self.root.after(delay, self.check)

    def start(self):
        self.check()
        self.root.mainloop()


def main():
    root = tk.Tk()
    root.attributes("-fullscreen", True)

    not_triggered = Layout(
        root=root, background_color="blue", message="Welcome to Hackathon 2025"
    )

    triggered = Layout(
        root=root, background_color="red", message="Thank you for coming!"
    )

    detector = detectors.KeyDetector(root)
    controller = LayoutControl(root, not_triggered, triggered, detector)
    controller.start()


if __name__ == "__main__":
    main()
