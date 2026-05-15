"""
Stopword Remover Bahasa Indonesia — Context-Aware
==================================================
Perbedaan utama dengan Sastrawi:

  1. TIGA MODE OPERASI
     - conservative : hanya hapus kata penghubung dasar (aman untuk sentimen)
     - standard     : hapus stopword standar (default, seimbang)
     - aggressive   : hapus semua stopword termasuk kata sifat umum

  2. PERLINDUNGAN KATA NEGASI (FITUR KILLER)
     Kata seperti "tidak", "bukan", "jangan", "belum", "tanpa"
     TIDAK AKAN dihapus, karena membalik makna kalimat.
     Ini masalah kritis yang ada di Sastrawi!

  3. CUSTOM STOPWORDS
     Pengguna bisa tambah stopword sendiri tanpa edit source code.

  4. FILE-BASED DICT
     Stopword list bisa diperbarui tanpa ubah kode Python.
"""

import os
from pathlib import Path


class StopwordRemover:
    """
    Stopword Remover konteks-cerdas untuk Bahasa Indonesia.

    Contoh:
        remover = StopwordRemover(mode="conservative")
        kata_bersih = remover.remove_tokens(["saya", "tidak", "suka", "ini"])
        # → ["tidak", "suka"]  (kata negasi dilindungi!)
    """

    # Kata negasi yang SELALU dilindungi (tidak boleh dihapus)
    KATA_NEGASI = frozenset([
        "tidak", "tak", "bukan", "jangan", "belum", "tanpa",
        "tiada", "nggak", "enggak", "gak", "ga", "ndak",
        "anti", "non", "a", "un",  # prefix negasi
    ])

    def __init__(
        self,
        mode: str = "standard",
        extra_words: list = None,
        negasi_path: str = None,
        stopword_path: str = None,
    ):
        """
        Inisialisasi Stopword Remover.

        Args:
            mode (str): Mode operasi — "conservative", "standard", "aggressive"
            extra_words (list): Stopword tambahan dari pengguna
            negasi_path (str): Path custom ke file kata negasi
            stopword_path (str): Path custom ke file stopwords
        """
        if mode not in ("conservative", "standard", "aggressive"):
            raise ValueError(f"Mode '{mode}' tidak valid. Gunakan: conservative/standard/aggressive")
        self.mode = mode

        # Load data files
        data_dir = Path(__file__).parent / "data"
        self.stopwords = self._load_stopwords(str(data_dir / "stopwords_id.txt"))

        # Tambah custom stopwords jika ada (ke semua mode)
        if extra_words:
            extra_set = set(w.lower() for w in extra_words)
            for mode_key in self.stopwords:
                self.stopwords[mode_key].update(extra_set)

    def remove_tokens(self, tokens: list) -> list:
        """
        Hapus stopword dari list token.

        Args:
            tokens (list): List kata hasil tokenisasi

        Returns:
            list: Token yang bukan stopword (kata negasi tetap ada)
        """
        hasil = []
        for token in tokens:
            token_lower = token.lower()

            # RULE 1: Kata negasi selalu dipertahankan
            if token_lower in self.KATA_NEGASI:
                hasil.append(token_lower)
                continue

            # RULE 2: Cek apakah termasuk stopword sesuai mode
            if not self._is_stopword(token_lower):
                hasil.append(token_lower)

        return hasil

    def remove(self, teks: str) -> str:
        """
        Hapus stopword dari string teks (input/output string).

        Args:
            teks (str): Teks yang akan diproses

        Returns:
            str: Teks tanpa stopword
        """
        tokens = teks.lower().split()
        hasil = self.remove_tokens(tokens)
        return " ".join(hasil)

    def is_negasi(self, kata: str) -> bool:
        """Cek apakah kata termasuk kata negasi."""
        return kata.lower() in self.KATA_NEGASI

    # ─────────────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ─────────────────────────────────────────────────────────────────

    def _is_stopword(self, kata: str) -> bool:
        """Tentukan apakah kata adalah stopword sesuai mode."""
        if self.mode == "conservative":
            # Hanya hapus konjungsi, preposisi, dan artikel dasar
            return kata in self.stopwords.get("conservative", set())
        elif self.mode == "standard":
            return kata in self.stopwords.get("standard", set())
        elif self.mode == "aggressive":
            return kata in self.stopwords.get("aggressive", set())
        return False

    def _load_stopwords(self, path: str) -> dict:
        """
        Muat stopwords dari file dan kelompokkan berdasarkan mode.

        Format file:
            [conservative]
            dan
            atau

            [standard]
            adalah
            ...

            [aggressive]
            sangat
            ...
        """
        stopwords = {
            "conservative": set(),
            "standard": set(),
            "aggressive": set(),
        }

        current_mode = None
        try:
            with open(path, encoding="utf-8") as f:
                for baris in f:
                    baris = baris.strip()
                    if not baris or baris.startswith("#"):
                        continue
                    if baris.startswith("[") and baris.endswith("]"):
                        current_mode = baris[1:-1].lower()
                    elif current_mode in stopwords:
                        stopwords[current_mode].add(baris.lower())
        except FileNotFoundError:
            # Fallback minimal
            stopwords["standard"] = {"dan", "atau", "di", "ke", "dari", "yang", "ini", "itu"}

        # Mode "standard" juga mencakup "conservative"
        stopwords["standard"] = stopwords["conservative"] | stopwords["standard"]
        # Mode "aggressive" mencakup semua
        stopwords["aggressive"] = stopwords["standard"] | stopwords["aggressive"]

        return stopwords
