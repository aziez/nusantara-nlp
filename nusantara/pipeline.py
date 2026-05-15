"""
Pipeline Utama Nusantara NLP
==============================
Menggabungkan semua komponen menjadi satu antarmuka yang mudah digunakan.

Alur Preprocessing (urutan default):
  1. Emoji Conversion   → emoji → teks deskripsi Indonesia
  2. Slang Normalization → kata gaul → kata formal
  3. Case Folding       → huruf kapital → huruf kecil
  4. Cleaning           → hapus karakter tidak relevan
  5. Tokenizing         → kalimat → list kata
  6. Stopword Removal   → hapus kata tidak bermakna (negasi aman)
  7. Stemming           → kata berimbuhan → kata dasar
"""

import re
from .normalizer import SlangNormalizer, EmojiConverter
from .stopword import StopwordRemover
from .stemmer import Stemmer
from .tokenizer import Tokenizer


class NLP:
    """
    Pipeline NLP Bahasa Indonesia — Antarmuka Utama Nusantara NLP.

    Contoh Penggunaan:
        nlp = NLP()

        # Proses lengkap (default)
        hasil = nlp.process("gw ga suka pelayanan ini 😠")
        print(hasil["tokens_clean"])

        # Hanya normalisasi
        teks_normal = nlp.normalize("makan2 yg enak bgt")

        # Hanya stemming
        teks_stem = nlp.stem("mempermasalahkan")

    Args:
        stopword_mode (str): Mode stopword removal.
            - "conservative" : hapus stopword dasar saja (aman untuk sentimen)
            - "standard"     : hapus stopword standar (default)
            - "aggressive"   : hapus semua stopword termasuk kata sifat umum
        extra_stopwords (list): Daftar stopword tambahan dari pengguna.
        extra_slang (dict): Kamus slang tambahan dari pengguna.
    """

    def __init__(
        self,
        stopword_mode: str = "standard",
        extra_stopwords: list = None,
        extra_slang: dict = None,
    ):
        self.emoji_conv = EmojiConverter()
        self.slang_norm = SlangNormalizer(extra_kamus=extra_slang)
        self.stopword_rem = StopwordRemover(
            mode=stopword_mode, extra_words=extra_stopwords
        )
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def process(self, teks: str) -> dict:
        """
        Jalankan full preprocessing pipeline.

        Returns:
            dict dengan kunci:
                - raw          : teks asli
                - normalized   : setelah emoji conv + slang norm
                - cleaned      : setelah cleaning + case fold
                - tokens       : list token setelah cleaning
                - tokens_clean : list token setelah stopword removal
                - tokens_stem  : list token setelah stemming
                - result       : string akhir (join dari tokens_stem)
        """
        raw = teks

        # Tahap 1 & 2: Normalisasi (emoji + slang)
        normalized = self.normalize(teks)

        # Tahap 3 & 4: Case fold + cleaning
        cleaned = self._clean(normalized)

        # Tahap 5: Tokenisasi
        tokens = self.tokenizer.tokenize(cleaned)

        # Tahap 6: Stopword removal (negation-aware)
        tokens_clean = self.stopword_rem.remove_tokens(tokens)

        # Tahap 7: Stemming
        tokens_stem = [self.stemmer.stem(t) for t in tokens_clean]

        return {
            "raw": raw,
            "normalized": normalized,
            "cleaned": cleaned,
            "tokens": tokens,
            "tokens_clean": tokens_clean,
            "tokens_stem": tokens_stem,
            "result": " ".join(tokens_stem),
        }

    def normalize(self, teks: str) -> str:
        """Konversi emoji → teks, lalu slang → formal."""
        teks = self.emoji_conv.convert(teks)
        teks = self.slang_norm.normalize(teks)
        return teks

    def stem(self, kata: str) -> str:
        """Stem satu kata ke bentuk dasarnya."""
        return self.stemmer.stem(kata)

    def remove_stopwords(self, teks: str) -> str:
        """Hapus stopword dari teks (string input/output)."""
        tokens = self.tokenizer.tokenize(teks.lower())
        tokens_clean = self.stopword_rem.remove_tokens(tokens)
        return " ".join(tokens_clean)

    def tokenize(self, teks: str) -> list:
        """Tokenisasi teks menjadi list kata."""
        return self.tokenizer.tokenize(teks)

    # ------------------------------------------------------------------
    # PRIVATE HELPERS
    # ------------------------------------------------------------------

    def _clean(self, teks: str) -> str:
        """Case folding + hapus karakter non-alfabet."""
        teks = teks.lower()
        # Hapus URL
        teks = re.sub(r"http\S+|www\S+", "", teks)
        # Hapus mention & hashtag
        teks = re.sub(r"@\w+|#\w+", "", teks)
        # Hapus angka
        teks = re.sub(r"\d+", "", teks)
        # Hapus karakter selain huruf dan spasi
        teks = re.sub(r"[^a-z\s]", " ", teks)
        # Normalisasi spasi ganda
        teks = re.sub(r"\s+", " ", teks).strip()
        return teks
