"""Build the population-endings fixture sites.

Two fictional company sites whose web collection must end in a known
population status:

  brattli-ceramics/  one readable report + one unreadable report -> partially-complete
  stenvik-minerals/  one unreadable report only                  -> failed

The unreadable report passes the scraper's own file check (over 1024 bytes,
opens with %PDF-, ends with %%EOF) so it is stored and handed to ingestion,
and its body is not a PDF object graph, so the parser cannot open it. A file
the scraper check refused would never be stored and would not count as a
failed document at all.

Run: python3 build.py  (writes next to this file; deterministic bytes)
"""

import random
from pathlib import Path

ROOT = Path(__file__).parent
FOOTER = "Fictional company. QA test fixture for the beSirius platform."


def readable_pdf(title: str, lines: list[str]) -> bytes:
    content = "\n".join(
        f"BT /F1 11 Tf 50 {760 - 22 * index} Td ({line}) Tj ET" for index, line in enumerate([title, FOOTER, *lines])
    ).encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Title (" + title.encode("latin-1") + b") /Producer (beSirius QA fixture) >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 6 0 R >>\nstartxref\n{xref_at}\n%%EOF\n".encode()
    return bytes(out)


def unreadable_pdf(seed: int) -> bytes:
    generator = random.Random(seed)
    body = bytes(generator.randrange(256) for _ in range(6144))
    body = body.replace(b"%%EOF", b"%%EOG").replace(b"obj", b"obk")
    return b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n" + body + b"\n%%EOF\n"


def page(title: str, body: str) -> str:
    return (
        '<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8">'
        f"<title>{title}</title></head>\n<body>\n{body}\n"
        f"<p><small>{FOOTER} It describes no real organisation.</small></p>\n</body>\n</html>\n"
    )


def site(slug: str, name: str, about: str, reports: list[tuple[str, str, bytes]]) -> None:
    folder = ROOT / slug
    (folder / "reports").mkdir(parents=True, exist_ok=True)
    (folder / "sustainability").mkdir(parents=True, exist_ok=True)
    # The reports are linked from the homepage as well: the scraper agent reads the
    # homepage first and does not reliably follow a second hop on a one-page site.
    home_links = "\n".join(f'<li><a href="reports/{file}">{label} (PDF)</a></li>' for file, label, _ in reports)
    (folder / "index.html").write_text(
        page(
            name,
            f"<h1>{name}</h1>\n<p>{about}</p>\n<h2>Sustainability reports</h2>\n<ul>\n{home_links}\n</ul>\n"
            "<p><a href=\"sustainability/\">Sustainability</a></p>",
        )
    )
    links = "\n".join(f'<li><a href="../reports/{file}">{label} (PDF)</a></li>' for file, label, _ in reports)
    (folder / "sustainability" / "index.html").write_text(
        page(
            f"Sustainability - {name}",
            "<h1>Sustainability</h1>\n<p>Our sustainability reporting for 2025 is published below.</p>\n"
            f"<ul>\n{links}\n</ul>\n<p><a href=\"../\">Home</a></p>",
        )
    )
    for file, _, data in reports:
        (folder / "reports" / file).write_bytes(data)


site(
    "brattli-ceramics",
    "Brattli Ceramics AS",
    "Brattli Ceramics AS makes technical ceramic tiles at its Hovden plant.",
    [
        (
            "brattli-ceramics-sustainability-report-2025.pdf",
            "Sustainability Report 2025",
            readable_pdf(
                "Brattli Ceramics AS - Sustainability Report 2025",
                [
                    "Scope 1 emissions: 6,240 tCO2e. Scope 2 emissions (market-based): 980 tCO2e.",
                    "Energy use: 52 GWh, of which 64 percent from renewable sources.",
                    "Water withdrawal: 145,000 m3; process water is recycled in a closed loop.",
                    "Health and safety: lost-time injury frequency rate 2.1 per million hours worked.",
                    "Certifications: ISO 14001 and ISO 45001 at the Hovden plant.",
                    "Responsible sourcing: all clay and feldspar suppliers signed the supplier code of conduct.",
                    "Governance: the board sustainability committee met four times in 2025.",
                ],
            ),
        ),
        (
            "brattli-ceramics-climate-and-energy-report-2025.pdf",
            "Climate and Energy Report 2025",
            unreadable_pdf(13178),
        ),
    ],
)

site(
    "stenvik-minerals",
    "Stenvik Minerals AS",
    "Stenvik Minerals AS quarries and grinds calcium carbonate at its Stenvik works.",
    [
        (
            "stenvik-minerals-sustainability-report-2025.pdf",
            "Sustainability Report 2025",
            unreadable_pdf(13179),
        ),
    ],
)
