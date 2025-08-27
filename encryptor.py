# encryptor.py

class Encryptor:
    def __init__(self, key: int):
        """
        key: מפתח הצפנה פשוט מסוג int (0-255)
        """
        self.key = key

    def encrypt(self, text: str) -> str:
        """
        מבצע הצפנת XOR על כל תו במחרוזת.
        הצפנה ופענוח זהה עם אותו מפתח.
        """
        return "".join(chr(ord(c) ^ self.key) for c in text)

    def decrypt(self, text: str) -> str:
        """
        מפענח את המחרוזת המוצפנת (אותה פעולה כמו הצפנה).
        """
        return self.encrypt(text)  # XOR הפוך זהה להצפנה
