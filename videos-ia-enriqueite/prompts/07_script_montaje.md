# Prompt 07 · Script de montaje en Python (Claude Code o Codex)

**Cuándo usarlo:** Paso 8. Para que un agente de código escriba el script de montaje (ver también scripts/montar_video.py).

**Herramienta recomendada:** **Claude Code** o **Codex**, trabajando dentro de la carpeta del proyecto.

```text
Actúa como ingeniero de vídeo en Python. Escribe un script completo, ejecutable y comentado en español: montar_video.py.

Entradas (carpeta del proyecto [RUTA]):
- 03_visual/escenas.json: lista de escenas con "inicio", "fin", "imagen" o "clip", "texto_pantalla", "iconos", "animacion" y "fuente".
- 02_audio/locucion.wav o locucion.mp3 (grabada o generada con ElevenLabs) y 02_audio/musica.mp3
- 01_guion/subtitulos.srt (si no existe, genéralo a partir de escenas.json)
- assets/iconos/*.png y assets/fuentes/[FUENTE].ttf

Requisitos:
1. Solo Python 3, Pillow, numpy y ffmpeg (vía subprocess). Sin otras dependencias.
2. Resolución [1080x1920 | 1920x1080], 30 fps, H.264 yuv420p, audio AAC 192 kbps.
3. Fotogramas con PIL: fondo [blanco | imagen o clip de la escena], iconos con entrada (escala 0,8→1 y opacidad en 0,3 s) y micro-movimiento continuo para que nada quede estático más de 0,7 s.
4. Texto en pantalla grande dentro de la zona segura (8 % lateral, 15 % inferior). El gancho visible desde 0 s hasta [2,8] s.
5. Subtítulos quemados: máximo 2 líneas y 32 caracteres por línea, texto [COLOR DE TEXTO] sobre caja [COLOR SECUNDARIO] al 85 %, palabra clave en [COLOR DE ACENTO].
6. Cita de fuente en la parte inferior cuando la escena tenga "fuente".
7. Audio: música entre -20 y -24 LUFS bajo la voz, con ducking (sidechaincompress) durante la locución; mezcla final a -14 LUFS integrados y -1 dBTP con loudnorm en dos pasadas.
8. Fundido de entrada de 0,2 s y de salida de 0,5 s.
9. Argumentos: --formato reel|youtube --entrada [RUTA] --salida [ARCHIVO.mp4].
10. Envía los fotogramas por tubería a ffmpeg (stdin) en lugar de guardar miles de PNG.
11. Al final, mide la sonoridad con el filtro ebur128 e imprime el valor integrado.

Entrega: el script completo en un único bloque, un escenas.json de ejemplo con 3 escenas y el comando exacto para ejecutarlo.
```

**Qué esperar:** Un script que genera 04_video/final.mp4 y muestra al final la sonoridad medida (cerca de -14 LUFS).

**Si sale mal:** Pega el error completo de la terminal y escribe: "Corrige este error sin añadir dependencias nuevas". Si el vídeo va lento o se ve entrecortado: "Optimiza el renderizado precalculando los fondos y reutilizando capas".
