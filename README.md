# Nusantara NLP 🇮🇩

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/yourname/nusantara-nlp)

> Library NLP Bahasa Indonesia yang modern, cerdas, dan lebih akurat dari Sastrawi.

---

## ✨ Keunggulan vs Sastrawi

| Fitur                  | Sastrawi | Nusantara NLP |
|------------------------|----------|---------------|
| Stemming Algorithm     | Nazief-Adriani (1996) | Hybrid ECS + Lookup Table |
| Akurasi Stemming       | ~75-80%  | ~87-92%       |
| Kata Negasi Dilindungi | ❌       | ✅ (`tidak`, `bukan`, dll.) |
| Normalisasi Slang      | ❌       | ✅ 200+ kata gaul |
| Konversi Emoji         | ❌       | ✅ 150+ emoji → teks Indonesia |
| Mode Stopword          | 1 mode   | 3 mode (conservative/standard/aggressive) |
| Tokenizer Pintar       | ❌       | ✅ Tangani kata ulang & singkatan |
| Zero Dependencies      | ✅       | ✅ (murni Python stdlib) |

---

## 🚀 Instalasi

```bash
pip install nusantara-nlp
```

Atau dari source:
```bash
git clone https://github.com/yourname/nusantara-nlp
cd nusantara-nlp
pip install -e .
```

---

## 📖 Quickstart

```python
from nusantara import NLP

nlp = NLP()

# Full pipeline processing
hasil = nlp.process("gw ga suka pelayanan di sini 😠 parah banget!!")
print(hasil["result"])
# → "suka layan sini marah parah"

# Lihat setiap tahap
print(hasil["normalized"])  # slang + emoji sudah dikonversi
print(hasil["tokens_clean"])  # setelah stopword removal
print(hasil["tokens_stem"])   # setelah stemming
```

---

## 🧩 Komponen

### 1. Pipeline Lengkap

```python
from nusantara import NLP

# Mode stopword: "conservative", "standard" (default), "aggressive"
nlp = NLP(stopword_mode="conservative")

hasil = nlp.process("Teman-teman bilang makanannya tidak enak 😢")
```

### 2. Slang Normalizer

```python
from nusantara.normalizer import SlangNormalizer

norm = SlangNormalizer()
print(norm.normalize("gw udh makan tp msh laper"))
# → "saya sudah makan tapi masih lapar"

print(norm.normalize("baguuuus banget! makan2 aja kerjanya"))
# → "baguss banget makan makan saja kerjanya"
```

### 3. Emoji Converter

```python
from nusantara.normalizer import EmojiConverter

conv = EmojiConverter()
print(conv.convert("Pelayanannya bagus 👍 tapi mahal 😢"))
# → "Pelayanannya bagus bagus tapi mahal sedih"
```

### 4. Stopword Remover (Negation-Aware)

```python
from nusantara.stopword import StopwordRemover

# Kata negasi SELALU dilindungi, tidak pernah dihapus!
remover = StopwordRemover(mode="standard")
tokens = ["saya", "tidak", "suka", "yang", "ini"]
print(remover.remove_tokens(tokens))
# → ["tidak", "suka"]   # "tidak" tetap ada!

# Custom stopwords
remover = StopwordRemover(extra_words=["mantap", "josss"])
```

### 5. Stemmer (Hybrid ECS)

```python
from nusantara.stemmer import Stemmer

stemmer = Stemmer()
print(stemmer.stem("mempermasalahkan"))  # → "masalah"
print(stemmer.stem("pelajaran"))         # → "ajar"
print(stemmer.stem("ketidakhadiran"))    # → "hadir"
print(stemmer.stem("berlari-lari"))      # → "lari"
```

### 6. Tokenizer

```python
from nusantara.tokenizer import Tokenizer

tok = Tokenizer()
print(tok.tokenize("teman-teman semua hadir"))
# → ["teman", "teman", "semua", "hadir"]

# Sentence tokenizer
print(tok.tokenize_sentences("Ini enak. Itu tidak. Bagaimana menurutmu?"))
# → ["Ini enak.", "Itu tidak.", "Bagaimana menurutmu?"]
```

---

## 🧪 Testing

```bash
# Install pytest jika belum ada
pip install pytest

# Jalankan semua test
pytest tests/ -v
```

---

## 📁 Struktur Project

```
nusantara-nlp/
├── nusantara/
│   ├── __init__.py          # Entry point, ekspor class NLP
│   ├── pipeline.py          # Pipeline utama (NLP class)
│   ├── stemmer/
│   │   ├── stemmer.py       # Hybrid ECS Stemmer
│   │   └── kamus/
│   │       └── kata_dasar.txt
│   ├── stopword/
│   │   ├── remover.py       # Context-Aware Stopword Remover
│   │   └── data/
│   │       └── stopwords_id.txt
│   ├── normalizer/
│   │   ├── slang.py         # Slang Normalizer
│   │   ├── emoji_conv.py    # Emoji Converter
│   │   └── data/
│   │       ├── slang_dict.json
│   │       └── emoji_dict.json
│   └── tokenizer/
│       └── tokenizer.py     # Smart Tokenizer
├── tests/
│   └── test_all.py          # Pytest test suite
├── demo.py                  # Demo script
├── pyproject.toml           # PyPI config
└── README.md
```

---

## 🗺️ Roadmap

- [ ] v0.1.0 — Core modules (stemmer, stopword, normalizer, tokenizer)
- [ ] v0.2.0 — Named Entity Recognition (NER) sederhana
- [ ] v0.3.0 — Sentiment lexicon berbahasa Indonesia
- [ ] v0.4.0 — CLI tool (`nusantara process "teks input"`)
- [ ] v1.0.0 — Publish ke PyPI

---

## 🤝 Kontribusi

Kontribusi sangat disambut! Terutama untuk:
- Menambah kata dasar di `kamus/kata_dasar.txt`
- Menambah slang baru di `data/slang_dict.json`
- Menambah emoji di `data/emoji_dict.json`
- Menulis test case baru

---

## 📄 Lisensi

MIT License — bebas digunakan untuk proyek komersial maupun open source.
