"""
Nusantara NLP — Library NLP Bahasa Indonesia Modern
=====================================================
Library NLP berbahasa Indonesia yang lebih cerdas dan modern,
dirancang untuk menangani teks formal maupun informal (slang,
media sosial, emoji, dll).

Fitur Unggulan vs Sastrawi:
  ✅ Slang Normalization   — konversi kata gaul ke formal
  ✅ Emoji Conversion      — emoji → deskripsi teks Indonesia
  ✅ Negation-aware SW     — kata negasi tidak dihapus
  ✅ Hybrid Stemmer        — Lookup Table + ECS Algorithm
  ✅ Smart Tokenizer       — tangani kata majemuk & singkatan

Contoh Penggunaan:
    from nusantara import NLP
    nlp = NLP()
    result = nlp.process("gw ga suka makanan ini 😠")
    print(result)
"""

from .pipeline import NLP

__version__ = "0.1.0"
__author__ = "Nusantara NLP Team"
__all__ = ["NLP"]
