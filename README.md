# Drescher Ochoa

Sitio web en alemán de Heidrun Drescher-Ochoa, con blog, biblioteca, presentación de la autora y fundamentos de HOLLA.

**Sitio publicado:** https://drescher-ochoa-lesewelten.elisaaguilar10524.chatgpt.site/

## Vista previa local

El sitio es estático y no requiere instalar dependencias:

```sh
python3 -m http.server 4173 --directory dist
```

Abre http://localhost:4173/ en el navegador. Para las rutas de artículos y libros, sirve siempre `dist/` como raíz del sitio.

## Archivos principales

- `dist/index.html`: portada y secciones principales.
- `dist/style.css`: diseño adaptable y paleta de colores.
- `dist/app.js`: búsqueda, filtros, favoritos y lectura de artículos.
- `dist/data.js`: contenidos de los 28 artículos y 8 libros.
- `dist/assets/`: imágenes, diploma y PDF de HOLLA.
- `dist/artikel/`, `dist/buecher/`: páginas HTML independientes para rastreo e indexación.
- `dist/blog/`, `dist/bibliothek/`: archivos navegables sin JavaScript.
- `dist/paths.js`: relación entre identificadores y direcciones de las páginas.
- `dist/robots.txt`, `dist/sitemap.xml`, `dist/llms.txt`: descubrimiento del contenido.
- `.openai/hosting.json`: configuración del sitio existente en Sites.
- `scripts/generate-search-pages.py`: generador de páginas de archivo y metadatos; revisar sus modificaciones sobre la portada antes de volver a ejecutarlo.

## Publicación

El contenido listo para servir está en `dist/`. La publicación actual se administra con Sites. Este repositorio es una copia del código y sus recursos; subir cambios a GitHub no actualiza automáticamente el sitio publicado.

Las direcciones canónicas y el mapa del sitio apuntan al dominio de publicación actual. Deben actualizarse si se cambia el dominio.

## Contenido y créditos

Textos, imágenes y publicaciones proceden del sitio original https://drescher-ochoa.net/ y de los materiales aportados por la propietaria. Los derechos corresponden a sus respectivos titulares. No se concede una licencia de reutilización adicional mediante este repositorio.

El diploma incluye la fotografía original y una versión aclarada para presentación en pantalla.

## GitHub Pages

La acción `.github/workflows/pages.yml` publica automáticamente `dist/` cuando cambia `main`.

**GitHub Pages:** https://eliszen-28.github.io/drescher-ochoa-de/

`prepare-github-pages.py` adapta las rutas al prefijo `/drescher-ochoa-de/` en el artefacto de publicación. Los archivos de producción y sus direcciones canónicas de Sites permanecen intactos.
