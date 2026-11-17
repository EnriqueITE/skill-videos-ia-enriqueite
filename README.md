![Crea vídeos con IA · EnriqueITE. De la idea al vídeo.](assets/social-preview.jpg)

# Crea vídeos con IA · EnriqueITE

Una skill en español para convertir una idea en un guion, escenas y un vídeo para
**Reels, Shorts y YouTube**, con fuentes verificadas y aprobación del guion antes de producir.

**Autor:** [Enrique Serrano Aparicio · EnriqueITE](https://github.com/EnriqueITE)  
**Licencia:** [GPLv3](LICENSE) · `GPL-3.0-only`

[🚀 Instalar la skill](#empieza-aquí) · [📚 Ver los prompts](videos-ia-enriqueite/prompts/README.md) · [☕ Invítame a un café](https://buymeacoffee.com/enriqueite)

**💡 Idea → 🔎 Fuentes → ✍️ Guion → 🎬 Escenas → 🎙️ Voz → ▶️ Vídeo**

## Empieza aquí

Pega esto en un agente que pueda instalar skills desde GitHub:

```text
Instala la skill videos-ia-enriqueite de este repositorio:
https://github.com/EnriqueITE/skill-videos-ia-enriqueite
La carpeta que debes instalar es videos-ia-enriqueite; contiene SKILL.md.
```

Después:

```text
Hazme un reel sobre [TEMA] usando la skill de creación de vídeos de EnriqueITE.
```

Cuéntale tu temática, público, idioma y colores. El asistente propone ideas,
comprueba fuentes y prepara el guion. **Tú apruebas el guion antes de continuar.**

Está preparada para agentes compatibles con `SKILL.md`, como Claude Code, Codex
y Cursor. La detección, instalación, búsqueda web y ejecución de herramientas
dependen del agente y de su versión. Un chat sin acceso a archivos o herramientas
puede ayudarte con los textos, pero no ejecutar el montaje local.

## Qué incluye

| Recurso | Para qué sirve |
|---|---|
| [Skill](videos-ia-enriqueite/SKILL.md) | Método de producción paso a paso |
| [15 prompts](videos-ia-enriqueite/prompts/README.md) | Ideas, ganchos, verificación, guion, escenas, voz y publicación |
| [Plantillas](videos-ia-enriqueite/templates/) | Perfil, guiones, escenas y checklist |
| [Scripts Python](videos-ia-enriqueite/scripts/) | Crear un proyecto y montar imágenes, textos, iconos, subtítulos y audio |
| [Guía de uso](videos-ia-enriqueite/README.md) | Instalación, personalización, voz y comandos |

El tutorial PDF se comparte por separado y no forma parte de este repositorio.

## Instalación manual

Descarga el ZIP desde **Code → Download ZIP**, o clona el repositorio:

```bash
git clone https://github.com/EnriqueITE/skill-videos-ia-enriqueite.git
```

Copia **solo la carpeta `videos-ia-enriqueite`**, con todo su contenido, dentro
del directorio de skills que utilice tu agente. La estructura final debe ser:

```text
[directorio de skills]/videos-ia-enriqueite/SKILL.md
```

Conserva `LICENSE` al copiar o redistribuir el paquete. Abre una nueva sesión del
agente si es necesario. Para actualizar, ejecuta `git pull` en el clon y vuelve
a copiar la carpeta instalada; no guardes tus proyectos personales dentro de ella.

## Montaje local

Requiere **Python 3.10+**, **Pillow**, **numpy** y **FFmpeg con libx264** disponible
en el PATH. Desde la raíz del repositorio:

```bash
python -m venv .venv
```

Activa el entorno con `.venv\Scripts\Activate.ps1` en PowerShell o
`source .venv/bin/activate` en macOS/Linux. Después:

```bash
python -m pip install -r videos-ia-enriqueite/requirements.txt
ffmpeg -version
python videos-ia-enriqueite/scripts/nuevo_video.py --tema mi-primer-video --formato reel --raiz ../mis-videos
```

Edita `03_visual/escenas.json` en la carpeta creada y añade tus recursos. Sustituye
`[CARPETA CREADA]` por la ruta que imprime el comando anterior:

```bash
python videos-ia-enriqueite/scripts/montar_video.py --formato reel --entrada "[CARPETA CREADA]" --salida prueba.mp4 --escala 0.5
```

El ejemplo JSON dura 17 segundos y contiene marcadores por rellenar; no es un
guion final verificado. Los scripts rechazan proyectos o salidas que ya existan
para evitar sobrescribir tu trabajo. El montaje utiliza imágenes, textos, iconos,
SRT existentes y audio; no incorpora clips de vídeo ni crea escenas 3D o voz.
Los prompts permiten preparar esas tareas con herramientas adicionales.

ElevenLabs es **opcional** y utiliza tu cuenta y tus créditos. Puedes grabar tu
propia locución. No se incluyen claves, suscripciones ni un servidor MCP.

**Publicidad · Enlace de afiliado:** EnriqueITE es afiliado independiente de
ElevenLabs y puede recibir una comisión si contratas una suscripción de pago
mediante este enlace: [Conocer ElevenLabs](https://try.elevenlabs.io/enriqueite-pdf-videos-ia).
Usarlo es voluntario y no es necesario para utilizar la skill. Consulta los precios
y las condiciones vigentes del servicio antes de contratar.
[Información sobre afiliación y marcas](videos-ia-enriqueite/AFILIACION.md).

## Licencia, vídeos y versiones derivadas

Copyright (c) 2026 Enrique Serrano Aparicio (EnriqueITE).

El código, las instrucciones, los prompts y las plantillas originales de este
repositorio se ofrecen bajo **GNU GPL versión 3 únicamente**. El texto completo
está en [LICENSE](LICENSE), también incluido en la carpeta instalable.

- Puedes usar, estudiar, modificar y redistribuir la skill, incluso comercialmente.
- Si distribuyes una versión derivada, debes cumplir GPLv3, conservar sus avisos,
  indicar los cambios y facilitar el código fuente correspondiente bajo esa licencia.
- No estás obligado a enviar tus modificaciones a este repositorio.
- Usar el script no convierte automáticamente tus vídeos en obras GPL. Los
  recursos y el contenido protegido que reproduzcas conservan sus condiciones.
- La licencia no concede acceso de escritura a GitHub ni permiso para presentar
  una versión ajena como una publicación oficial de EnriqueITE.

Se ofrece sin garantías, en los términos de la licencia. No garantiza alcance,
monetización ni aprobación de ninguna plataforma. Revisa las fuentes, los derechos
de imágenes, música y voces y las normas vigentes antes de publicar.

## Propuestas y seguridad

Puedes proponer mejoras mediante issues y pull requests desde tu fork. El
mantenedor decide qué se incorpora: una propuesta no se fusiona automáticamente.
Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y [SECURITY.md](SECURITY.md).

Guarda tu perfil, claves y vídeos fuera del repositorio. El `.gitignore` ayuda a
evitar que se añadan por accidente, pero revisa siempre los archivos antes de subirlos.
