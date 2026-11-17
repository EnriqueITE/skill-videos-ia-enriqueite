#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Enrique Serrano Aparicio (EnriqueITE)
# SPDX-License-Identifier: GPL-3.0-only
# Revisión 2026-11-17: evita sobrescribir proyectos existentes.
"""
nuevo_video.py - Crea la carpeta de un vídeo nuevo con la estructura del método.

Uso:
    python3 nuevo_video.py --tema receta-rapida --formato reel [--raiz ./videos]

Crea  AAAA-MM-DD_<tema>_<formato>/  con  01_guion, 02_audio, 03_visual, 04_video, 05_portada
y copia dentro las plantillas de la skill. Solo usa la biblioteca estándar.
"""
import argparse, datetime, os, re, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
PLANTILLAS = os.path.join(AQUI, "..", "templates")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tema", required=True)
    ap.add_argument("--formato", choices=["reel", "youtube"], required=True)
    ap.add_argument("--raiz", default=".")
    a = ap.parse_args()
    tema = re.sub(r"[^a-z0-9-]+", "-", a.tema.lower()).strip("-")
    if not tema:
        ap.error("El tema debe contener al menos una letra de a-z o un número.")
    nombre = "%s_%s_%s" % (datetime.date.today().isoformat(), tema, a.formato)
    base = os.path.join(a.raiz, nombre)
    try:
        os.makedirs(base, exist_ok=False)
    except FileExistsError:
        ap.error("La carpeta ya existe; usa otro tema o raíz para no sobrescribir tu trabajo: " + base)
    for sub in ("01_guion", "02_audio", "03_visual/imagenes", "03_visual/clips", "04_video", "05_portada", "assets/iconos"):
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    guion = "guion_reel.md" if a.formato == "reel" else "guion_youtube.md"
    shutil.copy(os.path.join(PLANTILLAS, guion), os.path.join(base, "01_guion", "guion.md"))
    shutil.copy(os.path.join(PLANTILLAS, "escenas_plantilla.md"), os.path.join(base, "03_visual", "escenas.md"))
    shutil.copy(os.path.join(PLANTILLAS, "escenas_ejemplo.json"), os.path.join(base, "03_visual", "escenas.json"))
    shutil.copy(os.path.join(PLANTILLAS, "checklist_publicacion.md"), os.path.join(base, "checklist.md"))
    open(os.path.join(base, "01_guion", "fuentes.md"), "w", encoding="utf-8").write(
        "# Fuentes\n\n| Dato | Fuente primaria | Fecha | Estado |\n|---|---|---|---|\n")
    print("Carpeta creada:", base)

if __name__ == "__main__":
    main()
