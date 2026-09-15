"""Genera keycat.ico (varios tamanos) a partir de recursos/keycat.png.

El icono es un gato parado sobre el teclado de una laptop, compuesto con los
emoji del sistema. La fuente esta en recursos/keycat.html: se abre en un
navegador y se captura a 512x512 con fondo transparente. Este script solo hace
el paso de PNG a .ico, que es el que necesita Windows.

    python make_icon.py
"""
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).parent
ORIGEN = AQUI / "recursos" / "keycat.png"
DESTINO = AQUI / "keycat.ico"

TAMANOS = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

if not ORIGEN.exists():
    raise SystemExit(f"no encuentro {ORIGEN} — mira el docstring de arriba")

img = Image.open(ORIGEN).convert("RGBA")
if img.size != (512, 512):
    img = img.resize((512, 512), Image.LANCZOS)

img.save(DESTINO, sizes=TAMANOS)
print(f"{DESTINO.name} generado con {len(TAMANOS)} tamanos")
