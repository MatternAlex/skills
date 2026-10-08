#!/usr/bin/env python3
"""Exportiert aus einer Mockup-PSD den Geräterahmen ALS TRANSPARENTE AUFLAGE
(Bildschirmfläche ausgeschnitten) und gibt die exakte Position des Bildschirm-Loches
in Prozent aus — für Verfahren C aus dem Skill (Inhalt liegt hinter dem Rahmen und
ist per CSS austauschbar, funktioniert für Screenshots UND Videos).

Unterschied zu frame_screenshot.py: Dort wird der Screenshot fest in den Rahmen
gerechnet (ein flaches Ergebnisbild). Hier bleibt der Bildschirm ein echtes Loch,
damit im HTML ein <img> oder <video> dahinter gelegt werden kann.

    pip3 install psd-tools pillow numpy   # einmalig
    python3 export_frame.py RAHMEN.psd rahmen-transparent.png [--aspect 0.6664]

Ausgabe:
  * das PNG mit transparentem Bildschirm
  * die CSS-Prozentwerte für left/top/width/height des Bildschirms
  * der Eckenradius des Bildschirms als CSS-Prozentpaar (border-radius: X% / Y%)

`--aspect` (Breite/Höhe) schneidet das Ergebnis auf ein gewünschtes Seitenverhältnis
zu, horizontal auf die Gerätemitte zentriert. Nützlich, um mehrere Mockups auf einer
Website optisch gleich groß zu halten (z.B. denselben Wert wie ein bereits
vorhandenes Mockup-Bild verwenden).
"""
import argparse
import json

import numpy as np
from PIL import Image
from psd_tools import PSDImage

HIDE_LAYERS = ("Delete this layer", "Background", "Highlights", "Highlights pixel",
               "[BG] Change Color")


def screen_mask_from_psd(psd, design_group_name="Design", mockup_group="Mockup",
                         extra_hide=()):
    """Findet die Bildschirmflaeche. Packs sind unterschiedlich aufgebaut:
    mockups-design.com hat eine Gruppe "Mockup" mit einer Gruppe "Design",
    ls.graphics hat pro Gerätefarbe eine Gruppe (z.B. "Space Gray") mit einem
    Smart Object "Change This". Deshalb sind beide Namen einstellbar, und mit
    --hide lassen sich weitere Ebenen ausblenden (z.B. die zweite Farbvariante)."""
    hide = tuple(HIDE_LAYERS) + tuple(extra_hide)

    try:
        mockup = next(l for l in psd if l.name == mockup_group)
    except StopIteration:
        raise SystemExit(
            f"Gruppe {mockup_group!r} nicht gefunden. Vorhandene oberste Ebenen: "
            + ", ".join(repr(l.name) for l in psd))
    try:
        design = next(c for c in mockup if c.name == design_group_name)
    except StopIteration:
        raise SystemExit(
            f"Ebene {design_group_name!r} nicht in {mockup_group!r} gefunden. Vorhanden: "
            + ", ".join(repr(c.name) for c in mockup))
    dx0, dy0, dx1, dy1 = design.bbox

    def visible(layer):
        return layer.visible and layer.name not in hide

    frame = psd.composite(layer_filter=visible)
    mask = np.zeros((psd.height, psd.width), dtype=bool)
    mask[dy0:dy1, dx0:dx1] = np.array(design.composite())[:, :, 3] > 200
    return frame, mask


def corner_radius(mask, x0, y0, x1, y1):
    """Radius der abgerundeten Bildschirmecke: Einrückung der obersten Maskenzeile."""
    rows = mask[y0:y1, x0:x1]
    mid_left = np.where(rows[rows.shape[0] // 2])[0].min()
    top_left = np.where(rows[0])[0].min()
    return int(top_left - mid_left)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("psd")
    ap.add_argument("output_png")
    ap.add_argument("--design-group", default="Design",
                    help="Name der Bildschirm-Ebene/-Gruppe, z.B. 'Design' oder 'Change This'")
    ap.add_argument("--mockup-group", default="Mockup",
                    help="Name der Geraete-Gruppe, z.B. 'Mockup' oder 'Space Gray'")
    ap.add_argument("--hide", nargs="*", default=[],
                    help="Weitere Ebenennamen ausblenden, z.B. die zweite Farbvariante 'Silver'")
    ap.add_argument("--aspect", type=float, default=None,
                    help="Zielverhältnis Breite/Höhe, z.B. 0.6664")
    ap.add_argument("--width", type=int, default=900, help="Zielbreite des PNG (Standard 900)")
    args = ap.parse_args()

    psd = PSDImage.open(args.psd)
    frame, mask = screen_mask_from_psd(psd, args.design_group, args.mockup_group, args.hide)

    ys, xs = np.where(mask)
    sx0, sy0, sx1, sy1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    radius = corner_radius(mask, sx0, sy0, sx1, sy1)

    # Bildschirm im Rahmen wirklich transparent machen (in PSDs ist das oft nur eine
    # Platzhalterfarbe, kein echtes Loch).
    arr = np.array(frame)
    arr[:, :, 3] = np.where(mask, 0, arr[:, :, 3])
    img = Image.fromarray(arr, "RGBA")

    # Zuschnitt: sichtbarer Geräteinhalt inkl. Schatten, plus optionales Zielverhältnis.
    solid = np.array(img)[:, :, 3] > 3
    solid[sy0:sy1, sx0:sx1] = True
    cys, cxs = np.where(solid)
    cx0, cy0, cx1, cy1 = int(cxs.min()), int(cys.min()), int(cxs.max()) + 1, int(cys.max()) + 1

    if args.aspect:
        # Gerätekörper = deutlich opake Pixel; daran horizontal zentrieren.
        body = np.array(img)[:, :, 3] > 30
        body[sy0:sy1, sx0:sx1] = True
        bys, bxs = np.where(body)
        body_cx = (int(bxs.min()) + int(bxs.max())) / 2
        h = cy1 - cy0
        w = round(h * args.aspect)
        cx0 = round(body_cx - w / 2)
        cx1 = cx0 + w

    img = img.crop((cx0, cy0, cx1, cy1))
    W, H = img.size
    img = img.resize((args.width, round(args.width * H / W)), Image.LANCZOS)
    img.save(args.output_png)

    info = {
        "png": [img.width, img.height],
        "aspect_w_h": round(W / H, 6),
        "css_left_pct": round((sx0 - cx0) / W * 100, 3),
        "css_top_pct": round((sy0 - cy0) / H * 100, 3),
        "css_width_pct": round((sx1 - sx0) / W * 100, 3),
        "css_height_pct": round((sy1 - sy0) / H * 100, 3),
        "screen_px": [sx1 - sx0, sy1 - sy0],
        "corner_radius_px": radius,
        "css_border_radius": (f"{round(radius / (sx1 - sx0) * 100, 2)}% "
                              f"/ {round(radius / (sy1 - sy0) * 100, 2)}%"),
    }
    print(json.dumps(info, indent=2))
    print("\nCSS für das Inhalts-Element (siehe references/frame-overlay-component.md):")
    print(f"  left: {info['css_left_pct']}%; top: {info['css_top_pct']}%;")
    print(f"  width: {info['css_width_pct']}%; height: {info['css_height_pct']}%;")
    print(f"  border-radius: {info['css_border_radius']};")


if __name__ == "__main__":
    main()
