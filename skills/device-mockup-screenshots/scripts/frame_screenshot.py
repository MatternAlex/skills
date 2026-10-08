#!/usr/bin/env python3
"""
Setzt einen App-/Webapp-Screenshot in ein Device-Mockup ein — entweder ein fertiges transparentes
PNG (z.B. iPhone-Rahmen von webmobilefirst.com) oder eine hochwertigere, mehrschichtige PSD-Mockup-
Datei (z.B. von mockups-design.com, mit eigenem Schatten/Licht/Noise für mehr Fotorealismus).

Modus 1 — einfaches transparentes PNG:
    python3 frame_screenshot.py --frame RAHMEN.png --screenshot SCREENSHOT.png --output ERGEBNIS.png

    Erkennt den transparenten Bildschirm-Ausschnitt im Rahmen automatisch (Flood-Fill vom Bildrand
    aus), skaliert den Screenshot per "cover" hinein, maskiert exakt auf die (ggf. abgerundete)
    Loch-Form. Neuen Rahmen: auf webmobilefirst.com/en/mockups/ das passende Modell suchen,
    "-transparent.png" herunterladen.

Modus 2 — PSD-Mockup-Pack (z.B. mockups-design.com, höhere Auflösung + Fotorealismus):
    python3 frame_screenshot.py --psd RAHMEN.psd --screenshot SCREENSHOT.png --output ERGEBNIS.png

    Erwartet die bei mockups-design.com übliche Ebenen-Struktur: eine Gruppe "Mockup" mit einer
    Bildschirm-Ebenengruppe (Default-Name "Design", per --design-group anpassbar), deren Ebenenmaske
    die abgerundete Bildschirm-Form vorgibt. "Background"/"Highlights"/"Delete this layer" werden
    automatisch ausgeblendet, damit das Ergebnis transparent bleibt (kein Foto-Hintergrund).
    Braucht `pip install psd-tools scikit-image` (einmalig).

Neue PSD-Mockups von mockups-design.com: kostenlos, "Personal & commercial use", keine
Namensnennung nötig — Einschränkung laut Lizenz: die PSD-Datei selbst nicht weitergeben/verkaufen,
nur das fertige (flache) Ergebnisbild verwenden.
"""
import argparse
from collections import deque

from PIL import Image
import numpy as np


def find_screen_mask(frame: Image.Image, alpha_threshold: int = 10) -> np.ndarray:
    """True = gehört zum Bildschirm-Loch (innen, nicht mit dem Bildrand verbunden)."""
    alpha = np.array(frame.convert("RGBA"))[:, :, 3]
    h, w = alpha.shape
    transparent = alpha < alpha_threshold
    outside = np.zeros_like(transparent)

    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if transparent[y, x] and not outside[y, x]:
                outside[y, x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if transparent[y, x] and not outside[y, x]:
                outside[y, x] = True
                q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and transparent[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True
                q.append((nx, ny))

    screen = transparent & ~outside
    if not screen.any():
        raise ValueError("Kein innerer transparenter Bildschirm-Bereich im Rahmen gefunden.")
    return screen


def fit_cover(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    scale = max(target_w / img.width, target_h / img.height)
    new_w, new_h = round(img.width * scale), round(img.height * scale)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def frame_screenshot(frame_path: str, screenshot_path: str, output_path: str) -> None:
    frame = Image.open(frame_path).convert("RGBA")
    screenshot = Image.open(screenshot_path).convert("RGBA")

    screen_mask = find_screen_mask(frame)
    ys, xs = np.where(screen_mask)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    fitted = fit_cover(screenshot, x1 - x0, y1 - y0)

    # Screenshot-Ebene auf Rahmengröße, dann exakt auf die Loch-Form zuschneiden (nicht nur
    # auf das rechteckige Bounding-Box — sonst gucken an abgerundeten Ecken Kanten raus).
    shot_layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    shot_layer.paste(fitted, (x0, y0))
    shot_arr = np.array(shot_layer)
    shot_arr[:, :, 3] = np.where(screen_mask, shot_arr[:, :, 3], 0)
    shot_layer = Image.fromarray(shot_arr, "RGBA")

    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    result.alpha_composite(shot_layer)
    result.alpha_composite(frame)
    result.save(output_path)
    print(f"Bildschirm-Loch erkannt: {(x0, y0, x1, y1)} ({screen_mask.sum()} px) -> gespeichert unter {output_path}")


def frame_screenshot_psd(
    psd_path: str,
    screenshot_path: str,
    output_path: str,
    mockup_group: str = "Mockup",
    design_group_name: str = "Design",
    hide_layers: tuple[str, ...] = ("Delete this layer", "Background", "Highlights", "Highlights pixel"),
) -> None:
    from psd_tools import PSDImage  # lazy import, nur für Modus 2 nötig

    psd = PSDImage.open(psd_path)
    screenshot = Image.open(screenshot_path).convert("RGBA")

    mockup = next(l for l in psd if l.name == mockup_group)
    design_group = next(c for c in mockup if c.name == design_group_name)
    dx0, dy0, dx1, dy1 = design_group.bbox

    def visible(layer):
        return layer.visible and layer.name not in hide_layers

    frame = psd.composite(layer_filter=visible)  # Rahmen, transparenter Hintergrund, Screen = Platzhalterfarbe

    screen_mask = np.zeros((psd.height, psd.width), dtype=bool)
    design_alpha = np.array(design_group.composite())[:, :, 3]
    screen_mask[dy0:dy1, dx0:dx1] = design_alpha > 200  # abgerundete Bildschirm-Form der Design-Ebenenmaske

    ys, xs = np.where(screen_mask)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    fitted = fit_cover(screenshot, x1 - x0, y1 - y0)

    shot_layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    shot_layer.paste(fitted, (x0, y0))
    shot_arr = np.array(shot_layer)
    shot_arr[:, :, 3] = np.where(screen_mask, shot_arr[:, :, 3], 0)
    shot_layer = Image.fromarray(shot_arr, "RGBA")

    # Reihenfolge umgekehrt zu Modus 1: der Bildschirm im PSD-Rahmen ist keine echte Transparenz,
    # sondern ein opaker Platzhalter — der Screenshot muss also OBEN drauf, nicht drunter.
    result = frame.copy()
    result.alpha_composite(shot_layer)
    result.save(output_path)
    print(f"Bildschirm-Form erkannt: {(x0, y0, x1, y1)} ({screen_mask.sum()} px) -> gespeichert unter {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame", help="Modus 1: transparentes Device-Mockup-PNG")
    parser.add_argument("--psd", help="Modus 2: mehrschichtige Mockup-PSD-Datei")
    parser.add_argument("--design-group", default="Design", help="Nur bei --psd: Name der Bildschirm-Ebenengruppe")
    parser.add_argument("--screenshot", required=True, help="Screenshot (Statusleiste kann drinbleiben)")
    parser.add_argument("--output", required=True, help="Zieldatei (PNG mit Alphakanal)")
    args = parser.parse_args()

    if bool(args.frame) == bool(args.psd):
        parser.error("Genau eins von --frame oder --psd angeben.")
    if args.frame:
        frame_screenshot(args.frame, args.screenshot, args.output)
    else:
        frame_screenshot_psd(args.psd, args.screenshot, args.output, design_group_name=args.design_group)
