# Prompt 06 · Imágenes y clips 3D por escena

**Cuándo usarlo:** Paso 6. Para generar fondos e imágenes o clips 3D sin texto por escena.

**Herramienta recomendada:** Claude o ChatGPT para escribir los prompts; tu generador de imagen y vídeo preferido para ejecutarlos.

```text
Actúa como director de arte 3D y escribe prompts para mis generadores de imagen ([HERRAMIENTA DE IMAGEN]) y de vídeo ([HERRAMIENTA DE VÍDEO]).

Escenas:
[PEGA LA TABLA DE ESCENAS]
Formato: [16:9 | 9:16]
Paleta: [COLOR PRINCIPAL], [COLOR SECUNDARIO], acentos [COLOR DE ACENTO].
Estilo: "mundo diseñado" 3D sobre [TU TEMÁTICA], limpio y tipo maqueta, iluminación volumétrica suave, materiales mate y vidrio, profundidad de campo ligera.

Para cada escena escribe:
1. PROMPT DE IMAGEN en inglés (40-70 palabras): sujeto, entorno, composición, luz, lente y estilo.
2. PROMPT DE VÍDEO en inglés (25-45 palabras): un movimiento de cámara concreto (dolly in, orbit, fly-through, crane up), duración de [4-6] s y velocidad lenta y constante.
3. NEGATIVE PROMPT: text, letters, words, numbers, logos, watermark, people, faces, hands, brand names, readable UI.
4. Nota de continuidad con la escena anterior (objetos y colores que se repiten).

Reglas: ninguna imagen contiene texto, logos ni personas; el texto se añade después en edición. Mantén el mismo estilo y la misma luz en todas las escenas.
```

**Qué esperar:** Por cada escena, un prompt de imagen, uno de vídeo, un negative prompt y una nota de continuidad.

**Si sale mal:** Si las imágenes salen con letras inventadas o carteles: refuerza el negative prompt y añade "clean surfaces, no signage". Si cambian de estilo: "Usa la imagen de la escena 1 como referencia de estilo para todas".
