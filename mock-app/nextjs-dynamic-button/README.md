# Next.js Dynamic Button Color

Web sederhana dengan **warna button yang dibaca dari `config.json`** setiap kali halaman di-render (Server-Side Rendering).

## Cara Kerja

Setiap request ke halaman `/`, Next.js menjalankan `getServerSideProps` yang:
1. Membaca file `config.json` dari root project menggunakan `fs.readFileSync`
2. Mem-parse JSON-nya
3. Mengirim data config sebagai `props` ke komponen React

Karena menggunakan `getServerSideProps` (bukan `getStaticProps`), file `config.json` dibaca **fresh setiap render** — tanpa perlu restart server.

## Struktur Project

```
nextjs-dynamic-button/
├── config.json          ← ubah warna di sini!
├── pages/
│   ├── _app.js
│   ├── index.js         ← halaman utama + getServerSideProps
│   └── api/
│       └── config.js    ← API untuk baca/update config
├── styles/
│   ├── globals.css
│   └── Home.module.css
└── package.json
```

## Instalasi & Menjalankan

```bash
npm install
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000)

## Mengubah Warna Button

**Cara 1 — Edit langsung `config.json`:**

```json
{
  "buttonColor": "#ef4444",
  "buttonTextColor": "#ffffff",
  "buttonLabel": "Tombol Baru",
  "siteName": "Dynamic Button App",
  "description": "Warna button ini dibaca dari config.json setiap render!"
}
```

Simpan file → refresh browser → warna langsung berubah!

**Cara 2 — Lewat API (POST):**

```bash
curl -X POST http://localhost:3000/api/config \
  -H "Content-Type: application/json" \
  -d '{"buttonColor": "#10b981", "buttonLabel": "Hijau!"}'
```

## Contoh Warna

| Nama    | Hex       |
|---------|-----------|
| Ungu    | `#6366f1` |
| Merah   | `#ef4444` |
| Hijau   | `#10b981` |
| Oranye  | `#f97316` |
| Biru    | `#3b82f6` |
| Kuning  | `#eab308` |
