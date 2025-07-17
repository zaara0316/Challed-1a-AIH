# PDF Outline Extractor (Dockerized)

## ✅ What It Does

Processes PDFs in `/app/input` to extract:

- Title (largest font on page 1)
- Headings (H1, H2, H3) based on font size
- Page numbers for each heading

Outputs results to `/app/output` in the required JSON format.

---

## 🛠️ How to Build and Run

### Build Docker Image:

```bash
docker build --platform linux/amd64 -t pdfoutline:latest .
```
