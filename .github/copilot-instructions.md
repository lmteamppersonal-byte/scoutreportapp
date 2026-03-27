# 📘 AI Assistant Guide for Scout Report

This repository is a small Streamlit application that produces professional scouting reports for football players. All logic is contained in a single script (`scout_app.py`), with supporting test scripts and an HTML template. Use this document to understand the "why" and key patterns so that an AI agent can contribute quickly.

---
## 🏗️ Big Picture

- **Single-page Streamlit app** (`scout_app.py`) drives the UI, data flow, export logic and helper functions.
- **Data model** is defined by the `SCOUTING_MODEL` constant at the top of `scout_app.py`.  It maps each **position** to four sub‑categories (`Físicas`, `Técnicas`, `Táticas`, `Cognitivas`) and lists of attributes.  The rest of the UI loops over this structure; adding a new position or attribute usually only requires editing this dictionary.
- **User inputs** are collected via `streamlit` widgets (text_input, selectbox, sliders) and stored in local variables or `st.session_state`.  The evaluation sliders use keys formatted as `"{position}_{cat}_{attr}"` so values persist across reruns.
- **Visualisation** uses Plotly (`go.Figure`, `Barpolar`) and a fixed `CATEGORY_COLORS` map.  A radar chart (polar bar) and a summary table are generated from the same data structure.
- **Exports**:
  - **PDF** via `reportlab` (ReportLab styles defined inside `main()`; a temporary file mechanism handles images).  See the large `if st.button("📄 Gerar Relatório PDF"):` block.
  - **HTML** using a static `report_template.html` with placeholder tokens (`{player_name}`, `{chart_html}`, etc.) replaced with `.replace()`.  The app base64‑encodes images and writes the final string to a download button.
- **Scraping helpers** exist (`extrair_id_jogador()`, `puxar_dados_sofascore()`, `puxar_dados_sofascore_selenium()`), though the UI currently collects data manually. These functions expect a SofaScore URL/ID and return JSON.
- **Testing** consists of two standalone scripts: `test_kaleido.py` (verifies Plotly/Kaleido image export) and `test_sofa.py` (exercises the URL extractor).  They are not part of a formal test suite but can be run with `python` directly.

---
## ⚙️ Developer Workflow

1. **Environment setup**
   ```bash
   pip install -r requirements.txt
   ```
   Dependencies: `streamlit`, `pandas`, `plotly`, `requests`, `beautifulsoup4`, `reportlab`, `kaleido`, `selenium`, `webdriver-manager`.
   Selenium is optional; it’s only used by the helper that boots Chrome in headless mode (webdriver‑manager auto‑downloads the driver).

2. **Run the app locally**
   ```bash
   streamlit run scout_app.py
   ```
   Open `http://localhost:8501` in a browser.

3. **Run tests**
   ```bash
   python test_kaleido.py
   python test_sofa.py
   ```
   (no test framework configured).

4. **Debugging**
   - Modify `scout_app.py` and reload Streamlit; stateful sliders keep values between runs.
   - Print stack traces in the UI (`st.error` + `st.code(traceback.format_exc())` is already used in export blocks).
   - Temporary images are cleaned up in a `finally` block after PDF generation.

5. **Adding features**
   - Follow existing UI patterns: use `st.sidebar` for configuration, `st.columns()` and `st.tabs()` for layout.
   - Use the `SCOUTING_MODEL` structure for anything position‑specific; the export logic automatically adapts.
   - When manipulating the HTML template, add corresponding `{placeholder}` tokens and update the replacement section in code.

6. **Localization / strings**
   The UI is in Portuguese; all hard‑coded labels in `scout_app.py` reflect that. Keep consistency if you add new text.

---
## 🧩 Project‑specific Conventions

- **Colors** are picked by the user in the sidebar and passed through exports. `highlight_color` and `text_color` are hex strings that drive PDF/HTML styling.
- **Session state** is used exclusively for the editable statistics table (`st.session_state.df_stats`).  The `st.session_state` key names are documented in the code.
- **Temporary files** for images/profiles/heatmaps are created with `tempfile.NamedTemporaryFile(delete=False)` and explicitly removed after export.
- **Placeholder substitution** in HTML uses simple `.replace()` rather than template engines; the order of replacements matters when placeholders are substrings of one another.
- **User uploads** (`file_uploader`) return a `BytesIO`‑like object; the code writes `profile_pic.getvalue()` directly to disk for ReportLab or encodes to base64 for HTML.
- **Attribute ordering** for the radar chart is fixed by flattening `categories.values()` into `all_attrs_ordered` to keep axes consistent.

---
## 🔗 Integration Points & External Dependencies

- **SofaScore scraping**: two helper variants. The API method (`requests` + headers) is preferred. The Selenium version is a fallback when the API fails.
- **Plotly/Kaleido**: must generate images in headless contexts; `test_kaleido.py` ensures this works.  PNG export is used for embedding in both PDF and HTML.
- **ReportLab**: all PDF layout is done programmatically (no separate template). Styles are defined inline; refer to the `ParagraphStyle` and `TableStyle` definitions for examples.
- **Streamlit**: the app uses modern components like `st.data_editor` and `st.plotly_chart`; review the docs if you add new widgets.

---
## ✅ What to Add to PRs

When modifying behavior that affects the export outputs (e.g. new data in PDF/HTML), include a screenshot or example file in the PR description.  Since there is no CI, manual verification is expected.

---
> **Need help?** After reviewing these instructions, let me know if any section seems unclear or if there’s additional context you’d like documented.