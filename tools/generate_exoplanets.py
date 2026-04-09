"""
Script de pre-traitement : NASA Exoplanet Archive -> assets/exoplanets.json

Usage : py tools/generate_exoplanets.py
Lance depuis la racine du projet Flutter.

Lit le CSV brut, filtre default_flag=1 (une ligne par planete),
extrait les colonnes utiles et genere un fichier JSON compact.
"""

import csv
import json
import os
import sys

INPUT_FILE  = "PS_2026.04.09_03.06.45.csv"
OUTPUT_FILE = os.path.join("assets", "exoplanets.json")

# Indices des colonnes (en-tete ligne 90 du fichier CSV)
COL = {
    'pl_name':         0,
    'hostname':        1,
    'default_flag':    2,
    'discoverymethod': 6,
    'disc_year':       7,
    'disc_facility':   8,
    'pl_orbper':      12,   # periode orbitale (jours)
    'pl_rade':        20,   # rayon (Terres)
    'pl_radj':        24,   # rayon (Jupiters)
    'pl_bmasse':      28,   # masse (Terres)
    'pl_eqt':         41,   # temperature equilibre (K)
    'st_spectype':    46,   # type spectral etoile
    'st_teff':        47,   # temperature etoile (K)
    'rastr':          69,   # ascension droite (texte)
    'ra':             70,   # ascension droite (degres)
    'decstr':         71,   # declinaison (texte)
    'dec':            72,   # declinaison (degres)
    'sy_dist':        77,   # distance (parsecs)
}


def safe_float(val, decimals=2):
    try:
        return round(float(val), decimals)
    except (ValueError, TypeError):
        return None


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERREUR : fichier introuvable -> {INPUT_FILE}")
        print("Lance ce script depuis la racine du projet.")
        sys.exit(1)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    planets = []
    skipped_non_default = 0

    print(f"Lecture de {INPUT_FILE} ...")
    with open(INPUT_FILE, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith('#') or row[0] == 'pl_name':
                continue
            try:
                if row[COL['default_flag']] != '1':
                    skipped_non_default += 1
                    continue
            except IndexError:
                continue

            planets.append({
                "n":  row[COL['pl_name']],           # name
                "h":  row[COL['hostname']],           # host star
                "m":  row[COL['discoverymethod']],    # method
                "y":  row[COL['disc_year']],          # year
                "f":  row[COL['disc_facility']],      # facility
                "op": safe_float(row[COL['pl_orbper']]),          # orbital period
                "re": safe_float(row[COL['pl_rade']]),            # radius Earth
                "rj": safe_float(row[COL['pl_radj']], 4),         # radius Jupiter
                "me": safe_float(row[COL['pl_bmasse']]),          # mass Earth
                "t":  safe_float(row[COL['pl_eqt']], 0),          # eq temperature
                "sp": row[COL['st_spectype']],                    # spectral type
                "st": safe_float(row[COL['st_teff']], 0),         # star temp
                "rs": row[COL['rastr']],                          # RA string
                "ra": safe_float(row[COL['ra']], 4),              # RA degrees
                "ds": row[COL['decstr']],                         # Dec string
                "dc": safe_float(row[COL['dec']], 4),             # Dec degrees
                "d":  safe_float(row[COL['sy_dist']], 1),         # distance pc
            })

    print(f"  Doublons filtres (default_flag!=1) : {skipped_non_default}")
    print(f"  Planetes conservees               : {len(planets)}")

    print(f"\nGeneration de {OUTPUT_FILE} ...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(planets, f, ensure_ascii=False, separators=(',', ':'))

    size_kb = os.path.getsize(OUTPUT_FILE) // 1024
    print(f"  Fichier genere : {OUTPUT_FILE} ({size_kb} KB)")
    print("\nTermine. N'oublie pas de declarer l'asset dans pubspec.yaml.")


if __name__ == '__main__':
    main()
