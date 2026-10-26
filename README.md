# ALEPH

Superposición transparente de guías de composición en la pantalla. Útil
para el análisis y estudio de la fotografía cinematográfica viendo
películas, series y anime.

![Captura de la app](docs/Aleph-Panel.png)

## CARACTERÍSTICAS

- Pool con 11 guías preestablecidas: regla de tercios, triángulos áureos,
  espirales de Fibonacci, centro, diagonales y rejilla áurea (Phi Grid).
  Incluye un espacio vacío para trabajar solo con las reglas propias.

- Definición de reglas personalizadas por el usuario.

- Modo pasivo (click-through): la ventana deja de capturar el ratón y
  los clics pasan al contenido de abajo.

- Ventana redimensionable, para ajustar los marcos a diferentes
  resoluciones.

- Captura de pantalla limpia con las guías y reglas superpuestas.

- Acceso directo en el Escritorio y registro en el menú de aplicaciones
  en la primera ejecución.

## GALERÍA

Las guías de Aleph sobre una película, en modo pasivo: la overlay no
intercepta el ratón ni las teclas, así que la película sigue siendo lo
que estás mirando.

<table>
  <tr>
    <td width="50%"><a href="docs/aleph-01.jpg"><img src="docs/aleph-01.jpg" alt="Aleph sobre una película, muestra 1"></a></td>
    <td width="50%"><a href="docs/aleph-02.jpg"><img src="docs/aleph-02.jpg" alt="Aleph sobre una película, muestra 2"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="docs/aleph-03.jpg"><img src="docs/aleph-03.jpg" alt="Aleph sobre una película, muestra 3"></a></td>
    <td width="50%"><a href="docs/aleph-04.jpg"><img src="docs/aleph-04.jpg" alt="Aleph sobre una película, muestra 4"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="docs/aleph-05.jpg"><img src="docs/aleph-05.jpg" alt="Aleph sobre una película, muestra 5"></a></td>
    <td width="50%"><a href="docs/aleph-06.jpg"><img src="docs/aleph-06.jpg" alt="Aleph sobre una película, muestra 6"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="docs/aleph-07.jpg"><img src="docs/aleph-07.jpg" alt="Aleph sobre una película, muestra 7"></a></td>
    <td width="50%"><a href="docs/aleph-08.jpg"><img src="docs/aleph-08.jpg" alt="Aleph sobre una película, muestra 8"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="docs/aleph-09.jpg"><img src="docs/aleph-09.jpg" alt="Aleph sobre una película, muestra 9"></a></td>
    <td width="50%"><a href="docs/aleph-10.jpg"><img src="docs/aleph-10.jpg" alt="Aleph sobre una película, muestra 10"></a></td>
  </tr>
</table>

## INSTALACIÓN

### Binarios (sin Python)

Descargá el binario de tu sistema desde la pestaña Releases del
repositorio:

<https://github.com/LucasLassa/aleph/releases>

- Linux x86_64
- Windows x86_64

En Linux, dale permisos de ejecución con `chmod +x`.
En Windows, "Ejecutar de todas formas" (SmartScreen).

### Desde el código

Requisitos:

- Python ≥ 3.11
- PySide6 ≥ 6.5

