import nbformat as nbf
import glob
import os

LICENSE_TEXT = """>**Licensing Notice**: Text and media: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); Code: [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)"""

def inject_license():
    # Targets all notebooks in posts/ and its subdirectories
    for nb_path in glob.glob("posts/**/*.ipynb", recursive=True):
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbf.read(f, as_version=4)

        if not nb.cells:
            continue

        # Check if license exists and where
        license_indices = [i for i, cell in enumerate(nb.cells) if "Licensing Notice" in cell.source]

        # If exactly one license and it's at the end, skip
        if len(license_indices) == 1 and license_indices[0] == len(nb.cells) - 1:
            continue

        # Remove existing license cells (if checks failed above, we need to move/add)
        nb.cells = [cell for i, cell in enumerate(nb.cells) if i not in license_indices]

        # Create and append the license cell
        new_cell = nbf.v4.new_markdown_cell(LICENSE_TEXT)
        nb.cells.append(new_cell)

        with open(nb_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f"✅ Injected license into: {nb_path}")

if __name__ == "__main__":
    inject_license()
