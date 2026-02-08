from flask import Flask, render_template, abort
import os

app = Flask(__name__)

# Modules (3 modules)
MODULES = {
    "circuit": {
        "nom": "Circuit électrique",
        "description": "Cours, TD et examens du module Circuit électrique.",
        "folder": "circuit"
    },
    "analogique": {
        "nom": "Électronique analogique",
        "description": "Cours, TD et examens du module Électronique analogique.",
        "folder": "analogique"
    },
    "electrotechnique": {
        "nom": "Électrotechnique",
        "description": "Cours, TD et examens du module Électrotechnique.",
        "folder": "electrotechnique"
    }
}

# 3 sections fixes
SECTIONS = [
    ("cours", "Cours"),
    ("td", "Travaux dirigés"),
    ("examens", "Examens")
]

# Lire automatiquement les PDF
def list_pdfs(module_folder, section_key):
    path = os.path.join(app.static_folder, "pdf", module_folder, section_key)
    if not os.path.isdir(path):
        return []
    files = [f for f in os.listdir(path) if f.lower().endswith(".pdf")]
    files.sort()
    return files


# ------------------- Pages principales -------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/modules")
def modules():
    return render_template("modules.html", modules=MODULES)


@app.route("/apropos")
def apropos():
    return render_template("apropos.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ------------------- Pages modules -------------------
@app.route("/module/<slug>")
def module_home(slug):
    module = MODULES.get(slug)
    if not module:
        abort(404)

    return render_template(
        "module_home.html",
        module=module,
        slug=slug,
        sections=SECTIONS
    )


@app.route("/module/<slug>/<section>")
def module_section(slug, section):
    module = MODULES.get(slug)
    if not module:
        abort(404)

    valid_sections = [s[0] for s in SECTIONS]
    if section not in valid_sections:
        abort(404)

    pdfs = list_pdfs(module["folder"], section)
    section_label = dict(SECTIONS)[section]
    base_url = f"pdf/{module['folder']}/{section}"

    return render_template(
        "module_section.html",
        module=module,
        slug=slug,
        section=section,
        section_label=section_label,
        pdfs=pdfs,
        base_url=base_url
    )


if __name__ == "__main__":
    app.run(debug=True)
