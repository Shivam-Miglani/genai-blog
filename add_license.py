import nbformat as nbf
import glob
import os

LICENSE_TEXT = """::: {.callout-note appearance="simple"}
### Licensing Notice
Text and media: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
Code and snippets: [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
:::"""

def inject_license():
    # Targets all notebooks in posts/ and its subdirectories
    for nb_path in glob.glob("posts/**/*.ipynb", recursive=True):
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbf.read(f, as_version=4)

        if not nb.cells:
            continue

        # Check if license already exists in the first two cells to avoid duplicates
        if any("Licensing Notice" in cell.source for cell in nb.cells[:2]):
            continue

        # Create the license cell
        new_cell = nbf.v4.new_markdown_cell(LICENSE_TEXT)

        # Logic: If first cell is Quarto YAML (--- title: ... ---), insert as 2nd cell
        first_cell_src = nb.cells[0].source.strip()
        if first_cell_src.startswith("---") and first_cell_src.endswith("---"):
            nb.cells.insert(1, new_cell)
        else:
            nb.cells.insert(0, new_cell)

        with open(nb_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f"✅ Injected license into: {nb_path}")

if __name__ == "__main__":
    inject_license()
