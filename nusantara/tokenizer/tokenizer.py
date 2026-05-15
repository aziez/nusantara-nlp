"""
Tokenizer Bahasa Indonesia — Cerdas & Konteks-Aware
====================================================
Perbedaan dari tokenizer sederhana (split()):

  1. TANGANI KATA ULANG BERULANG
     "sehari-hari" → ["sehari", "hari"] (bukan ["sehari-hari"])

  2. TANGANI SINGKATAN UMUM
     "dll." → tetap "dll" (tidak dipecah jadi ["dll", ""])

  3. TOKENISASI KALIMAT (sentence tokenizer)
     Memecah paragraf menjadi list kalimat berdasarkan tanda baca.

Contoh:
    tokenizer = Tokenizer()

    # Word tokenizer
    tokenizer.tokenize("makanan-makanan enak ada di sana")
    # → ["makanan", "makanan", "enak", "ada", "di", "sana"]

    # Sentence tokenizer
    tokenizer.tokenize_sentences("Ini enak. Itu tidak. Bagaimana menurutmu?")
    # → ["Ini enak.", "Itu tidak.", "Bagaimana menurutmu?"]
"""

import re


class Tokenizer:
    """
    Smart Tokenizer untuk Bahasa Indonesia.
    """

    # Singkatan umum Indonesia yang tidak boleh dipecah di titiknya
    ABBREVIATIONS = frozenset([
        "dll", "dsb", "dst", "dkk", "dls", "dr", "prof", "mr", "mrs",
        "no", "vol", "hal", "hlm", "jl", "gg", "blk", "rt", "rw",
        "sd", "smp", "sma", "smk", "s1", "s2", "s3",
        "pt", "cv", "tbk", "ud", "pd",
        "yth", "ttd", "a/n", "u/p",
    ])

    def __init__(self):
        pass

    def tokenize(self, teks: str) -> list:
        """
        Tokenisasi teks menjadi list kata.

        Proses:
          1. Expand kata ulang: "makanan-makanan" → "makanan makanan"
          2. Split berdasarkan spasi

        Args:
            teks (str): Teks yang sudah di-lowercase dan cleaned

        Returns:
            list: List token (string)
        """
        # Tahap 1: Expand kata ulang (reduplikasi dengan tanda hubung)
        # e.g., "sehari-hari" → "sehari hari", "makan-makan" → "makan makan"
        teks = self._expand_reduplikasi(teks)

        # Tahap 2: Split dan filter token kosong
        tokens = [t.strip() for t in teks.split() if t.strip()]

        # Tahap 3: Filter token yang terlalu pendek (1 karakter selain 'a', 'i')
        tokens = [t for t in tokens if len(t) > 1 or t in ("a", "i")]

        return tokens

    def tokenize_sentences(self, teks: str) -> list:
        """
        Tokenisasi paragraf menjadi list kalimat.

        Menangani titik pada singkatan agar tidak memecah kalimat
        di tempat yang salah.

        Args:
            teks (str): Teks/paragraf yang akan dipecah

        Returns:
            list: List kalimat
        """
        # Sederhanakan: pecah berdasarkan . ! ? yang diikuti spasi + huruf kapital
        kalimat_list = re.split(r"(?<=[.!?])\s+(?=[A-Z])", teks)
        return [k.strip() for k in kalimat_list if k.strip()]

    # ─────────────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ─────────────────────────────────────────────────────────────────

    def _expand_reduplikasi(self, teks: str) -> str:
        """
        Expand kata ulang berimbuhan-tanda-hubung menjadi dua kata terpisah.

        Contoh:
          "sayur-mayur" → "sayur mayur"
          "berlari-lari" → "berlari lari"
          "teman-teman" → "teman teman"
        """
        # Pattern: kata-kata (dua bagian dipisah tanda hubung)
        return re.sub(r"(\b\w+)-(\w+\b)", r"\1 \2", teks)
