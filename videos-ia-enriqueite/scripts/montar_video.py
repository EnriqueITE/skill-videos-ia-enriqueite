#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Enrique Serrano Aparicio (EnriqueITE)
# SPDX-License-Identifier: GPL-3.0-only
# Revisión 2026-11-17: valida tiempos, protege salidas y conserva la duración con audio corto.
"""
montar_video.py - Montaje automático de reels (9:16) y vídeos de YouTube (16:9).

Ejemplo de la skill "videos-ia-enriqueite". Solo usa Python 3, Pillow, numpy y ffmpeg (vía subprocess).

Estructura esperada en la carpeta del vídeo (--entrada):
    01_guion/subtitulos.srt        (opcional) subtítulos que se queman en el vídeo
    02_audio/locucion.wav|.mp3     (opcional) voz (grabada o generada, p. ej. con ElevenLabs)
    02_audio/musica.mp3            (opcional) música de fondo
    03_visual/escenas.json         (obligatorio) lista de escenas, ver templates/escenas_ejemplo.json
    03_visual/imagenes/...         (opcional) fondos referenciados en "imagen"
    assets/iconos/<nombre>.png     (opcional) iconos; si faltan, se dibuja un marcador genérico

Uso:
    python3 montar_video.py --formato reel --entrada ./2026-01-01_tema_reel --salida final.mp4
    python3 montar_video.py --formato youtube --entrada ./carpeta --salida final.mp4 --fuente ./MiFuente.ttf
    python3 montar_video.py --formato reel --entrada ./carpeta --salida prueba.mp4 --escala 0.5   # vista previa rápida

Buenas prácticas que aplica (adáptalas a tu canal):
    - El gancho (primera escena) se ve desde el fotograma 0.
    - Nada queda estático más de 0,7 s: cada elemento entra y luego "respira" (escala del 2-4 %).
    - Textos dentro de la zona segura (8 % lateral, 15 % inferior, 10 % superior en vertical).
    - La fuente del dato se muestra abajo mientras dura la escena.
    - Audio: música bajo la voz con ducking y mezcla final a -14 LUFS / -1 dBTP (loudnorm en dos pasadas).
"""
import argparse, json, math, os, re, shutil, subprocess, sys, tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ configuración
FORMATOS = {"reel": (1080, 1920), "youtube": (1920, 1080)}
FPS = 30
# Colores por defecto: cámbialos por los de tu marca (o usa --color-principal / --color-acento).
COLOR_PRINCIPAL = "#1F2937"   # texto e iconos
COLOR_ACENTO = "#F5C518"      # subrayados y palabra clave
COLOR_FONDO_REEL = "#FFFFFF"  # fondo claro por defecto en reels (cámbialo por el tuyo)
COLOR_FONDO_YT = "#111827"    # fondo de respaldo en YouTube si la escena no tiene imagen
FUENTES_CANDIDATAS = [        # se usa la primera que exista si no pasas --fuente
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cargar_fuente(ruta, tam):
    for r in ([ruta] if ruta else []) + FUENTES_CANDIDATAS:
        if r and os.path.exists(r):
            return ImageFont.truetype(r, tam)
    return ImageFont.load_default()


def ease_out(t):
    """curva de entrada suave (0..1)."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


# ------------------------------------------------------------------ subtítulos
def leer_srt(ruta):
    """Devuelve [(inicio, fin, texto)] a partir de un .srt sencillo."""
    if not os.path.exists(ruta):
        return []
    bloques = open(ruta, encoding="utf-8").read().strip().split("\n\n")
    out = []
    for b in bloques:
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", b)
        if not m:
            continue
        g = list(map(int, m.groups()))
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        z = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        texto = " ".join(b.split("\n")[2:]).strip()
        out.append((a, z, texto))
    return out


def partir_lineas(draw, texto, fuente, ancho_max, max_lineas=3):
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if draw.textlength(prueba, font=fuente) <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas[:max_lineas]


# ------------------------------------------------------------------ capas
class Montador:
    def __init__(self, formato, carpeta, fuente=None, escala=1.0, principal=COLOR_PRINCIPAL, acento=COLOR_ACENTO):
        w, h = FORMATOS[formato]
        self.formato = formato
        self.W, self.H = int(w * escala) // 2 * 2, int(h * escala) // 2 * 2   # H.264 necesita dimensiones pares
        self.s = self.W / w                                                    # factor de escala general
        self.carpeta = carpeta
        self.principal, self.acento = hex_rgb(principal), hex_rgb(acento)
        base = min(self.W, self.H)
        self.f_texto = cargar_fuente(fuente, int(base * 0.085))
        self.f_fuente = cargar_fuente(fuente, int(base * 0.034))
        self.f_sub = cargar_fuente(fuente, int(base * 0.045))
        self.f_icono = cargar_fuente(fuente, int(base * 0.07))
        # zona segura
        self.mx = int(self.W * 0.08)
        self.top = int(self.H * 0.10)
        self.bottom = int(self.H * (0.85 if formato == "reel" else 0.90))
        self._cache_fondos, self._cache_iconos = {}, {}

    # --- fondos (se precalculan una vez por escena)
    def fondo(self, escena):
        clave = escena.get("imagen") or "__liso__"
        if clave in self._cache_fondos:
            return self._cache_fondos[clave]
        ruta = os.path.join(self.carpeta, "03_visual", escena["imagen"]) if escena.get("imagen") else None
        if ruta and os.path.exists(ruta):
            img = Image.open(ruta).convert("RGB")
            # recorte tipo "cover" con un 6 % de margen para el zoom lento
            r = max(self.W * 1.06 / img.width, self.H * 1.06 / img.height)
            img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
        else:
            color = COLOR_FONDO_REEL if self.formato == "reel" else COLOR_FONDO_YT
            img = Image.new("RGB", (int(self.W * 1.06), int(self.H * 1.06)), hex_rgb(color))
        self._cache_fondos[clave] = img
        return img

    def recorte_fondo(self, img, t_rel):
        """zoom lento (Ken Burns): evita que el fondo quede estático."""
        z = 1.0 + 0.05 * t_rel                          # 0..1 a lo largo de la escena
        cw, ch = int(self.W * 1.06 / z), int(self.H * 1.06 / z)
        x0, y0 = (img.width - cw) // 2, (img.height - ch) // 2
        return img.crop((x0, y0, x0 + cw, y0 + ch)).resize((self.W, self.H), Image.BILINEAR)

    # --- iconos (PNG con transparencia o marcador genérico)
    def icono(self, nombre, tam):
        clave = (nombre, tam)
        if clave in self._cache_iconos:
            return self._cache_iconos[clave]
        ruta = os.path.join(self.carpeta, "assets", "iconos", nombre + ".png")
        if os.path.exists(ruta):
            ic = Image.open(ruta).convert("RGBA").resize((tam, tam), Image.LANCZOS)
        else:
            ic = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
            d = ImageDraw.Draw(ic)
            d.ellipse((4, 4, tam - 4, tam - 4), outline=self.principal + (255,), width=max(3, tam // 18))
            letra = nombre[:1].upper() or "?"
            tw = d.textlength(letra, font=self.f_icono)
            d.text(((tam - tw) / 2, tam * 0.18), letra, font=self.f_icono, fill=self.acento + (255,))
        self._cache_iconos[clave] = ic
        return ic

    # --- un fotograma
    def fotograma(self, escena, t, subtitulos):
        dur = max(0.01, escena["fin"] - escena["inicio"])
        t_rel = (t - escena["inicio"]) / dur
        t_loc = t - escena["inicio"]
        frame = self.recorte_fondo(self.fondo(escena), t_rel).convert("RGBA")
        capa = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        oscuro = escena.get("imagen") or self.formato == "youtube"
        col_texto = (255, 255, 255) if oscuro else self.principal

        # 1) texto principal: entrada en 0,3 s (escala 0,8 -> 1 y opacidad) + respiración continua
        texto = escena.get("texto_pantalla") or ""
        if texto:
            e = 1.0 if escena["inicio"] == 0 else ease_out(t_loc / 0.3)
            respira = 1 + 0.025 * math.sin(2 * math.pi * t_loc / 1.4)
            lineas = partir_lineas(d, texto, self.f_texto, self.W - 2 * self.mx)
            alto_linea = int(self.f_texto.size * 1.15)
            y = self.top + int(self.H * 0.08)
            bloque = Image.new("RGBA", (self.W, alto_linea * len(lineas) + 30), (0, 0, 0, 0))
            db = ImageDraw.Draw(bloque)
            for i, ln in enumerate(lineas):
                tw = db.textlength(ln, font=self.f_texto)
                db.text(((self.W - tw) / 2, i * alto_linea), ln, font=self.f_texto, fill=col_texto + (255,))
            subr_w = int(self.W * 0.18 * e)
            db.rectangle(((self.W - subr_w) // 2, len(lineas) * alto_linea + 8,
                          (self.W + subr_w) // 2, len(lineas) * alto_linea + 8 + max(4, int(10 * self.s))), fill=self.acento + (255,))
            f = (0.8 + 0.2 * e) * respira
            bw, bh = int(bloque.width * f), int(bloque.height * f)
            bloque = bloque.resize((max(1, bw), max(1, bh)), Image.BILINEAR)
            alpha = bloque.split()[3].point(lambda a: int(a * e))
            bloque.putalpha(alpha)
            capa.alpha_composite(bloque, ((self.W - bw) // 2, y - (bh - alto_linea * len(lineas)) // 2))

        # 2) iconos: entrada escalonada + pulso con desfase (nada quieto más de 0,7 s)
        iconos = escena.get("iconos") or []
        if iconos:
            tam = int(min(self.W, self.H) * 0.16)
            hueco = int(tam * 0.4)
            total = len(iconos) * tam + (len(iconos) - 1) * hueco
            x = (self.W - total) // 2
            y = int(self.H * (0.50 if self.formato == "reel" else 0.55))
            for k, nombre in enumerate(iconos):
                e = ease_out((t_loc - 0.12 * k) / 0.3)
                if e <= 0:
                    x += tam + hueco
                    continue
                pulso = 1 + 0.04 * math.sin(2 * math.pi * (t_loc / 0.9 + k * 0.33))
                lado = max(1, int(tam * (0.8 + 0.2 * e) * pulso))
                ic = self.icono(nombre, tam).resize((lado, lado), Image.BILINEAR)
                a = ic.split()[3].point(lambda v: int(v * e))
                ic.putalpha(a)
                dy = int((1 - e) * tam * 0.3)
                capa.alpha_composite(ic, (x + (tam - lado) // 2, y + (tam - lado) // 2 + dy))
                x += tam + hueco

        # 3) fuente del dato, abajo y dentro de la zona segura
        if escena.get("fuente"):
            fy = self.bottom - int(self.f_fuente.size * 1.6)
            tw = d.textlength(escena["fuente"], font=self.f_fuente)
            d.text(((self.W - tw) / 2, fy), escena["fuente"], font=self.f_fuente, fill=col_texto + (230,))

        # 4) subtítulos quemados: máx. 2 líneas, caja semitransparente y texto claro
        sub = next((s for s in subtitulos if s[0] <= t < s[1]), None)
        if sub:
            lineas = partir_lineas(d, sub[2], self.f_sub, self.W - 2 * self.mx - 40, max_lineas=2)
            alto = int(self.f_sub.size * 1.25)
            y0 = self.bottom - int(self.H * 0.06) - alto * len(lineas) - 24
            anchomax = max(d.textlength(l, font=self.f_sub) for l in lineas)
            d.rounded_rectangle(((self.W - anchomax) / 2 - 20, y0 - 12, (self.W + anchomax) / 2 + 20, y0 + alto * len(lineas) + 8),
                                radius=14, fill=(0, 0, 0, 191))
            for i, l in enumerate(lineas):
                tw = d.textlength(l, font=self.f_sub)
                d.text(((self.W - tw) / 2, y0 + i * alto), l, font=self.f_sub, fill=(255, 255, 255, 255))

        frame.alpha_composite(capa)
        return frame.convert("RGB")


# ------------------------------------------------------------------ audio
def ffmpeg(*args, capturar=False):
    cmd = ["ffmpeg", "-hide_banner", "-y"] + list(args)
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        sys.exit("Error de ffmpeg:\n" + r.stderr[-2000:])
    return r.stderr if capturar else None


def mezclar_audio(carpeta, duracion, destino):
    """Voz + música con ducking, normalizada a -14 LUFS / -1 dBTP en dos pasadas."""
    voz = os.path.join(carpeta, "02_audio", "locucion.wav")
    if not os.path.exists(voz):  # p. ej. la voz generada con ElevenLabs por MCP suele ser .mp3
        voz = os.path.join(carpeta, "02_audio", "locucion.mp3")
    mus = os.path.join(carpeta, "02_audio", "musica.mp3")
    hay_voz, hay_mus = os.path.exists(voz), os.path.exists(mus)
    if not hay_voz and not hay_mus:
        ffmpeg("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "%.2f" % duracion, "-c:a", "pcm_s16le", destino)
        return False
    entradas, filtro = [], ""
    if hay_voz and hay_mus:
        entradas = ["-i", voz, "-stream_loop", "-1", "-i", mus]
        # música unos 18 dB por debajo de la voz (aprox. -20/-24 LUFS en la mezcla) y ducking mientras hay voz
        filtro = ("[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v1][v2];"
                  "[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-18dB[m];"
                  "[m][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];"
                  "[v2][md]amix=inputs=2:duration=first:normalize=0[mix]")
    elif hay_voz:
        entradas = ["-i", voz]
        filtro = "[0:a]aresample=48000,aformat=channel_layouts=stereo[mix]"
    else:
        entradas = ["-stream_loop", "-1", "-i", mus]
        filtro = "[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB[mix]"
    previo = destino + ".premix.wav"
    filtro += ";[mix]apad[completo]"
    ffmpeg(*entradas, "-filter_complex", filtro, "-map", "[completo]", "-t", "%.2f" % duracion, previo)
    # loudnorm: 1.ª pasada para medir, 2.ª para aplicar los valores medidos
    log = ffmpeg("-i", previo, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-", capturar=True)
    m = json.loads(log[log.rfind("{"):log.rfind("}") + 1])
    af = ("loudnorm=I=-14:TP=-1:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:"
          "measured_thresh={input_thresh}:offset={target_offset}:linear=true").format(**m)
    ffmpeg("-i", previo, "-af", af + ",aresample=48000", destino)
    os.remove(previo)
    return True


def medir_lufs(video):
    log = ffmpeg("-i", video, "-af", "ebur128", "-f", "null", "-", capturar=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    return float(m[-1]) if m else None


# ------------------------------------------------------------------ principal
def main():
    ap = argparse.ArgumentParser(description="Monta un reel o un vídeo de YouTube a partir de escenas.json")
    ap.add_argument("--formato", choices=FORMATOS, required=True)
    ap.add_argument("--entrada", required=True, help="carpeta del vídeo")
    ap.add_argument("--salida", required=True, help="archivo .mp4 de salida")
    ap.add_argument("--fuente", help="ruta a una tipografía .ttf")
    ap.add_argument("--escala", type=float, default=1.0, help="0.5 = vista previa a media resolución")
    ap.add_argument("--color-principal", default=COLOR_PRINCIPAL)
    ap.add_argument("--color-acento", default=COLOR_ACENTO)
    a = ap.parse_args()

    if not math.isfinite(a.escala) or not 0.1 <= a.escala <= 1.0:
        ap.error("--escala debe estar entre 0.1 y 1.0.")
    if os.path.exists(a.salida):
        ap.error("La salida ya existe; elige otro nombre para no sobrescribirla.")

    if not shutil.which("ffmpeg"):
        sys.exit("No se encuentra ffmpeg. Instálalo y vuelve a intentarlo.")
    ruta_json = os.path.join(a.entrada, "03_visual", "escenas.json")
    if not os.path.exists(ruta_json):
        sys.exit("Falta %s (usa templates/escenas_ejemplo.json como base)." % ruta_json)
    datos = json.load(open(ruta_json, encoding="utf-8"))
    escenas = datos["escenas"] if isinstance(datos, dict) else datos
    if not isinstance(escenas, list) or not escenas:
        ap.error("escenas.json debe contener una lista de escenas no vacía.")
    for escena in escenas:
        if not isinstance(escena, dict) or any(
            not isinstance(escena.get(k), (int, float)) or isinstance(escena.get(k), bool)
            or not math.isfinite(escena[k]) for k in ("inicio", "fin")
        ):
            ap.error("Cada escena necesita inicio y fin numéricos y finitos.")
        if escena["inicio"] < 0 or escena["fin"] <= escena["inicio"]:
            ap.error("Cada escena debe tener 0 <= inicio < fin.")
        if escena.get("clip"):
            ap.error("Este montador de ejemplo admite imágenes, no clips de vídeo.")
    escenas = sorted(escenas, key=lambda e: e["inicio"])
    esperado = 0.0
    for escena in escenas:
        if not math.isclose(escena["inicio"], esperado, abs_tol=0.001):
            ap.error("Las escenas deben empezar en 0 y ser consecutivas, sin huecos ni solapamientos.")
        esperado = escena["fin"]
    duracion = escenas[-1]["fin"]
    subtitulos = leer_srt(os.path.join(a.entrada, "01_guion", "subtitulos.srt"))

    mont = Montador(a.formato, a.entrada, a.fuente, a.escala, a.color_principal, a.color_acento)
    tmp = tempfile.mkdtemp(prefix="montaje_")
    video_mudo = os.path.join(tmp, "video.mp4")
    audio = os.path.join(tmp, "audio.wav")

    # Fotogramas por tubería a ffmpeg (sin guardar miles de PNG)
    proc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (mont.W, mont.H), "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", video_mudo],
                            stdin=subprocess.PIPE)
    n = int(round(duracion * FPS))
    idx = 0
    for i in range(n):
        t = i / FPS
        while idx < len(escenas) - 1 and t >= escenas[idx]["fin"]:
            idx += 1
        img = mont.fotograma(escenas[idx], t, subtitulos)
        # Solo fundido de salida: el gancho debe verse desde el primer fotograma.
        g = min(1.0, (duracion - t) / 0.5)
        arr = np.asarray(img, dtype=np.uint8)
        if g < 1.0:
            arr = (arr.astype(np.float32) * max(0.0, g)).astype(np.uint8)
        proc.stdin.write(arr.tobytes())
        if i % FPS == 0:
            print("\rRenderizando %d/%d s" % (i // FPS, int(duracion)), end="", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg no pudo codificar el vídeo.")
    print()

    con_audio = mezclar_audio(a.entrada, duracion, audio)
    ffmpeg("-i", video_mudo, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", a.salida)
    shutil.rmtree(tmp, ignore_errors=True)

    print("Vídeo listo: %s (%dx%d, %d fps, %.1f s)" % (a.salida, mont.W, mont.H, FPS, duracion))
    if con_audio:
        lufs = medir_lufs(a.salida)
        print("Sonoridad integrada medida: %s LUFS (objetivo: -14)" % (lufs if lufs is not None else "?"))
    else:
        print("Sin locución ni música: se ha añadido una pista de audio en silencio.")


if __name__ == "__main__":
    main()
