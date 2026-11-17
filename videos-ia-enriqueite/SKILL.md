---
name: videos-ia-enriqueite
license: GPL-3.0-only
description: Crea reels, shorts y vídeos de YouTube con el método de EnriqueITE. Úsala para preparar ideas, fuentes, guiones, escenas, locución, montaje local con Python y FFmpeg, portadas o revisión previa a publicar, y cuando se solicite esta skill.
---

# videos-ia-enriqueite · Skill de creación de vídeos de EnriqueITE

De la idea al vídeo publicado, sobre cualquier temática.

Esta skill guía la producción de un vídeo sobre la temática de la persona en 10 pasos.
La IA propone; la persona decide y verifica. Trabaja siempre por pasos y **detente
para pedir aprobación del guion antes de producir escenas, imágenes, voz o montaje**.

Archivos de apoyo (léelos solo cuando el paso los necesite):

| Carpeta | Contenido |
|---|---|
| `prompts/` | Los 15 prompts completos del método (índice en `prompts/README.md`). |
| `templates/` | Guion de reel, guion de YouTube, escenas con tiempos, `escenas_ejemplo.json`, checklist de publicación y perfil de creador. |
| `scripts/` | `montar_video.py` (montaje con PIL, numpy y ffmpeg) y `nuevo_video.py` (crea la carpeta de un vídeo). |

## Paso 0 · Contexto del creador

1. Busca un perfil de creador en el proyecto (por ejemplo `perfil.md` en la raíz de la carpeta de vídeos).
   Si no existe, pide en una sola pregunta: temática, público, idioma y país, formatos, colores de marca y frase de cierre.
   Ofrece guardar las respuestas con `templates/perfil_creador.md`.
2. Aplica siempre los datos del perfil: `[TU TEMÁTICA]`, `[TU AUDIENCIA]`, `[TUS COLORES]`, `[TU CIERRE]` y las preferencias de estilo.
   Si falta algún dato, usa los valores por defecto de esta skill y dilo.
3. Determina el formato: **reel 9:16 de 25-35 s** o **YouTube 16:9 de 2-3 min**. Si no se indica, propone reel.
4. Si la persona solo pide una parte (por ejemplo "revisa este guion"), salta directamente al paso que corresponda.

## Paso 1 · Ideas (`prompts/01_ideas_del_dia.md`)

- Busca novedades, tendencias, preguntas frecuentes o datos poco conocidos de `[TU TEMÁTICA]` en fuentes fiables:
  organismos oficiales y estadísticas públicas, webs oficiales de marcas o instituciones, estudios con metodología
  y expertos reconocidos del sector. Los medios y las redes sirven para descubrir, no como fuente final.
- Si no tienes acceso a la web, dilo y pide a la persona los enlaces o el texto. **No inventes enlaces, cifras ni citas.**
- Propón 3 ideas con: titular neutro, gancho, dato clave, fuente original con fecha, estado y puntuación.
- Puntúa de 1 a 5: impacto, verificabilidad, potencial visual y novedad. Recomienda grabar solo con 14/20 o más.
- Descarta rumores, historias centradas en una persona, temas políticos y promesas que no se pueden demostrar.

## Paso 2 · Verificación (`prompts/04_verificacion.md`)

Para cada afirmación: (1) ve a la fuente primaria, (2) copia la frase literal con enlace y fecha,
(3) contrasta con una segunda fuente independiente, (4) reformula sin exagerar ni redondear al alza.
Estados: `CONFIRMADO` (2+ fuentes), `SIN CONFIRMAR` (1 fuente: se dice en la locución y se muestra en pantalla),
`INEXACTO` (propón la redacción correcta), `NO ENCONTRADO` (fuera del guion).
Prepara el texto de pantalla: `Fuente: [organización], [mes año]`.
Si la temática toca salud, dinero o derecho, añade un aviso breve: "Consulta a un profesional".

