# Prompt 05 · Dividir en escenas con tiempos, animación e iconos

**Cuándo usarlo:** Paso 5. Con el guion aprobado, para dividirlo en escenas con tiempos.

**Herramienta recomendada:** **Claude** o ChatGPT.

```text
Actúa como director de motion graphics para vídeos sobre [TU TEMÁTICA].

Guion aprobado (con tiempos):
[PEGA LA TABLA DEL GUION]
Formato: [REEL 1080x1920 | YOUTUBE 1920x1080]. Duración total: [SEGUNDOS] s.
Estilo: [REEL: fondo limpio, iconos planos con acentos [COLOR DE ACENTO] y [COLOR PRINCIPAL] | YOUTUBE: mundo 3D diseñado relacionado con el tema, objetos 3D, vuelos de cámara].

Divide el vídeo en escenas de [1,5-4 s (reel) | 4-8 s (YouTube)]. Para cada escena indica:
1. Número y tiempo de inicio-fin (formato 00:00.0).
2. Frase de locución que cubre.
3. Texto en pantalla (máx. 6 palabras). El gancho permanece visible desde 00:00.0 hasta al menos 00:02.5.
4. Iconos concretos (2-4), p. ej. "lupa", "reloj", "gráfico".
5. Si aparece una app o una lista de opciones: tarjeta grande con 4-5 opciones y la correcta resaltada.
6. Animación: entrada, movimiento continuo y salida. Ningún elemento puede quedar estático más de 0,7 s (usa escalados del 2-4 %, desplazamientos o pulsos).
7. Transición a la escena siguiente.
8. Cita de fuente en pantalla si la escena contiene un dato.

Reglas: datos personales siempre tapados; sin logos de marcas ni personas reales.
Entrega una tabla y, al final, la lista única de iconos y el archivo escenas.json con los campos: inicio, fin, texto_pantalla, iconos, animacion, fuente.
```

**Qué esperar:** Una tabla de 8-12 escenas (reel) o 20-30 (YouTube), la lista de iconos y un escenas.json listo para el script de montaje.

**Si sale mal:** Si hay escenas sin movimiento o con demasiados elementos: "Revisa cada escena: máximo 4 iconos y ningún elemento quieto más de 0,7 s. Corrige la tabla y el JSON".
