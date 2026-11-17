# Prompt 08 · Locución con indicaciones de tono o guion con tiempos

**Cuándo usarlo:** Paso 7. Para preparar la locución (voz propia o voz clonada con permiso).

**Herramienta recomendada:** Claude o ChatGPT para el texto; tu servicio de voz clonada o tu micrófono para grabar.

**Publicidad · Enlace de afiliado:** EnriqueITE es afiliado independiente de
ElevenLabs y puede recibir una comisión si contratas una suscripción de pago
mediante este enlace: [Conocer ElevenLabs](https://try.elevenlabs.io/enriqueite-pdf-videos-ia).
Es voluntario y puedes usar tu propia grabación. [Información sobre afiliación y marcas](../AFILIACION.md).

```text
Actúa como director de locución para vídeos sobre [TU TEMÁTICA].

Guion aprobado:
[PEGA EL GUION]
Modo: [VOZ ELEVENLABS POR MCP | GRABACIÓN CON MI VOZ]
Voz de ElevenLabs (si aplica): [NOMBRE O ID DE LA VOZ]
Duración objetivo: [SEGUNDOS] s (ritmo de 150-165 palabras por minuto).
Cierre: [TU CIERRE]

Si el modo es VOZ ELEVENLABS POR MCP:
- Si me muestras un enlace de afiliado, explica junto a él quién recibe la posible comisión y su relación con el servicio. Para el enlace de este documento, el afiliado es EnriqueITE. No insertes esta promoción en mi locución salvo que te lo pida.
- Reescribe el texto para locución con etiquetas de tono en inglés y minúsculas: [curious], [serious tone], [short pause], [warm], [slower], [emphasis].
- Máximo una etiqueta por frase; [short pause] antes del dato y antes del giro.
- Escribe cifras, siglas y direcciones como se pronuncian (p. ej. "dos mil veintiséis", "punto com").
- Si tienes el MCP de ElevenLabs conectado, avísame de que consume créditos y, cuando lo confirme, genera la voz y guárdala como 02_audio/locucion.mp3.

Si el modo es GRABACIÓN CON MI VOZ:
- Devuelve una tabla: Tiempo | Frase | Intención (curiosidad, seriedad, cercanía) | Palabra a enfatizar | Pausa.
- Marca con / las pausas breves y con // las largas.

En ambos casos: frases de máximo 15 palabras, segunda persona, y termina con el cierre exacto. Indica la duración estimada.
```

**Qué esperar:** Un texto listo para el motor de voz con etiquetas, o una tabla de grabación con tiempos, intención y pausas.

**Si sale mal:** Si la voz suena robótica: "Reduce las etiquetas a la mitad y acorta las frases". Si dura más de lo previsto: "Ajusta a [N] palabras manteniendo el cierre".