## Paso 3 · Gancho (`prompts/02_ganchos.md`)

Propón 5-10 ganchos de máximo 8 palabras, universales (sin excluir por dispositivo, edad, profesión o nivel)
y que abran una pregunta que el vídeo responde después. Fórmulas: contradicción, detalle oculto, consecuencia, reto,
utilidad, lista. Marca los 3 más fuertes y recomienda uno.

## Paso 4 · Guion no lineal (`prompts/03_guion_no_lineal.md`, plantillas en `templates/`)

Estructura: **gancho → contexto → dato verificado con fuente → giro → consejo práctico → cierre**.

| Bloque | Reel | YouTube |
|---|---|---|
| Gancho | 0-3 s | 0-5 s |
| Contexto | 3-8 s | 5-30 s |
| Dato | 8-14 s | 30-60 s |
| Giro | 14-20 s | 60-110 s |
| Consejo | 20-28 s | 110-160 s |
| Cierre | 28-32 s | 160-175 s |

- Longitud a 150-165 palabras por minuto: reel 70-90 palabras; YouTube 330-450.
- Bucle abierto: en reels, un recordatorio antes del giro; en YouTube, cada 30-40 s.
- Cierre: `[TU CIERRE]` del perfil, siempre igual.
- Entrega una tabla `Bloque | Tiempo | Locución | Texto en pantalla (máx. 6 palabras)` y el recuento de palabras.
- **PAUSA OBLIGATORIA:** muestra el guion y espera la aprobación antes de seguir.

## Paso 5 · Escenas (`prompts/05_escenas.md`, `templates/escenas_plantilla.md`)

- Reel: escenas de 1,5-4 s, fondo limpio, 2-4 iconos por escena, apps o listas como tarjetas grandes con 4-5 opciones.
- YouTube: escenas de 4-8 s, "mundo diseñado" en 3D con vuelos de cámara lentos.
- Ningún elemento estático más de 0,7 s (entrada, micro-movimiento del 2-4 %, salida).
- Gancho visible desde 0,0 s hasta al menos 2,5 s. Zona segura en vertical: 8 % lateral, 15 % inferior, 10 % superior.
- Usa `[TUS COLORES]` del perfil. Genera `escenas.json` con el formato de `templates/escenas_ejemplo.json`.

## Paso 6 · Imágenes y clips 3D (`prompts/06_imagenes_3d.md`)

Por escena: prompt de imagen (40-70 palabras, en inglés), prompt de vídeo con un movimiento de cámara concreto,
negative prompt (`text, letters, words, numbers, logos, watermark, people, faces, hands, brand names, readable UI`)
y nota de continuidad. Las imágenes no llevan texto: el texto se añade en el montaje.

## Paso 7 · Voz (`prompts/08_locucion.md`)

- Opciones: voz grabada por la persona, o voz generada con ElevenLabs (una voz de su biblioteca o la voz clonada
  de la propia persona). Voces de terceros **solo** con consentimiento escrito.
- **Recomendado: ElevenLabs conectado por MCP.** Si el asistente tiene disponible el servidor MCP de ElevenLabs
  (configurado por la persona con su API key), genera la locución con la voz `[ID O NOMBRE DE LA VOZ]` del perfil,
  bloque a bloque, y guárdala como `02_audio/locucion.mp3`. Esto consume créditos de la cuenta de la persona:
  avisa antes de generar y no regeneres sin necesidad.
- Alternativa sin MCP: si la variable de entorno `ELEVENLABS_API_KEY` ya está definida, puedes usar la API de
  ElevenLabs con ella. Nunca pidas que pegue la clave en el chat, nunca la imprimas ni la guardes en archivos.
- Si no hay MCP ni clave, entrega el texto de locución y la tabla de grabación para que la persona grabe su voz.
- Etiquetas de tono: como máximo una por frase (`[curious]`, `[short pause]`, `[serious tone]`, `[warm]`), según lo que admita el modelo.
- Niveles: música entre -20 y -24 LUFS con ducking; mezcla final a -14 LUFS integrados y -1 dBTP.

