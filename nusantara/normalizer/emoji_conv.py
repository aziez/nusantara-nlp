"""
Emoji Converter — Ubah Emoji menjadi Deskripsi Teks Bahasa Indonesia
====================================================================
Fitur penting untuk analisis teks media sosial karena pengguna sering
mengekspresikan sentimen lewat emoji.

Contoh:
    converter = EmojiConverter()
    converter.convert("Pelayanannya bagus 👍")
    # → "Pelayanannya bagus jempol"
    converter.convert("Aku sedih 😢 tapi tetap semangat 💪")
    # → "Aku sedih sedih tapi tetap semangat kuat"
"""

import json
import re
from pathlib import Path


class EmojiConverter:
    """
    Konverter emoji ke deskripsi teks bahasa Indonesia.

    Args:
        kamus_path (str): Path custom ke file kamus emoji JSON.
        mode (str): "replace" (default) atau "remove" untuk menghapus emoji.
    """

    def __init__(self, kamus_path: str = None, mode: str = "replace"):
        if mode not in ("replace", "remove"):
            raise ValueError("mode harus 'replace' atau 'remove'")
        self.mode = mode

        if kamus_path is None:
            kamus_path = Path(__file__).parent / "data" / "emoji_dict.json"

        self.kamus = self._load_kamus(str(kamus_path))

    def convert(self, teks: str) -> str:
        """
        Konversi emoji dalam teks ke deskripsi Indonesia.

        Args:
            teks (str): Teks yang mungkin mengandung emoji

        Returns:
            str: Teks dengan emoji dikonversi/dihapus
        """
        hasil = []
        for karakter in teks:
            if karakter in self.kamus:
                if self.mode == "replace":
                    hasil.append(f" {self.kamus[karakter]} ")
                # Jika mode "remove", skip emoji
            else:
                hasil.append(karakter)

        # Normalisasi spasi ganda
        return re.sub(r"\s+", " ", "".join(hasil)).strip()

    def has_emoji(self, teks: str) -> bool:
        """Cek apakah teks mengandung emoji yang dikenali."""
        return any(c in self.kamus for c in teks)

    def list_emoji_found(self, teks: str) -> list:
        """Kembalikan list emoji yang ditemukan beserta artinya."""
        return [(c, self.kamus[c]) for c in teks if c in self.kamus]

    def _load_kamus(self, path: str) -> dict:
        """Muat kamus emoji dari file JSON."""
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return {k: v for k, v in data.items() if not k.startswith("_")}
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback kamus emoji paling umum
            return {
                "😀": "senang", "😊": "senyum", "😢": "sedih",
                "😡": "marah", "👍": "bagus", "👎": "jelek",
                "❤️": "cinta", "💪": "kuat", "🔥": "keren",
            }
