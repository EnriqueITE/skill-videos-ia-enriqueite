# videos-ia-enriqueite · Skill de creación de vídeos de EnriqueITE

Skill para crear vídeos con IA sobre cualquier temática. Autor: EnriqueITE.

Una **skill** es una carpeta con un archivo `SKILL.md` (instrucciones), plantillas y scripts que tu
asistente de IA lee cuando los necesita. Con esta skill instalada no hace falta copiar y pegar prompts:
tu agente ya conoce el método completo para producir **reels 9:16** y **vídeos de YouTube 16:9**
sobre tu temática: cocina, finanzas personales, fitness, viajes, educación o lo que hagas.

Está preparada para agentes compatibles con `SKILL.md`, como **Claude Code**, **Codex** y **Cursor**.
La instalación y las herramientas disponibles dependen de cada agente y de su versión.

## Qué hace

1. Ideas con fuente original y puntuación.
2. Verificación de cada dato en su fuente primaria.
3. Ganchos de 2-3 segundos.
4. Guion no lineal con tiempos (y pausa para que lo apruebes).
5. Escenas con tiempos, iconos y animación, más `escenas.json`.
6. Prompts de imagen y clips 3D sin texto.
7. Voz: tu grabación o ElevenLabs conectado por MCP (voz de la biblioteca o tu voz clonada).
8. Montaje automático con Python (PIL, numpy y ffmpeg).
9. Portada, copy y hashtags.
10. Revisión de políticas de TikTok, Instagram y YouTube con veredicto.

## Contenido

```
videos-ia-enriqueite/
├── SKILL.md                     el método paso a paso (lo que lee el agente)
├── README.md                    este archivo
├── templates/
│   ├── guion_reel.md            guion de reel 25-35 s
│   ├── guion_youtube.md         guion de YouTube 2-3 min
│   ├── escenas_plantilla.md     escenas con tiempos
│   ├── escenas_ejemplo.json     formato que lee el script de montaje
│   ├── checklist_publicacion.md checklist antes de publicar
│   └── perfil_creador.md        tu perfil (temática, público, colores, cierre, voz)
├── prompts/                     los 15 prompts completos del método + índice
└── scripts/
    ├── montar_video.py          montaje de ejemplo (PIL + numpy + ffmpeg)
    └── nuevo_video.py           crea la carpeta de un vídeo nuevo
```

## Instalación

La forma más sencilla: copia el enlace de la skill y pégaselo a tu asistente:

> Instala esta skill: https://github.com/EnriqueITE/skill-videos-ia-enriqueite

Después, pídele un vídeo: "Hazme un reel sobre [TEMA] usando la skill de creación de vídeos de EnriqueITE."

Instalación manual (si prefieres hacerlo tú):

```bash
# 1. Clona el repositorio
git clone https://github.com/EnriqueITE/skill-videos-ia-enriqueite.git

# 2. Copia la skill en la carpeta de skills de tu agente
cp -r skill-videos-ia-enriqueite/videos-ia-enriqueite "[RUTA DE SKILLS DE TU AGENTE]/videos-ia-enriqueite"

# 3. Para actualizarla más adelante
cd skill-videos-ia-enriqueite && git pull
```

Cada agente guarda las skills en una carpeta distinta (a nivel de usuario o de proyecto).
Consulta la documentación de tu herramienta para saber cuál es `[RUTA DE SKILLS DE TU AGENTE]`.
Después, abre una sesión nueva del agente para que detecte la skill.
Tras `git pull`, vuelve a copiar la carpeta de la skill: la copia instalada no se actualiza sola.

Requisitos para el montaje: Python 3.10 o posterior, Pillow, numpy y ffmpeg con libx264.
Desde la carpeta `videos-ia-enriqueite`, instala las dependencias en tu entorno Python:

```bash
python -m pip install -r requirements.txt
```

FFmpeg se instala por separado y debe estar en el PATH; compruébalo con `ffmpeg -version`.

## Voz (opcional): ElevenLabs por MCP

