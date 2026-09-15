<p align="center">
  <a href="README.md">English</a> · <b>Español</b>
</p>

<div align="center">

<img src="recursos/gatoguard.png" width="104" alt="GatoGuard">

# GatoGuard

### Tu gato se paseó por el teclado. Éste lo vio venir.

Detecta cuando un gato se sube al teclado analizando **el comportamiento del
tecleo** —sin cámara, sin un modelo pesado—, bloquea la entrada hasta que un
humano la desbloquea, y deshace el «modo raro» que dejan los gatos: modificadores
atorados, Sticky Keys, CapsLock.

[![Release](https://img.shields.io/github/v/release/leostriker111/GatoGuard?style=flat-square&label=descargar)](../../releases)
[![Descargas](https://img.shields.io/github/downloads/leostriker111/GatoGuard/total?style=flat-square)](../../releases)
[![Plataforma: Windows](https://img.shields.io/badge/plataforma-Windows-0078D6?style=flat-square&logo=windows)](#instalación)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Licencia: PolyForm NC](https://img.shields.io/badge/licencia-PolyForm%20Noncommercial-ff69b4?style=flat-square)](LICENSE)

</div>

---

Un clon libre y en tu idioma de [PawSense](https://www.bitboost.com/pawsense/),
que es lo único que hace esto y lleva de shareware desde los noventa.

> Nació porque su autor tiene dos gatos a los que les encanta pasearse sobre el
> teclado, y no existía un equivalente libre por comportamiento para Windows.

## Qué es

Una **aplicación de bandeja**. La corres, aparece un gatito junto al reloj, y te
olvidas de ella hasta el día en que te salva. No hay línea de comandos ni nada
que configurar para que funcione.

Lo que la separa de una utilidad de «bloquear teclado» es que tiene que decidir,
de forma continua y en pocos milisegundos, si lo que está tecleando es una
persona apurada o un animal. Equivocarse en cualquiera de los dos sentidos la
vuelve inútil: si bloquea al humano es un estorbo, si se le va el gato es un
adorno.

## Propósito y alcance

**El propósito.** Los gatos se sientan en los teclados. El daño no es el
galimatías — es un `Ctrl+S` encima de un archivo bueno, un `rz555` en Blender, un
atajo que no sabías que existía. Esto te compra los dos segundos que necesitas
para levantar al gato.

**Qué abarca.** La detección, el bloqueo antes de que las teclas lleguen a
ninguna aplicación, recuperar el teclado después, y congelar el mouse cuando el
gato decide que la presa es el puntero.

**Qué no hace.** Sin cámara, sin nube, sin telemetría y sin permisos de
administrador. No mira *qué* escribes — la predicción de texto corre contra un
diccionario de frecuencias localmente, y no se guarda ni se manda nada.

## Contenido

- [Qué es](#qué-es) · [Propósito y alcance](#propósito-y-alcance)
- [Instalación](#instalación) · [Uso](#uso) · [Ajustar la sensibilidad](#ajustar-la-sensibilidad)
- [Cómo funciona la detección](#cómo-funciona-la-detección)
- [Para quien quiera meter mano](#contribuir)

## Instalación

**A — el ejecutable (lo más fácil).** Descarga `GatoGuard.exe` de
[Releases](../../releases) y ábrelo. Aparece un gatito en la bandeja del sistema.
Listo.

**B — con pip, desde el código:**

```bash
git clone https://github.com/leostriker111/GatoGuard.git
cd GatoGuard
pip install .
gatoguard
```

**C — correrlo directo:**

```bash
pip install -r requirements.txt
python gatoguard.py
```

Para que arranque solo con Windows, crea un acceso directo a `GatoGuard.exe` (o a
`pythonw gatoguard.py`) en:

```
%AppData%\Microsoft\Windows\Start Menu\Programs\Startup
```

## Uso

| acción | cómo |
|---|---|
| **Desbloquear** | Clic en cualquier parte de la pantalla de bloqueo, o <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>U</kbd> |
| **Modo descanso** — dejar de detectar sin cerrar | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>G</kbd>, alterna entre 🐈 *hay gatos cerca* y 😴 *no hay gatos cerca* |
| **Congelar / descongelar el mouse** | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>M</kbd> |
| **Avisar «¡aquí hay un gato!»** | <kbd>Shift</kbd>+<kbd>A</kbd>+<kbd>S</kbd>+<kbd>D</kbd> — modo alerta, umbrales más quisquillosos. Si lo pisa el gato, mejor: confirma la premisa 🐈 |
| **Ocultar / mostrar el panel de estado** | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>H</kbd> |
| **Minimizar el panel** | Clic en el gatito del panel |
| **Mover el panel** | Arrástralo a donde quieras; recuerda la posición |
| **Configurar** | Clic derecho en el ícono de la bandeja → **Configuración** |
| **Resetear el teclado ya** | Menú de la bandeja → **Resetear teclado ahora** |
| **Salir** | Menú de la bandeja → **Salir** |

La configuración se guarda en `config.json` — junto al script, o en
`%AppData%\GatoGuard\` si usas el `.exe`.

> Al suspender la PC, la librería de teclado pierde su hook. GatoGuard **se
> reinicia solo** al despertar (proceso nuevo = hooks nuevos). Si alguna vez no
> responde, **bandeja → «Reactivar detección»** hace lo mismo a mano.

### Ajustar la sensibilidad

Si te bota al escribir normal, abre **Configuración** y sube *Teclas en ráfaga* o
*Teclas simultáneas*, o apaga la señal que te moleste. Si no detecta al gato lo
suficientemente rápido, bájalas.

## Cómo funciona la detección

Un hook global de teclado alimenta un detector con cada evento. Se dispara con:

1. **Simultáneas** — N o más teclas presionadas dentro de 1.5 s y todavía
   sostenidas. Una pata cubre varias teclas.
2. **Ráfaga** — K teclas distintas en una ventana corta **y** lo tecleado no
   parece una palabra real.
3. **Tecla pegada** — una tecla (que no sea espacio, backspace, flechas o
   modificador) sostenida más de X ms. Un gato sentándose.

**Frenos de emergencia**, para cuando la certeza es tan alta que no hay que
esperar:

- *Velocidad imposible* — 6 teclas en 0.18 s, más rápido que cualquier mano.
- *Misma tecla machacada* — `aaaaaaa`, que antes contaba como una sola tecla.
- *Texto sin sentido* — `sdrtg`, `rz555`, aunque se escriba despacio. En Blender,
  `rz555` es un desastre.

**La retención de teclas es lo que lo hace funcionar.** Cada tecla se detiene unos
milisegundos *antes de entrar a la máquina*. Si en ese lapso no se detecta un
gato, se reinyecta tal cual y no notas nada; si se detecta, la tecla se
**descarta y jamás llega a ninguna app**. 60 ms por omisión, 0 la apaga, y se
desactiva sola en juegos a pantalla completa.

**La predicción de texto es lo que evita que te atrape a ti.** Escribir rápido no
es sospechoso si estás escribiendo palabras. El detector compara contra un
diccionario de frecuencias, tolerando *typos* y errores de dedo: una palabra
válida —o el principio de una— baja las sospechas y te da más margen de ráfaga,
mientras que la basura pura dispara antes.

Los idiomas se agarran solos de los teclados que tengas instalados en Windows.
Vienen diccionarios de español e inglés; otros (japonés en *romaji*, por ejemplo)
los cubre una heurística de distribución de vocales.

<br>

---

<div align="center">

## 🔧 Para quien quiera meter mano

*Todo lo de arriba es lo que hace. Todo lo de abajo es cómo lo hace.*

</div>

---

### Contribuir

Direcciones útiles:

- **Un port a macOS o Linux.** La lógica de detección de `deteccion.py` es pura y
  portable; todo lo que depende de la plataforma está en `winutils.py` y
  `hooks.py`.
- **Más diccionarios.** Agregar un idioma es una lista de frecuencias en el mismo
  formato que `es_50k.txt`.
- **Reportes de falsos positivos.** Si te bota escribiendo normal, el reporte que
  sirve dice *qué estabas escribiendo* y qué señal disparó — el panel de estado lo
  indica.

### De qué está hecho

**Python 3.9+ en Windows**, y la decisión interesante es que el motor de teclado
es **propio, escrito sobre `ctypes`**, sin ninguna librería de entrada de
terceros.

Eso importa por tres razones. Un solo hook de bajo nivel persistente hace
detección *y* bloqueo, en vez de instalar y quitar hooks y perder eventos en el
hueco. Ve **todas** las teclas — F1–F24, la tecla Windows, las de multimedia — y
no el subconjunto que expone un envoltorio. Y bloquea de verdad `F11`,
`Win+Ctrl+D` y los demás combos que casi todas las herramientas dejan pasar.

Ese mismo hook es la razón de que **los atajos sean a prueba de robo**: se
reconocen dentro de él, así que siguen funcionando aunque otra aplicación ya
tenga registrada esa combinación globalmente.

### Los archivos

| archivo | qué es |
|---|---|
| `gatoguard.py` | La aplicación: hooks, bandeja, GUI, overlay de bloqueo. |
| `deteccion.py` | **Lógica pura de detección** más la predicción de texto. Aquí no hay Windows, que es por lo que es el archivo con pruebas. |
| `hooks.py` | El motor de teclado sobre `ctypes`: el hook de bajo nivel, la retención y la reinyección. |
| `winutils.py` | Helpers de Windows: el campo de texto enfocado, el reset del teclado, los idiomas instalados. |
| `test_deteccion.py` | Pruebas de la lógica. |
| `es_50k.txt`, `en_50k.txt` | Diccionarios de frecuencias, de [FrequencyWords](https://github.com/hermitdave/FrequencyWords) (MIT). |
| `make_icon.py`, `build.ps1` | El ícono, y construir el `.exe`. |

### Construir el ejecutable

```powershell
pip install pyinstaller
./build.ps1
```

Queda en `dist/GatoGuard.exe`.

### El problema que le dio forma

La versión ingenua de este programa bloquea el teclado *después* de decidir que
hay un gato. Para entonces el gato ya tecleó. La detección necesita un puñado de
eventos para estar segura, y esos eventos ya llegaron a lo que tuvieras abierto.

De ahí la retención: detener cada tecla 60 ms, decidir, y recién entonces
dejarla pasar. Nadie percibe 60 ms de retraso escribiendo, y el detector consigue
su ventana gratis. El costo es que el programa tiene que poder reinyectar teclas
con fidelidad — que es la razón real de que el motor de teclado esté escrito a
mano en vez de prestado.

La segunda consecuencia es lo de ser consciente de la app al frente: 60 ms son
invisibles en un editor de texto e inaceptables en un juego, así que la retención
se apaga sola en juegos a pantalla completa, junto con ignorar las teclas típicas
de juego (WASD, flechas).

### Licencia

**[PolyForm Noncommercial 1.0.0](LICENSE)** — puedes usar, estudiar, modificar y
compartir el software libremente **para fines no comerciales**. No se permite
venderlo ni usarlo con fines de lucro. Diccionarios de
[FrequencyWords](https://github.com/hermitdave/FrequencyWords) (MIT).

### Proyectos relacionados

- **[PawSense](https://www.bitboost.com/pawsense/)** — el original, shareware de
  Windows desde los noventa. *Ése si prefieres pagar por algo con 25 años de
  camino encima;* éste existe porque también debería poder no pagarse.
