# CiptaCoding — Instagram Carousel

Sistem desain carousel Instagram untuk CiptaCoding, diturunkan dari sistem visual
**buildwithangga.com**.

## Spesifikasi

- Canvas: **1080 × 1350 px** (4:5, format portrait Instagram)
- Slide: 7 per carousel
- Render: Chrome headless → PNG, mode RGB, opaque
- Font: **Poppins** 300/400/500/600/700, di-embed base64 (latin subset)
- Bahasa: Indonesia

## Sistem visual (BWA-derived)

Token diekstrak dari CSS produksi buildwithangga.com
(`build/assets/app-*.css`, arsip Wayback 2025-01-03):

| Token | Nilai | Pemakaian |
|---|---|---|
| Ink | `#0F172A` | headline |
| Ink 800 | `#1E293B` | slide gelap, kartu solid |
| Ink 500 | `#64748B` | body copy |
| Surface | `#F1F5F9` | background tint |
| Accent | `#4F46E5` | indigo — emphasis, angka, dot aktif |
| Accent 200 | `#A5B4FC` | aksen di atas permukaan gelap |
| Brand blue | `#0664FE` | **hanya** tombol CTA |

Identitas CiptaCoding tetap hadir lewat logo dan warna CTA. Sisanya mengikuti
sistem BWA, bukan navy/off-white CiptaCoding lama.

## Struktur

```
posts/p1_01.html … p1_07.html   slide (HTML)
src/assets/style.css            design system + font ter-embed
src/assets/logo-mark.png        logo CiptaCoding (transparan)
exports/*.png                   hasil render 1080×1350
preview-all.png                 contact sheet 7 slide
render.py                       renderer Chrome headless
index.html                      galeri + design tokens
```

## Render ulang

```bash
python3 render.py        # semua slide
python3 render.py p1_04  # satu slide
```

## Alur carousel

1. **Hook** — Sewa software atau miliki sendiri? (+ 3 stat)
2. **Masalah** — Harga langganan tidak pernah turun (SaaS vs custom)
3. **Biaya tersembunyi** — 3 hal yang tidak muncul di invoice
4. **Hitungan** — Lima tahun, dua hasil berbeda (Rp 144 jt vs aset tetap)
5. **Kualifikasi** — Kapan custom software masuk akal
6. **Proses** — Empat tahap, tanpa kejutan
7. **CTA** — Mulai dari satu percakapan

## Regenerasi font

Style.css menyimpan Poppins sebagai base64. Untuk memperbarui:

```bash
curl -H "User-Agent: Mozilla/5.0" \
  "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" \
  -o /tmp/poppins.css
```

lalu konversi tiap `url()` latin subset ke base64 dan sisipkan sebagai `@font-face`.