**Publicidad · Enlace de afiliado:** EnriqueITE es afiliado independiente de
ElevenLabs y puede recibir una comisión si contratas una suscripción de pago
mediante este enlace: [Conocer ElevenLabs](https://try.elevenlabs.io/enriqueite-pdf-videos-ia).
Usarlo es voluntario; también puedes grabar tu propia voz. Consulta los precios
y las condiciones vigentes antes de contratar. [Información sobre afiliación y marcas](AFILIACION.md).

1. Crea una cuenta en ElevenLabs y copia tu API key.
2. Conecta el servidor MCP de ElevenLabs a tu asistente (Claude, Grok, Codex, Cursor...) siguiendo su documentación.
   La API key se guarda en la configuración del MCP, nunca en esta carpeta.
3. Elige una voz de la biblioteca o clona la tuya, y anota su nombre o ID en `perfil.md`.
4. Pide: "Ponle voz a este guion y monta el reel." La skill genera `02_audio/locucion.mp3` con tus créditos.

Sin MCP, la skill también puede usar la variable de entorno `ELEVENLABS_API_KEY` si ya la tienes definida.
Si no usas ElevenLabs, graba tu voz y guarda el archivo como `02_audio/locucion.wav`.

## Uso

Pídelo con tus palabras. Ejemplos:

- "Hazme un reel sobre [TEMA] usando la skill de creación de vídeos de EnriqueITE."
- "Hazme un vídeo de YouTube de 3 minutos sobre [TEMA] con estas fuentes: [ENLACES]."
- "Dame 3 ideas de vídeo para esta semana sobre [TU TEMÁTICA]."
- "Verifica estos datos antes de grabar: [DATOS]."
- "Convierte este reel en un vídeo de YouTube de 3 minutos."
- "Divide este guion en escenas y genera el escenas.json."
- "Ponle voz con ElevenLabs y monta el vídeo de la carpeta [CARPETA]."
- "Revisa este guion contra las políticas de TikTok."

La skill trabaja por pasos y **se detiene para que apruebes el guion** antes de producir escenas,
imágenes, voz y montaje.

Montaje directo, sin agente:

Ejecuta estos comandos desde la carpeta `videos-ia-enriqueite` que contiene `scripts/`.
Sustituye `AAAA-MM-DD` por la fecha de la carpeta que imprime el primer comando.

```bash
python3 scripts/nuevo_video.py --tema mi-tema --formato reel --raiz ./videos
python3 scripts/montar_video.py --formato reel --entrada ./videos/AAAA-MM-DD_mi-tema_reel --salida final.mp4
# vista previa rápida a media resolución
python3 scripts/montar_video.py --formato reel --entrada ./videos/AAAA-MM-DD_mi-tema_reel --salida prueba.mp4 --escala 0.5
```

## Personalización

- Rellena `templates/perfil_creador.md` y guárdalo como `perfil.md` en tu carpeta de vídeos.
- Usa tus colores con `--color-principal` y `--color-acento` (o cambia los valores por defecto en `scripts/montar_video.py`).
- El montador parte de una paleta neutra de blancos y grises, independiente de la marca de EnriqueITE. El asistente puede leer el código como referencia y adaptarlo a tu perfil; los fondos de respaldo se ajustan en `COLOR_FONDO_REEL` y `COLOR_FONDO_YT`.
- Las reglas de `SKILL.md` son **buenas prácticas por defecto**: gancho de 2-3 s, fuentes en pantalla,
  no nombrar personas, datos personales tapados y sin promesas exageradas. Ajústalas a tu canal en tu perfil.

## Privacidad y seguridad

- La skill no contiene claves de API, contraseñas ni tokens. No los guardes en esta carpeta.
- No publica nada por sí misma: la publicación la haces tú.
- La voz generada consume créditos de tu cuenta de ElevenLabs.
- Las normas de las plataformas y los precios de servicios son orientativos; revisa siempre la versión vigente.

## Alcance del montador de ejemplo

Anima imágenes y textos, añade iconos y subtítulos SRT existentes y mezcla audio.
No genera imágenes, voz, subtítulos automáticos ni escenas 3D; esas tareas requieren
el asistente y las herramientas correspondientes. No inserta clips de vídeo.
El campo `animacion` del ejemplo describe la intención visual: el script aplica
sus animaciones predefinidas, no interpreta diferentes efectos por nombre.
El JSON incluido es una demostración de 17 segundos con marcadores por rellenar.
Revisa el contenido y ajusta los tiempos antes de producir un vídeo real.

## Licencia y autoría

Copyright (c) 2026 Enrique Serrano Aparicio (EnriqueITE).
Este paquete se distribuye bajo **GNU GPL versión 3 únicamente (`GPL-3.0-only`)**;
consulta [LICENSE](LICENSE). Puedes usarlo, modificarlo y redistribuirlo, incluso
comercialmente. Si distribuyes una versión derivada, debes cumplir GPLv3,
conservar los avisos, identificar los cambios y facilitar el código fuente correspondiente.

Usar la herramienta no hace que tus vídeos sean automáticamente GPL. Los materiales
que incorpores y el contenido protegido que reproduzcas conservan sus propias condiciones.
No se garantiza un resultado, alcance o aceptación por las plataformas.
Una versión modificada no debe presentarse como una versión oficial de EnriqueITE.
