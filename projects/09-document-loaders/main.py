import argparse
import csv
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


def html_text(source):
    parser = Extractor()
    parser.feed(source)
    return " ".join(parser.parts)


def load_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return "\n".join(", ".join(f"{key}: {value}" for key, value in row.items()) for row in csv.DictReader(handle))


def load_document(path):
    path = Path(path)
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if ext == ".csv":
        return load_csv(path)
    if ext in {".html", ".htm"}:
        return html_text(path.read_text(encoding="utf-8"))
    if ext == ".pdf":
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    if ext == ".docx":
        from docx import Document
        return "\n".join(paragraph.text for paragraph in Document(str(path)).paragraphs)
    raise ValueError("Unsupported format: " + ext)


def load_url(url, timeout=10):
    request = urllib.request.Request(url, headers={"User-Agent": "mini-document-loader/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return html_text(response.read().decode("utf-8", errors="replace"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    for path in sorted(Path("data").glob("sample.*")):
        print(path.name + ":", load_document(path)[:180])
    if args.smoke:
        assert "photovoltaic" in load_document("data/sample.html").lower()
        assert "Sunlight" in load_document("data/sample.csv")
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
