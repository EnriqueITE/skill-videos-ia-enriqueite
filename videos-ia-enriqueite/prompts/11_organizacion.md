# Prompt 11 · Estructura del proyecto y calendario

**Cuándo usarlo:** Organización: estructura de carpetas, calendario y rutina.

**Herramienta recomendada:** Claude Code o Codex para el script; Claude o ChatGPT para el calendario.

```text
Actúa como gestor de producción de contenidos.

Mi ritmo: [N] reels y [N] vídeos de YouTube por semana. Días disponibles: [DÍAS]. Tiempo diario: [MINUTOS].
Temas fijos: [TEMAS, p. ej. "receta de la semana, error común, reto busca el fallo"].

1. Genera un script en Python (solo biblioteca estándar) que cree la carpeta de un vídeo nuevo con la estructura: 01_guion, 02_audio, 03_visual, 04_video, 05_portada, con el nombre AAAA-MM-DD_[tema]_[formato], y copie dentro las plantillas de _plantillas.
2. Crea un calendario de [4] semanas en una tabla Markdown: fecha, formato, tipo de vídeo, tema provisional y estado (idea, guion, montaje, publicado).
3. Propón un archivo .gitignore que excluya audio, vídeo y clips pesados.
4. Escribe una rutina diaria con horas y el prompt que corresponde a cada paso.
```

**Qué esperar:** Un script que crea carpetas, un calendario de 4 semanas, un .gitignore y una rutina diaria.

**Si sale mal:** Si el calendario no es realista para tu tiempo: "Reduce la carga a [N] vídeos semanales y prioriza los formatos con mejor resultado".