Instalación recomendada (venv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
aleph
```

En entornos con PEP 668, si preferís instalar en el usuario:

```bash
pip install --user --break-system-packages -e .[dev]
aleph
```

También podés correrlo sin instalar:

```bash
python -m src.main
```

## USO RÁPIDO

La ventana se abre a pantalla completa, adaptada al monitor, con el
marco activo.

### Atajos

| Tecla | Acción |
|---|---|
| `←` / `→` | Guía anterior / siguiente |
| `↑` / `↓` | Subir / bajar opacidad (pasos de 0.05) |
| `Shift + M` | Alternar modo marco (edición ↔ pasivo) |
| `Shift + D` | Borrar las reglas propias |
| `Shift + S` / `PrtScn` | Captura de pantalla con las líneas |
| `Shift + C` | Alternar color de las líneas (blanco / negro) |
| `F1` | Abrir / cerrar el manual |
| `Tab` | Abrir / cerrar el panel |
| `Clic izq.` | Con una regla armada, colocarla en el lienzo |
| `Shift + clic izq.` | Varias reglas seguidas / mover una existente |
| `Esc` | En cascada: cierra el manual → desarma la regla → cierra el panel → sale del modo película → cierra Aleph |

Las teclas se configuran en `src/core/keymap.py`.

### Panel lateral

Con el marco activo, se muestra un panel a la derecha que se despliega,
organizado en secciones:

- **Reglas**: guía anterior/posterior, opacidad y color de las líneas.
- **Dibujo**: botones para crear reglas propias (rectas, diagonales
  y vértices).
- **Modo película**: ocultar la botonera y borrar las líneas
  propias.
- **Opciones**: captura de pantalla, carpeta de guardado y manual de uso.
- **Apoya nuestra app**: link de donación, CVU y alias (para copiar y pegar).

### Modo pasivo

Con `Shift + M` (o el botón "Ocultar botonera") la overlay quita todo el
cromo y deja solo las guías; aparece un cartel "Shift+M para volver".
Abajo a la derecha queda un botón "Volver al modo edición". El manual
(`F1`) se abre desde cualquier modo.

Los atajos con Shift siguen funcionando con el marco OFF. El teclado
también responde sin botones visibles: `←` `→`, `↑` `↓`, `Shift + M`,
`Shift + C` y `Esc`.

## REGLAS PROPIAS

Además de las guías preestablecidas, podés crear líneas de composición a
medida. Los botones del panel se agrupan en rectas (horizontal y
vertical), diagonales (ascendente y descendente), vértices (cuatro
esquinas) y el punto de fuga.

### Cómo se colocan

1. Pulsá el botón del tipo de regla que quieras: el botón queda armado
   (iluminado) y el cursor se vuelve cruz.
2. Hacé click en el lienzo donde querés el vértice: la regla se coloca
   y el botón se desarma.
3. Mantené `Shift` al colocar para dibujar varias seguidas; con un
   arrastre movés la regla que acabás de colocar.

### Cómo se borran

`Shift + D` (o el botón "Borrar mis líneas dibujadas" del panel)
borra todas las reglas propias.

### Espacio vacío

La guía "Espacio vacío" no dibuja ninguna línea preestablecida: queda
el lienzo limpio. Es útil para usar solo tus reglas.

## CAPTURAS DE PANTALLA

`Shift + S`, `PrtScn` (o el botón "Capturar") guarda una foto con la guía
activa y las reglas superpuestas, casi sin demora.

- Se guarda en Descargas, o en la carpeta elegida con "Guardar en".
- Nombres: `aleph_regla_de_tercios_2026-10-24_15-30-12_001.png`
  (guía, fecha-hora y contador).

## CONFIGURACIÓN

La configuración se guarda en
`~/.config/aleph/config.json` al cerrar la app: opacidad,
color de líneas, carpeta de capturas y si ya se vio el manual
(`seen_manual`).

## DESARROLLO

```bash
pip install -e .[dev]
python -m pytest
ruff check src tests
```

Para generar los binarios:

```bash
pip install -e .[dev]
pyinstaller aleph.spec
# Linux/Windows: dist/aleph(.exe)    [onefile]
```

Estructura:

```
src/
├── main.py              # punto de entrada
├── app.py               # config + estado + plataforma + ventana
├── ui/                  # ventana, paintEvent, íconos
├── core/                # estado, guías, reglas, captura, keymap
├── platform/            # backends por SO (Qt genérico, Wayland)
├── config/              # defaults + load/save
└── utils/               # logger, geometría (Fibonacci, perpendicular)
```

