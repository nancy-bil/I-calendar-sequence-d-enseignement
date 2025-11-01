# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

def lire_ics(fichier_ics):
    """Lit un fichier .ics ADE et renvoie une liste de cours (planning)."""
    with open(fichier_ics, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    contenu = "".join(("\n" + l.strip()) if not l.startswith(" ") else l.strip() for l in lignes)
    planning, cours = [], {}

    for ligne in contenu.split("\n"):
        if "DTSTART" in ligne:
            cours["debut"] = datetime.strptime(ligne.split(":")[1], "%Y%m%dT%H%M%SZ") + timedelta(hours=1)
        elif "DTEND" in ligne:
            cours["fin"] = datetime.strptime(ligne.split(":")[1], "%Y%m%dT%H%M%SZ") + timedelta(hours=1)
        elif "SUMMARY" in ligne:
            cours["module"] = ligne.split(":", 1)[1]
        elif "LOCATION" in ligne:
            cours["salle"] = ligne.split(":", 1)[1]
        elif "DESCRIPTION" in ligne:
            desc = [p.strip() for p in ligne.split("\\n") if p and not p.startswith(("(", "RT")) and "Updated" not in p]
            cours["prof"] = desc[-1] if desc else "Inconnu"
        elif "END:VEVENT" in ligne:
            planning.append(cours)
            cours = {}
    return planning


def creer_html(planning, fichier_html):
    """Crée un fichier HTML simple avec le planning."""
    with open(fichier_html, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Planning ADE</title>")
        f.write("<style>body{font-family:Arial;}table{border-collapse:collapse;width:100%;}"
                "th,td{border:1px solid #ccc;padding:5px;text-align:left;}th{background:#eee;}</style></head><body>")
        f.write("<h2>Planning extrait depuis ADE</h2><table>")
        f.write("<tr><th>Date</th><th>Début</th><th>Fin</th><th>Module</th><th>Salle</th><th>Professeur</th></tr>")
        for c in planning:
            f.write(f"<tr><td>{c['debut'].strftime('%d/%m/%Y')}</td>"
                    f"<td>{c['debut'].strftime('%H:%M')}</td>"
                    f"<td>{c['fin'].strftime('%H:%M')}</td>"
                    f"<td>{c.get('module','')}</td>"
                    f"<td>{c.get('salle','')}</td>"
                    f"<td>{c.get('prof','')}</td></tr>")
        f.write("</table></body></html>")
