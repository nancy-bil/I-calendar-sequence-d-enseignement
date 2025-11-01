# -*- coding: utf-8 -*-


import argparse, os
from nom_module_projet import lire_ics, creer_html

def main():
    """Lit les fichiers .ics ADE et crée un planning HTML unique."""
    parser = argparse.ArgumentParser(description="Extraction ADE (.ics) → HTML")
    parser.add_argument("--input-file", nargs="+", required=True, help="Liste des fichiers .ics")
    parser.add_argument("--output-dir", required=True, help="Répertoire du fichier HTML")
    args = parser.parse_args()

    planning_total = []
    for fichier in args.input_file:
        planning_total.extend(lire_ics(fichier))

    os.makedirs(args.output_dir, exist_ok=True)
    sortie = os.path.join(args.output_dir, "planning.html")
    creer_html(planning_total, sortie)
    print(f" Fichier HTML généré : {sortie}")

if __name__ == "__main__":
    main()
