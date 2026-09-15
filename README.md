<p align="center">
  <b>English</b> · <a href="LEEME.md">Español</a>
</p>

<div align="center">

<img src="recursos/gatoguard.png" width="104" alt="GatoGuard">

# GatoGuard

### Your cat walked across the keyboard. This one saw it coming.

Detects a cat on the keyboard by **how the typing behaves** — no camera, no heavy
model — locks the input until a human unlocks it, and undoes the "weird mode"
cats leave behind: stuck modifiers, Sticky Keys, CapsLock.

[![Release](https://img.shields.io/github/v/release/leostriker111/GatoGuard?style=flat-square&label=download)](../../releases)
[![Downloads](https://img.shields.io/github/downloads/leostriker111/GatoGuard/total?style=flat-square)](../../releases)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-0078D6?style=flat-square&logo=windows)](#install)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: PolyForm NC](https://img.shields.io/badge/license-PolyForm%20Noncommercial-ff69b4?style=flat-square)](LICENSE)

</div>

---

A free, Spanish-and-English clone of [PawSense](https://www.bitboost.com/pawsense/),
which is the only other thing that does this and has been shareware since the
nineties.

> It exists because its author has two cats who love to stroll across the
> keyboard, and there was no open-source behaviour-based equivalent for Windows.

## What it is

A **tray application**. You run it, a small cat appears next to the clock, and
you forget about it until the day it saves you. There is no command line and
nothing to configure before it works.

The thing that makes it different from a "lock keyboard" utility is that it has to
decide, continuously and in a few milliseconds, whether the thing typing is a
person in a hurry or an animal. Getting that wrong in either direction is
useless: block the human and it's spyware, miss the cat and it's decoration.

## Purpose and scope

**The purpose.** Cats sit on keyboards. The damage isn't the gibberish — it's
`Ctrl+S` over a good file, `rz555` in Blender, a shortcut you didn't know
existed. This buys you the two seconds you need to pick the cat up.

**What it covers.** Detection, blocking before the keys reach any application,
recovering the keyboard afterwards, and freezing the mouse when the cat decides
the pointer is prey instead.

**What it does not do.** No camera, no cloud, no telemetry, no administrator
rights. It does not watch *what* you write — the text prediction runs against a
frequency dictionary locally, and nothing is stored or sent.

## Contents

- [What it is](#what-it-is) · [Purpose and scope](#purpose-and-scope)
- [Install](#install) · [Use](#use) · [Tuning the sensitivity](#tuning-the-sensitivity)
- [How the detection works](#how-the-detection-works)
- [For developers](#contributing)

## Install

**A — the executable (easiest).** Download `GatoGuard.exe` from
[Releases](../../releases) and open it. A cat appears in the system tray. Done.

**B — with pip, from source:**

```bash
git clone https://github.com/leostriker111/GatoGuard.git
cd GatoGuard
pip install .
gatoguard
```

**C — run it directly:**

```bash
pip install -r requirements.txt
python gatoguard.py
```

To start it with Windows, put a shortcut to `GatoGuard.exe` (or to
`pythonw gatoguard.py`) in:

```
%AppData%\Microsoft\Windows\Start Menu\Programs\Startup
```

## Use

| action | how |
|---|---|
| **Unlock** | Click anywhere on the lock screen, or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>U</kbd> |
| **Rest mode** — stop detecting without closing | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>G</kbd>, toggling between 🐈 *cats nearby* and 😴 *no cats nearby* |
| **Freeze / unfreeze the mouse** | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>M</kbd> |
| **Declare "there's a cat here!"** | <kbd>Shift</kbd>+<kbd>A</kbd>+<kbd>S</kbd>+<kbd>D</kbd> — alert mode, fussier thresholds. If the cat presses it, so much the better: it confirms the premise 🐈 |
| **Hide / show the status panel** | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>H</kbd> |
| **Minimise the panel** | Click the cat on the panel |
| **Move the panel** | Drag it anywhere; it remembers |
| **Configure** | Right-click the tray icon → **Configuración** |
| **Reset the keyboard now** | Tray menu → **Resetear teclado ahora** |
| **Quit** | Tray menu → **Salir** |

Settings are saved in `config.json` — next to the script, or in
`%AppData%\GatoGuard\` if you're running the `.exe`.

> When the PC suspends, the keyboard library loses its hook. GatoGuard
> **restarts itself** on wake (a new process means new hooks). If it ever stops
> responding, **tray → "Reactivar detección"** does the same thing by hand.

### Tuning the sensitivity

If it trips while you're typing normally, open **Configuración** and raise *Teclas
en ráfaga* or *Teclas simultáneas*, or switch off whichever signal annoys you. If
it's too slow to catch the cat, lower them.

## How the detection works

A global keyboard hook feeds a detector with every event. It trips on:

1. **Simultaneous** — N or more keys pressed within 1.5 s and still held. One paw
   covers several keys.
2. **Burst** — K distinct keys in a short window **and** what was typed doesn't
   look like a real word.
3. **Stuck key** — one key (not space, backspace, arrows or a modifier) held for
   more than X ms. A cat sitting down.

**Emergency brakes**, for when certainty is high enough not to wait:

- *Impossible speed* — 6 keys in 0.18 s, faster than any hand.
- *Same key mashed* — `aaaaaaa`, which used to count as a single key.
- *Nonsense text* — `sdrtg`, `rz555`, even typed slowly. In Blender, `rz555` is a
  disaster.

**Key retention is what makes it work.** Every keystroke is held for a few
milliseconds *before it enters the machine*. If no cat is detected in that window
it's re-injected untouched and you never notice; if one is, the key is
**discarded and never reaches any application**. 60 ms by default, 0 turns it
off, and it disables itself in fullscreen games.

**Text prediction is what stops it trapping you.** Typing fast is not suspicious
if you're typing words. The detector compares against a frequency dictionary,
tolerating typos and finger slips: a valid word — or the start of one — lowers
suspicion and buys you more burst, while pure garbage trips it sooner.

Languages are picked up automatically from your Windows keyboard layouts. Spanish
and English dictionaries ship with it; others (Japanese in romaji, for instance)
fall back to a vowel-distribution heuristic.

<br>

---

<div align="center">

## 🔧 For developers

*Everything above is what it does. Everything below is how it does it.*

</div>

---

### Contributing

Useful directions:

- **A macOS or Linux port.** The detection logic in `deteccion.py` is pure and
  portable; everything platform-specific is in `winutils.py` and `hooks.py`.
- **More dictionaries.** Adding a language is a frequency list in the same format
  as `es_50k.txt`.
- **False-positive reports.** If it trips on you while you're typing normally, the
  useful bug report is *what you were typing* and which signal fired — the status
  panel says which.

### What it's made of

**Python 3.9+ on Windows**, and the interesting decision is that the keyboard
engine is **its own, written on `ctypes`**, with no third-party input library.

That matters for three reasons. A single persistent low-level hook does both
detection *and* blocking, instead of installing and removing hooks and losing
events in the gap. It sees **every** key — F1–F24, the Windows key, media keys —
rather than the subset a wrapper exposes. And it genuinely blocks `F11`,
`Win+Ctrl+D` and the other combinations that most tools let slip through.

The same hook is why the **shortcuts are theft-proof**: they're recognised inside
it, so they still work even when another application has already registered that
combination globally.

### The files

| file | what it is |
|---|---|
| `gatoguard.py` | The application: hooks, tray, GUI, lock overlay. |
| `deteccion.py` | **Pure detection logic** plus text prediction. No Windows in here, which is why it's the file with tests. |
| `hooks.py` | The keyboard engine on `ctypes`: the low-level hook, retention and re-injection. |
| `winutils.py` | Windows helpers: the focused text field, keyboard reset, installed languages. |
| `test_deteccion.py` | Tests for the logic. |
| `es_50k.txt`, `en_50k.txt` | Frequency dictionaries, from [FrequencyWords](https://github.com/hermitdave/FrequencyWords) (MIT). |
| `make_icon.py`, `build.ps1` | The icon, and building the `.exe`. |

### Building the executable

```powershell
pip install pyinstaller
./build.ps1
```

It lands in `dist/GatoGuard.exe`.

### The problem that shaped it

The naive version of this program blocks the keyboard *after* deciding there's a
cat. By then the cat has already typed. Detection needs a handful of events to be
confident, and those events have already reached whatever you had open.

Hence retention: hold every key for 60 ms, decide, and only then let it through.
Nobody perceives 60 ms of latency while typing, and the detector gets its window
for free. The cost is that the program has to be able to re-inject keystrokes
faithfully — which is the actual reason the keyboard engine is hand-written
rather than borrowed.

The second consequence is the foreground-app awareness: 60 ms is invisible in a
text editor and unacceptable in a game, so retention turns itself off in
fullscreen games, along with the usual game keys (WASD, arrows) being ignored.

### License

**[PolyForm Noncommercial 1.0.0](LICENSE)** — use, study, modify and share it
freely **for non-commercial purposes**. Selling it or using it for profit is not
allowed. Dictionaries from [FrequencyWords](https://github.com/hermitdave/FrequencyWords) (MIT).

### Related projects

- **[PawSense](https://www.bitboost.com/pawsense/)** — the original, Windows
  shareware since the nineties. *Use that if you'd rather pay for something with
  25 years of shipping behind it;* this exists because it should also be possible
  not to.
