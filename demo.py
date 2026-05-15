"""
Demo Nusantara NLP — Jalankan dari folder nusantara-nlp/
=========================================================
Contoh:
    py demo.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nusantara import NLP
from nusantara.normalizer import SlangNormalizer, EmojiConverter
from nusantara.stemmer import Stemmer
from nusantara.stopword import StopwordRemover

SEPARATOR = "─" * 65


def demo_full_pipeline():
    print(f"\n{'═'*65}")
    print("  🌴 NUSANTARA NLP — Demo Pipeline Lengkap")
    print(f"{'═'*65}")

    nlp = NLP(stopword_mode="standard")

    contoh = [
        "gw ga suka pelayanan di sini 😠 parah banget!!",
        "makanannya enak bgt, mantap jiwa! 😋👍",
        "temen2 bilang tempat ini recommended buat liburan",
        "wkwk tp beneran deh, harganya ngga masuk akal",
        "Produk ini SANGAT mengecewakan, tidak sesuai deskripsi 😤",
    ]

    for teks in contoh:
        print(f"\n{SEPARATOR}")
        hasil = nlp.process(teks)
        print(f"  🔹 INPUT     : {hasil['raw']}")
        print(f"  🔸 NORMAL    : {hasil['normalized']}")
        print(f"  🔸 CLEANED   : {hasil['cleaned']}")
        print(f"  🔸 TOKENS    : {hasil['tokens']}")
        print(f"  🔸 NO STOP   : {hasil['tokens_clean']}")
        print(f"  🔸 STEMMED   : {hasil['tokens_stem']}")
        print(f"  ✅ RESULT    : {hasil['result']}")


def demo_stemmer():
    print(f"\n{'═'*65}")
    print("  🌱 DEMO STEMMER — Hybrid ECS + Lookup Table")
    print(f"{'═'*65}")
    stemmer = Stemmer()

    uji = [
        ("mempermasalahkan", "masalah"),
        ("berlari-lari", "lari"),
        ("ketidakhadiran", "hadir"),
        ("pembelajaran", "ajar"),
        ("pelajar", "ajar"),
        ("menyanyikan", "nyanyi"),
        ("kebaikan", "baik"),
        ("pertumbuhan", "tumbuh"),
    ]

    print(f"\n  {'Input':<25} {'Hasil':<20} {'Ekspektasi':<15} {'✓'}")
    print(f"  {'-'*60}")
    for kata, ekspektasi in uji:
        hasil = stemmer.stem(kata)
        status = "✅" if hasil == ekspektasi else "⚠️ "
        print(f"  {kata:<25} {hasil:<20} {ekspektasi:<15} {status}")


def demo_slang():
    print(f"\n{'═'*65}")
    print("  💬 DEMO SLANG NORMALIZER")
    print(f"{'═'*65}")
    norm = SlangNormalizer()

    contoh = [
        "gw udh makan tp masih laper",
        "baguuuus banget produknya, mantap bgt",
        "makan2 aja kerjanya lo",
        "ga ada yg bisa bantu?",
    ]

    for teks in contoh:
        print(f"\n  Input : {teks}")
        print(f"  Output: {norm.normalize(teks)}")


def demo_emoji():
    print(f"\n{'═'*65}")
    print("  😊 DEMO EMOJI CONVERTER")
    print(f"{'═'*65}")
    conv = EmojiConverter()

    contoh = [
        "Pelayanannya bagus 👍 tapi harganya mahal 😢",
        "Makanannya enak banget 😋🔥",
        "Saya tidak suka ini 😠❌",
    ]

    for teks in contoh:
        print(f"\n  Input : {teks}")
        print(f"  Output: {conv.convert(teks)}")


def demo_stopword():
    print(f"\n{'═'*65}")
    print("  🚫 DEMO STOPWORD REMOVAL (Negation-Aware)")
    print(f"{'═'*65}")

    tokens = ["saya", "tidak", "suka", "pelayanan", "yang", "ini"]
    print(f"\n  Input tokens : {tokens}")

    for mode in ["conservative", "standard", "aggressive"]:
        remover = StopwordRemover(mode=mode)
        hasil = remover.remove_tokens(tokens)
        print(f"  [{mode:12}] → {hasil}")

    print(f"\n  ⚡ Kata 'tidak' selalu dipertahankan (negation-protected!)")


if __name__ == "__main__":
    demo_full_pipeline()
    demo_stemmer()
    demo_slang()
    demo_emoji()
    demo_stopword()

    print(f"\n{'═'*65}")
    print("  🎉 Demo selesai! Nusantara NLP v0.1.0 siap digunakan.")
    print(f"{'═'*65}\n")
