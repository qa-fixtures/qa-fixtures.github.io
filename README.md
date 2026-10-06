# qa-fixtures.github.io

Public web fixtures for the beSirius automated and manual tests, served by GitHub Pages at
**https://qa-fixtures.github.io/**. The account is the shared QA identity
(`qa-autotests@besirius.io`), so no test depends on a person's account.

Everything here is either fictional (Halvorsen Silica Works AS, Nordvik, Société Minière du
Lac Ténébreux, АО «Северный Глинозём») or a verbatim copy of a redistributable third-party file
kept so that a test asserting its bytes does not depend on someone else's host.

The coordinates, the publish procedure and the inventory of every external page the tests
depend on are documented in the beSirius 2.0 repository, `architecture/development/qa-environments.md`,
section "QA web fixture host".

| Path | What it is | Used by |
|---|---|---|
| `index.html`, `about.html`, `sustainability/index.html` | Company site of the fictional Halvorsen Silica Works AS — the scraper walks it | TestRail C16344 |
| `policies/halvorsen-responsible-sourcing-policy-2026.txt` | UTF-8 policy published only as `.txt`, linked from the sustainability page | C16344; BugBug artifact `bb-legacy-txt-manifest.json` (C19070) |
| `legacy/*.doc`, `legacy/*.xls` | Genuine OLE2 Word 97 / Excel 97 files | C16371 and the 1.0-import conversion checks |
| `legacy/ooxml/*.xlsx`, `legacy/ooxml/*.docx` | OOXML bytes served under legacy `.xls` / `.doc` names by a manifest | BugBug artifact `bb-legacy-ooxml-manifest.json` (C16387) |
| `encodings/politika-cp1251.txt`, `encodings/politique-latin1.txt` | Non-UTF-8 plain text (Windows-1251, ISO-8859-1) | C19072, C16345 |
| `encodings/politique-utf8.txt` | The same prose as UTF-8 | C16345 |
| `encodings/policy-page-html.txt` | A saved HTML page under a `.txt` name | C19073, C16345 |
| `broken/truncated-300-bytes.pdf` | The first 300 bytes of a PDF | C16728, C16739–C16741, C16748, C16749, C17013 |
| `broken/random-2048-bytes.pdf` | 2048 random bytes (Python `random.seed(1)`) named `.pdf` | the same cases |
| `third-party/ietf/rfc2119.txt` | RFC 2119, verbatim (IETF Trust permits full reproduction) | BugBug artifact `bb-legacy-txt-manifest.json` (C19070) |
| `third-party/xlrd/*.xls` | Excel 97-2003 samples from python-excel/xlrd, verbatim, under its `LICENSE` | C17012, C17013 |

## Rules

- **Paths are a contract.** BugBug artifacts and TestRail preconditions name these URLs. Never
  rename or delete a file; add a new one beside it.
- **Bytes are a contract too.** Never edit a file in place — a test may assert its size or encoding.
- `.nojekyll` keeps GitHub Pages from transforming anything; files are served as stored.
- A push is live in about a minute.
