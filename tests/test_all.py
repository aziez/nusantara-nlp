"""
Test Suite — Nusantara NLP
============================
Jalankan dengan: pytest tests/ -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from nusantara import NLP
from nusantara.stemmer import Stemmer
from nusantara.stopword import StopwordRemover
from nusantara.normalizer import SlangNormalizer, EmojiConverter
from nusantara.tokenizer import Tokenizer


# ────────────────────────────────────────────────
# TEST: Stemmer
# ────────────────────────────────────────────────

class TestStemmer:
    def setup_method(self):
        self.stemmer = Stemmer()

    def test_kata_dasar_tidak_berubah(self):
        assert self.stemmer.stem("makan") == "makan"
        assert self.stemmer.stem("jalan") == "jalan"

    def test_strip_prefix_me(self):
        # "membantu" → "bantu"
        hasil = self.stemmer.stem("membantu")
        assert hasil == "bantu"

    def test_strip_prefix_ber(self):
        hasil = self.stemmer.stem("berjalan")
        assert hasil == "jalan"

    def test_strip_suffix_kan(self):
        hasil = self.stemmer.stem("jalankan")
        assert hasil == "jalan"

    def test_strip_suffix_an(self):
        hasil = self.stemmer.stem("makanan")
        assert hasil == "makan"

    def test_konfiks_ke_an(self):
        hasil = self.stemmer.stem("kebaikan")
        assert hasil == "baik"

    def test_kata_pendek_tidak_di_stem(self):
        assert self.stemmer.stem("di") == "di"
        assert self.stemmer.stem("ke") == "ke"

    def test_kata_tidak_dikenali_dikembalikan_utuh(self):
        # Kata asing tidak diubah
        hasil = self.stemmer.stem("xyz123")
        assert hasil == "xyz123"


# ────────────────────────────────────────────────
# TEST: Stopword Remover
# ────────────────────────────────────────────────

class TestStopwordRemover:
    def test_mode_standard(self):
        remover = StopwordRemover(mode="standard")
        tokens = ["saya", "suka", "makan", "dan", "minum"]
        hasil = remover.remove_tokens(tokens)
        assert "dan" not in hasil
        assert "makan" in hasil

    def test_negasi_selalu_dipertahankan(self):
        remover = StopwordRemover(mode="aggressive")
        tokens = ["saya", "tidak", "suka", "ini", "yang"]
        hasil = remover.remove_tokens(tokens)
        # "tidak" HARUS tetap ada walau mode aggressive
        assert "tidak" in hasil

    def test_mode_conservative_lebih_sedikit_hapus(self):
        conservative = StopwordRemover(mode="conservative")
        standard = StopwordRemover(mode="standard")
        tokens = ["adalah", "merupakan", "di", "dan", "untuk"]
        hasil_c = set(conservative.remove_tokens(tokens))
        hasil_s = set(standard.remove_tokens(tokens))
        # conservative menghapus lebih sedikit
        assert len(hasil_c) >= len(hasil_s)

    def test_mode_invalid_raises_error(self):
        with pytest.raises(ValueError):
            StopwordRemover(mode="ngasal")

    def test_extra_stopwords(self):
        remover = StopwordRemover(extra_words=["mantap", "josss"])
        tokens = ["pelayanan", "mantap", "josss", "sekali"]
        hasil = remover.remove_tokens(tokens)
        assert "mantap" not in hasil
        assert "josss" not in hasil
        assert "pelayanan" in hasil


# ────────────────────────────────────────────────
# TEST: Slang Normalizer
# ────────────────────────────────────────────────

class TestSlangNormalizer:
    def setup_method(self):
        self.norm = SlangNormalizer()

    def test_singkatan_umum(self):
        hasil = self.norm.normalize("aing dah makan")
        assert "saya" in hasil
        assert "sudah" in hasil

    def test_negasi_slang(self):
        hasil = self.norm.normalize("kaga mau pergi")
        assert "tidak" in hasil

    def test_repetisi_huruf(self):
        hasil = self.norm.normalize("baguuuus banget")
        # "baguuuus" → "baguss" (max 2 huruf berulang)
        assert "uuu" not in hasil

    def test_reduplikasi_angka(self):
        hasil = self.norm.normalize("makan2 terus")
        # "makan2" → "makan makan"
        assert hasil.count("makan") == 2

    def test_extra_kamus(self):
        norm = SlangNormalizer(extra_kamus={"mantul": "mantap sekali"})
        hasil = norm.normalize("mantul banget")
        assert "mantap sekali" in hasil


# ────────────────────────────────────────────────
# TEST: Emoji Converter
# ────────────────────────────────────────────────

class TestEmojiConverter:
    def setup_method(self):
        self.conv = EmojiConverter()

    def test_emoji_dikonversi(self):
        hasil = self.conv.convert("bagus 👍")
        assert "👍" not in hasil
        assert "bagus" in hasil

    def test_mode_remove(self):
        conv = EmojiConverter(mode="remove")
        hasil = conv.convert("bagus 👍 sekali")
        assert "👍" not in hasil

    def test_has_emoji(self):
        assert self.conv.has_emoji("ini 😊 bagus") is True
        assert self.conv.has_emoji("tanpa emoji") is False

    def test_teks_tanpa_emoji_tidak_berubah(self):
        teks = "pelayanan sangat baik"
        assert self.conv.convert(teks) == teks


# ────────────────────────────────────────────────
# TEST: Tokenizer
# ────────────────────────────────────────────────

class TestTokenizer:
    def setup_method(self):
        self.tok = Tokenizer()

    def test_tokenisasi_dasar(self):
        hasil = self.tok.tokenize("makan minum jalan")
        assert hasil == ["makan", "minum", "jalan"]

    def test_expand_reduplikasi_hubung(self):
        hasil = self.tok.tokenize("teman-teman semua hadir")
        assert "teman" in hasil
        assert "teman-teman" not in hasil

    def test_filter_token_pendek(self):
        hasil = self.tok.tokenize("di a b makan")
        # "b" harus difilter, "a" dan "di" boleh
        assert "b" not in hasil
        assert "a" in hasil

    def test_tokenize_sentences(self):
        paragraf = "Ini enak. Itu tidak enak. Bagaimana menurutmu?"
        kalimat = self.tok.tokenize_sentences(paragraf)
        assert len(kalimat) >= 2


# ────────────────────────────────────────────────
# TEST: Full Pipeline (NLP class)
# ────────────────────────────────────────────────

class TestNLPPipeline:
    def setup_method(self):
        self.nlp = NLP()

    def test_output_berisi_semua_kunci(self):
        hasil = self.nlp.process("aing tidak suka ini")
        required_keys = ["raw", "normalized", "cleaned", "tokens",
                         "tokens_clean", "tokens_stem", "result"]
        for key in required_keys:
            assert key in hasil

    def test_negasi_tidak_hilang(self):
        hasil = self.nlp.process("saya tidak suka pelayanan ini")
        # Kata "tidak" harus ada di tokens_clean
        assert "tidak" in hasil["tokens_clean"]

    def test_emoji_diproses(self):
        hasil = self.nlp.process("bagus 👍")
        # Emoji sudah terkonversi
        assert "👍" not in hasil["normalized"]

    def test_slang_ternormalisasi(self):
        hasil = self.nlp.process("aing mau makan")
        assert "saya" in hasil["normalized"]

    def test_result_adalah_string(self):
        hasil = self.nlp.process("makanan enak")
        assert isinstance(hasil["result"], str)
