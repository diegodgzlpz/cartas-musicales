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

## Controles

- Doble toque / doble clic en la carta, botón **Revelar** o `Espacio`: girar la carta
- Botón **Siguiente** o `→`: siguiente carta
- El mazo se baraja sin repeticiones y el progreso se guarda en el navegador

## Actualizar las cartas

Desde la carpeta del generador:

```
python web/build_data.py --csv cards_with_design_columns.csv
```

Después, commit y push: GitHub Pages publica los cambios en uno o dos minutos.
