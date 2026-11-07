# Cartas Musicales

Web para jugar con las tarjetas QR de canciones de Spotify.
Muestra la cara del QR para escanearla con el móvil y, con doble toque o el botón **Revelar**,
da la vuelta a la carta y muestra artista, año, mes y título.

Sitio estático, sin servidor: funciona con GitHub Pages o abriendo `index.html` con doble clic.

## Estructura

```
index.html            La página (HTML, CSS y JS)
cards.js              Las cartas (generado, no editar a mano)
vendor/qrcode.min.js  Generador de QR (qrcode-generator 1.4.4)
.nojekyll             Evita que GitHub Pages procese el sitio con Jekyll
```

## Cómo se juega

- Al empezar se eligen el modo, el número de equipos (1–8), sus nombres y las monedas iniciales.
- **Línea temporal** (por defecto, como Hitster): cada equipo empieza con una carta revelada.
  En su turno toca el hueco de su línea donde cree que va la canción y pulsa **Comprobar**
  (o doble toque). Si el año encaja (año igual vale a cualquier lado) se queda la carta;
  si no, se descarta. Gana el primero que llega a las cartas objetivo (10 por defecto).
- **Desafío**: con el hueco elegido y antes de comprobar, otro equipo puede gastar 1 moneda y poner
  su ficha en otro hueco de la misma línea. Si el equipo en turno acierta, el desafío pierde la ficha;
  si falla y la ficha estaba bien, ese equipo roba la carta para su línea. La ficha se gasta siempre;
  tocando de nuevo al equipo antes de comprobar se retira y se recupera la moneda.
- Reglas: máximo 5 monedas por equipo; en línea temporal no se pasa turno sin colocar y comprobar
  la carta (o saltarla con moneda); el desafío solo aparece si algún otro equipo tiene monedas.
- **Libre**: solo turnos y monedas; la línea temporal se juega fuera de la web.
- **Dificultad**:
  - **Fácil**: como normal y, además, **Comprar** (o `C`): el equipo en turno paga 3 monedas y la carta
    va directa a su línea temporal (solo en línea temporal, antes de comprobar y sin desafíos puestos).
  - **Normal**: las reglas de siempre.
  - **Difícil**: no se puede saltar canciones con monedas y, si la carta es del mismo año que otra de
    la línea, el mes decide si va antes o después (si alguna de las dos no tiene mes, vale a cualquier lado).
    Las cartas de la línea muestran el mes.
- **Categorías**: se puede jugar solo con algunos estilos, idiomas o décadas (por defecto, todas).
  Dentro de cada grupo se pueden marcar varias opciones; el mazo se baraja solo con las canciones que cumplen.
- Arriba se muestra el equipo en turno y las monedas de cada equipo.
- Doble toque / doble clic en la carta, botón **Revelar** o `Espacio`: girar la carta.
- **Siguiente** o `→`: siguiente carta y turno del siguiente equipo.
- **Saltar** o `S`: el equipo en turno paga 1 moneda, la carta se revela marcada como saltada
  y **Otra carta** saca una nueva sin pasar el turno.
- Tocando la fila de equipos se suman o restan monedas (aciertos, desafíos) o se empieza otra partida.
- El mazo se baraja sin repeticiones; la partida y el progreso se guardan en el navegador.

## Reproducir la canción sin escanear

En el botón de la pantalla (icono de TV, arriba) se elige qué pasa al pulsar ▶ (o tocar la carta una vez, o OK
sobre la carta con el mando, o `P` / ⏯):

- **Solo QR**: sin botón; se escanea el QR como siempre.
- **Mi app (Android)**: abre la app SpotifyQR con `spqrplayer://play?track=ID`; suena sin mostrar el título y
  vuelve sola al navegador. Solo en el móvil donde está instalada la app.
- **Spotify Connect**: la web manda la canción a cualquier Spotify de la cuenta (app de la TV, móvil, altavoz…)
  con la Web API. Necesita Premium. Opción para jugar en la TV. Se puede hacer que suene sola al sacar cada carta;
  al pasar de carta se para la anterior.

Configuración en [developer.spotify.com](https://developer.spotify.com/dashboard) (una vez), en la app de Spotify
que usa SpotifyQR (Client ID `8c3b5fcb…`, se puede cambiar en los ajustes):

1. En *Redirect URIs* añade `https://diegodgzlpz.github.io/cartas-musicales/`
   (y `http://127.0.0.1:8000/` si pruebas en local con `python -m http.server 8000`).
2. En *APIs used* marca **Web API**.
3. En *User Management* añade el correo de cada cuenta que vaya a iniciar sesión (modo desarrollo).

Inicio de sesión en la TV: **Iniciar sesión aquí** (con el teclado del mando) o **Iniciar sesión con el móvil**:
la TV muestra un QR, se escanea con el móvil y se inicia sesión allí. La sesión viaja cifrada (AES-GCM, clave solo
en el QR) por un canal aleatorio de [ntfy.sh](https://ntfy.sh); el móvil no la guarda.

## Jugar en la TV

Abre `https://diegodgzlpz.github.io/cartas-musicales/` en el navegador de la TV. El modo TV se activa solo en
Android TV / Google TV, Fire TV, Samsung (Tizen) y LG (webOS); también con `?tv=1` o en los ajustes.

- Pantalla apaisada: carta a la izquierda, equipos, línea temporal y botones a la derecha, con margen para
  las TV que recortan los bordes.
- Mando: flechas para moverse, OK para pulsar, OK sobre la carta o ⏯ para reproducir, ⏭ siguiente carta,
  Atrás cierra el diálogo abierto.
- Dispositivos: Android TV y Chromecast con Google TV necesitan un navegador (TV Bro, Puffin TV, Firefox…);
  Fire TV trae Silk; Samsung y LG su navegador. Un Chromecast antiguo (sin mando) solo puede recibir la pestaña
  enviada desde Chrome del ordenador o el móvil («Enviar…»), y se maneja desde ahí.
- Para que suene: Spotify Connect con la app de Spotify de la TV abierta (sigue sonando en segundo plano en
  Android TV) o con el móvil o un altavoz como dispositivo.

## Actualizar las cartas

`cards.js` se genera desde la carpeta del generador (la de encima de `web/`):

```
python cartas.py playlist <URL>     # cartas nuevas desde una playlist (luego --apply)
python cartas.py web                # solo regenerar cards.js
```

El estilo y el idioma salen de MusicBrainz y se corrigen a mano en `data/categorias_*.csv`;
la década se calcula en la web a partir del año. Detalles en el README del generador.

Después, commit y push: GitHub Pages publica los cambios en uno o dos minutos.
