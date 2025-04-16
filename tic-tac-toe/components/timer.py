class TurnTimer:
    def __init__(self, root, duration, on_timeout, label):
        self.root = root
        self.duration = duration
        self.on_timeout = on_timeout
        self.label = label
        self.remaining = duration
        self.timer_id = None

    def start(self):
        self.cancel()
        self.remaining = self.duration
        self._tick()

    def _tick(self):
        self.label.config(text=f"⏱ {self.remaining}s")
        if self.remaining > 0:
            self.remaining -= 1
            self.timer_id = self.root.after(1000, self._tick)
        else:
            self.on_timeout()

    def cancel(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
