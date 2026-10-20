# Cartas Musicales

Web para jugar con las tarjetas QR de canciones de Spotify.
Muestra la cara del QR para escanearla con el móvil y, con doble toque o el botón **Revelar**,
da la vuelta a la carta y muestra artista, año, mes y título.

Sitio estático, sin servidor: funciona con GitHub Pages o abriendo `index.html` con doble clic.

## Estructura

```
index.html            La página (HTML, CSS y JS)
cards.js              Las 2250 cartas (generado, no editar a mano)
vendor/qrcode.min.js  Generador de QR (qrcode-generator 1.4.4)
build_data.py         Regenera cards.js desde el CSV
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

## Actualizar las cartas

Desde la carpeta del generador:

```
python classify_categories.py          # solo si hay cartas nuevas: estilo e idioma -> categorias.csv
python web/build_data.py --csv cards_with_design_columns.csv
```

`classify_categories.py` busca cada artista en MusicBrainz (etiquetas y país) y deduce el estilo y el
idioma. Las correcciones se hacen a mano en `categorias.csv`; al relanzarlo solo clasifica las cartas
que aún no estén en el CSV. La década se calcula en la web a partir del año.

Después, commit y push: GitHub Pages publica los cambios en uno o dos minutos.