## Paso 8 · Montaje (`scripts/montar_video.py`, `prompts/07_script_montaje.md`)

1. Resuelve `scripts/` y `templates/` respecto a la carpeta de esta skill. Crea el proyecto fuera de la skill instalada con `python scripts/nuevo_video.py --tema [tema] --formato reel --raiz [CARPETA DE VIDEOS]` usando la ruta del script resuelta.
2. Coloca `escenas.json`, imágenes, `locucion.wav` o `locucion.mp3` y `musica.mp3` donde indica el script.
3. Ejecuta: `python3 scripts/montar_video.py --formato reel --entrada [CARPETA] --salida final.mp4 --color-principal [#HEX] --color-acento [#HEX]`.
4. Requisitos: Python 3.10 o posterior, Pillow, numpy y ffmpeg; consulta `requirements.txt`. Si falta algo, pide a la persona que lo instale; no lo instales sin permiso.
5. Si el script falla, lee el error, corrige sin añadir dependencias nuevas y vuelve a ejecutar.
6. El montador incluido anima imágenes, texto e iconos; no inserta clips, genera voz ni crea subtítulos automáticamente. El campo `animacion` no selecciona efectos distintos. Si necesitas esas funciones, adapta el montaje antes de prometerlas.

## Paso 9 · Portada y copy (`prompts/09_portada_copy.md`)

- Portada .jpg (1080x1920 reel, 1280x720 YouTube): 2-4 palabras, una destacada en el color de acento, un objeto grande, contraste alto, texto centrado (el perfil recorta a 3:4).
- Copy: una frase de hasta 20 palabras que complete el gancho sin repetirlo, y 3 hashtags (amplio, nicho y tema).

## Paso 10 · Revisión de políticas (`prompts/10_revision_politicas.md`)

Revisa voz, subtítulos, textos en pantalla, portada, copy y hashtags. Devuelve una tabla
`Problema | Dónde | Riesgo | Corrección` y un veredicto: `LISTO PARA PUBLICAR` o `CORREGIR ANTES DE PUBLICAR`.
Las normas de las plataformas cambian: recomienda revisar su página oficial y no afirmes reglas que no puedas comprobar.

## Entrega final

Entrega el paquete en este orden: guion final, `escenas.json`, prompts de imagen y vídeo, locución (texto y archivo si se generó),
comando de montaje, portada (texto + prompt), copy y hashtags, informe de revisión y la checklist de
`templates/checklist_publicacion.md` marcada.

## Buenas prácticas por defecto (el perfil del creador manda)

- **Gancho de 2-3 s**, dicho y escrito en pantalla desde el primer fotograma.
- **Fuentes en pantalla**: `Fuente: [organización], [mes año]`, visible mientras se oye el dato.
- **No nombrar personas** ni señalar culpables: contar hechos. Sin nombres de usuario, rostros ni datos personales en capturas.
- **Datos personales tapados** (matrículas, direcciones, correos, teléfonos) desde el primer fotograma.
- **Sin promesas** de salud, dinero o resultados garantizados; evita palabras que las plataformas suelen limitar.
- **Etiqueta de contenido con IA** cuando haya voz clonada o escenas realistas.
- Tono claro y cercano, en segunda persona; frases de máximo 15 palabras; sin sensacionalismo ni política.
- Cierre constante: `[TU CIERRE]`.
- Precios de servicios siempre marcados como orientativos.

## Qué no hacer

- No publiques ni subas nada en nombre de la persona.
- No inventes fuentes, cifras, citas ni enlaces.
- No pidas, muestres ni guardes claves de API, contraseñas o tokens: la persona los configura en el MCP o en variables de entorno.
- No generes voz con ElevenLabs sin avisar de que consume créditos de su cuenta.
