from abc import ABC, abstractmethod

class IWriter(ABC):
    @abstractmethod
    def send_data(self, data: str, machine_name: str) -> None:
        pass


class Encryptor:
    def __init__(self, key: int):
        self.key = key

    def xor_encrypt(self, text: str) -> str:
        # מצפין/מפענח כל תו לפי מפתח ה־XOR
        return "".join(chr(ord(c) ^ self.key) for c in text)


class FileWriter(IWriter):
    def __init__(self, file_path: str, encryptor: Encryptor):
        self.file_path = file_path
        self.encryptor = encryptor

    def send_data(self, data: str, machine_name: str) -> None:
        # מוסיף את שם המכונה לנתון
        full_text = f"[{machine_name}] {data}"
        # הצפנה ב־XOR
        encrypted = self.encryptor.xor_encrypt(full_text)
        # שמירה לקובץ
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(encrypted + "\n")