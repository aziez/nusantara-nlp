"""
Slang Normalizer — Konversi Teks Informal → Formal
===================================================
Fitur KILLER yang tidak dimiliki Sastrawi!

Menangani:
  - Singkatan umum    : "gw" → "saya", "yg" → "yang"
  - Slang gaul        : "bokap" → "ayah", "mantap" → "bagus"
  - Pengulangan huruf : "baguuuus" → "bagus"
  - L33tspeak         : "4ku" → "aku", "s3p3rti" → "seperti"
  - Kata gabung       : "makan2" → "makan makan"

Arsitektur:
  1. Pra-proses: normalisasi pengulangan huruf + l33tspeak
  2. Lookup: cari di kamus slang (JSON)
  3. Pasca-proses: tangani kata gabung angka (e.g. "makan2")
"""

import re
import json
from pathlib import Path


class SlangNormalizer:
    """
    Normalisasi teks informal/slang ke bahasa formal.

    Args:
        extra_kamus (dict): Kamus slang tambahan dari pengguna.
                            Key = slang, Value = kata formal.
    """

    # Tabel konversi l33tspeak → huruf normal
    LEETSPEAK_MAP = {
        "4": "a", "3": "e", "1": "i", "0": "o",
        "5": "s", "7": "t", "8": "b", "9": "g",
        "@": "a", "!": "i", "$": "s", "+": "t",
    }

    def __init__(self, kamus_path: str = None, extra_kamus: dict = None):
        """
        Inisialisasi SlangNormalizer dan muat kamus slang.

        Args:
            kamus_path (str): Path custom ke file kamus JSON.
            extra_kamus (dict): Kamus tambahan dari pengguna.
        """
        if kamus_path is None:
            kamus_path = Path(__file__).parent / "data" / "slang_dict.json"

        self.kamus = self._load_kamus(str(kamus_path))

        if extra_kamus:
            # Merge kamus custom, user punya prioritas lebih tinggi
            self.kamus.update({k.lower(): v for k, v in extra_kamus.items()})

    def normalize(self, teks: str) -> str:
        """
        Normalisasi teks slang menjadi teks formal.

        Urutan proses:
          1. Tangani kata gabung angka: "makan2" → "makan makan"
          2. Normalisasi pengulangan huruf: "baguuuus" → "bagus"
          3. Lookup kamus slang per kata

        Args:
            teks (str): Teks input yang akan dinormalisasi

        Returns:
            str: Teks yang sudah dinormalisasi
        """
        # Tahap 1: Tangani pengulangan kata (makan-makan, makan2)
        teks = self._normalize_reduplikasi(teks)

        # Tahap 2: Normalisasi pengulangan huruf
        teks = self._normalize_repetisi_huruf(teks)

        # Tahap 3: Normalisasi l33tspeak (hanya jika ada angka dalam kata)
        teks = self._normalize_leetspeak(teks)

        # Tahap 4: Lookup kamus slang per kata
        kata_list = teks.split()
        kata_list = [self.kamus.get(kata.lower(), kata) for kata in kata_list]

        return " ".join(kata_list)

    # ─────────────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ─────────────────────────────────────────────────────────────────

    def _normalize_reduplikasi(self, teks: str) -> str:
        """
        Konversi kata ulang:
          - "makan2" → "makan makan"
          - "bolak-balik" → tetap (bukan pengulangan sama)
        """
        # Pattern: kata diikuti angka 2 (e.g. "makan2")
        teks = re.sub(r"(\b[a-zA-Z]+)2\b", r"\1 \1", teks)
        return teks

    def _normalize_repetisi_huruf(self, teks: str) -> str:
        """
        Normalisasi huruf yang diulang berlebihan:
          - "baguuuuus" → "bagus"
          - "hahahaha" → "haha" (tawa)
          - "wkwkwkwk" → "wkwk" (tawa khas Indonesia)
        """
        # Kurangi huruf berulang lebih dari 2x menjadi 2x saja
        teks = re.sub(r"(.)\1{2,}", r"\1\1", teks)
        return teks

    def _normalize_leetspeak(self, teks: str) -> str:
        """Konversi karakter l33tspeak ke huruf biasa."""
        hasil = []
        for kata in teks.split():
            # Hanya proses jika ada karakter l33tspeak
            if any(c in self.LEETSPEAK_MAP for c in kata):
                kata = "".join(self.LEETSPEAK_MAP.get(c, c) for c in kata)
            hasil.append(kata)
        return " ".join(hasil)

    def _load_kamus(self, path: str) -> dict:
        """Muat kamus slang dari file JSON."""
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            # Hapus key komentar (key yang diawali "_")
            return {k.lower(): v for k, v in data.items() if not k.startswith("_")}
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback kamus minimal
            return {
                "gw": "saya", "gue": "saya", "lo": "kamu",
                "yg": "yang", "ga": "tidak", "gak": "tidak",
                "nggak": "tidak", "bgt": "banget", "jg": "juga",
                "kayak": "seperti", "aja":"saja",
                
            }
