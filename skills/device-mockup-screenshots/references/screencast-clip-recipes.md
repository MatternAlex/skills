# Aus einer Bildschirmaufnahme einen Website-Clip machen

Rohaufnahmen sind fast immer zu lang, haben Standbild-Pausen und enthalten Dinge, die nicht
öffentlich gezeigt werden dürfen. Diese Rezepte bringen sie in einen Zustand, der auf eine
Website darf. Braucht `ffmpeg` (`brew install ffmpeg`).

## 0 — Aufnahme-Hygiene (spart die ganze Nacharbeit)

Vor dem Aufnehmen:
- **Demo-Konto verwenden**, nie ein echtes Nutzer-/Patientenkonto. Aufnahmen aus echten Konten
  enthalten regelmäßig Klarnamen, Geburtsdaten, Befunde, Medikamente, E-Mail-Adressen.
- **Nicht-stören-Modus an**, sonst poppen private Benachrichtigungen ins Bild.
- **Roter Aufnahme-Punkt vermeiden**: iPhone per Kabel an den Mac und über QuickTime →
  „Neue Filmaufnahme" mit dem iPhone als Quelle aufnehmen, statt die Bildschirmaufnahme im
  iOS-Kontrollzentrum zu starten. Dann nimmt iOS nicht selbst auf, es gibt keinen roten Punkt
  und keine verbreiterte Dynamic Island.
- Am Desktop vorher aufräumen: Lesezeichenleiste mit internen Tools, Seitenleisten mit
  „Angemeldet als …", offene Test-Einträge mit Namen wie „asdf" oder „Test 123".

## 1 — Bewegungsprofil: wo passiert überhaupt etwas?

Statt blind zu schneiden erst messen, sonst besteht der Clip halb aus Standbildern.

```bash
mkdir -p /tmp/motion && rm -f /tmp/motion/*.png
ffmpeg -y -ss 36 -to 58 -i AUFNAHME.mov -vf "fps=5,scale=120:-1" /tmp/motion/m_%04d.png
python3 - <<'PY'
import glob
import numpy as np
from PIL import Image
files = sorted(glob.glob('/tmp/motion/m_*.png'))
prev = None
START, STEP = 36, 0.2          # an -ss und fps anpassen
for i, f in enumerate(files):
    a = np.asarray(Image.open(f).convert('L'), dtype=np.float32)
    if prev is not None:
        d = np.abs(a - prev).mean()
        print(f'{START + i*STEP:6.1f}  {d:6.2f} ' + '#' * int(min(d, 40)))
    prev = a
PY
```

Werte unter ~0,3 sind Standbild, Ausschläge über ~5 sind Taps, Übergänge oder Szenenwechsel.
Daraus die aktiven Fenster ablesen und die längsten Totzeiten notieren.

## 2 — Schneiden, Totzeit entfernen, beschleunigen

Zwei Teilstücke zusammensetzen und die Standbild-Pause dazwischen entfernen. Wenn beide
Schnittkanten in einem Standbild liegen, ist der Schnitt **unsichtbar**, weil links und rechts
dasselbe Bild steht.

```bash
ffmpeg -y -i AUFNAHME.mov -filter_complex "\
[0:v]trim=start=37.8:end=41.0,setpts=PTS-STARTPTS[a]; \
[0:v]trim=start=44.5:end=52.8,setpts=PTS-STARTPTS[b]; \
[a][b]concat=n=2:v=1[cat]; \
[cat]setpts=PTS/2,fps=30,scale=540:-2[out]" \
  -map "[out]" -an -c:v libx264 -crf 24 -pix_fmt yuv420p -movflags +faststart clip.mp4
```

- `setpts=PTS/2` = doppelte Geschwindigkeit. Für Bedienoberflächen mit Text lieber 1,3x–1,6x,
  damit man mitlesen kann; für reine Bewegungen (3D-Modell drehen) sind 2x in Ordnung.
- `-an` entfernt die Tonspur (auf Websites ohnehin stumm).
- `-movflags +faststart` sorgt dafür, dass das Video sofort startet statt erst komplett zu laden.
- Zielgröße: Handy-Clip ~540px Breite, Desktop-Clip ~1200px Breite. Das reicht für Retina,
  weil die Anzeige nur ~420px bzw. ~600px breit ist. Faustwert Dateigröße: 60–100 KB pro Sekunde.

**Immer den fertigen Clip Bild für Bild gegenprüfen**, nicht nur die Zeitmarken glauben:

```bash
ffmpeg -y -i clip.mp4 -vf "fps=2,scale=220:-1" /tmp/check_%02d.png
```

Häufiger Fehler: Einzelbilder aus `fps=1` sind um eine Sekunde verschoben (`f_054` entspricht
Sekunde 53, nicht 54). Deshalb Schnittgrenzen immer am Bewegungsprofil aus Schritt 1
festmachen, nicht an Bildnummern.

## 3 — Nur den App-Inhalt behalten (Desktop-Aufnahmen)

Browser-Leisten, Lesezeichen, Seitenleisten mit Namen und System-Benachrichtigungen weg:

```bash
# crop=BREITE:HÖHE:X:Y  — Werte an einem Vollbild der Aufnahme ausmessen
ffmpeg -y -i AUFNAHME.mov -filter_complex "\
[0:v]trim=start=73.05:end=79.45,setpts=PTS-STARTPTS, \
crop=2514:1430:510:300,setpts=PTS/1.4,fps=30,scale=1200:-2[out]" \
  -map "[out]" -an -c:v libx264 -crf 25 -pix_fmt yuv420p -movflags +faststart clip.mp4
```

Beim Zuschnitt bewusst entscheiden: Die Produkt-Navigation am linken Rand zu behalten zeigt
den Funktionsumfang, sie wegzuschneiden entfernt oft gleichzeitig ein „Angemeldet als
<Klarname>" am unteren Ende. Im Zweifel wegschneiden.

## 4 — Poster erzeugen

Immer ein Poster mitliefern. Es zeigt sich bei „Bewegung reduzieren", blockiertem Autoplay und
während des Ladens. **Nicht** das allererste Bild nehmen, wenn dort noch ein Ladezustand oder
Spinner zu sehen ist.

```bash
ffmpeg -y -ss 1.0 -i clip.mp4 -frames:v 1 poster.png
python3 -c "from PIL import Image; Image.open('poster.png').convert('RGB').save('poster.webp','WEBP',quality=82,method=6)"
```

(Manche ffmpeg-Builds haben keinen WebP-Encoder, deshalb der Umweg über Pillow.)

## 5 — Fallstrick: Headless-Screenshots täuschen bei Mobile-Breiten

`chrome --headless --window-size=390,...` erzeugt **keinen** echten 390-px-Viewport. Das Layout
rendert breiter und der Screenshot wird nur auf 390 px beschnitten. Folge: Texte und Karten
sehen abgeschnitten aus, obwohl die Seite in Ordnung ist. Genau dieser Fehlalarm hat schon
einmal eine Bug-Jagd nach einem nicht existierenden Fehler ausgelöst.

Verlässlich ist eine Wrapper-Seite mit `<iframe style="width:390px">` auf die zu prüfende Seite:
darin stimmen Media Queries, Textumbruch und `getBoundingClientRect()`.

Für Overflow-Prüfungen die Rechtecke **aller** Elemente gegen die Viewport-Breite messen
(`getBoundingClientRect().right`), nicht `scrollWidth` je Element: bei `overflow: visible`
verrät `scrollWidth` überstehende Kinder nicht.

Autoplay im Headless-Test freischalten mit `--autoplay-policy=no-user-gesture-required`,
sonst bleibt im Screenshot immer nur das Poster stehen und man sucht den Fehler an der
falschen Stelle. Scrollen im iframe funktioniert in Headless dagegen nicht zuverlässig —
das Pausieren beim Wegscrollen lässt sich dort nicht automatisch prüfen, das muss von Hand
im echten Browser gegengesehen werden.

## 6 — Vor der Live-Schaltung

- Clip Bild für Bild auf Klarnamen, Geburtsdaten, Befunde, Medikamente, E-Mail-Adressen,
  private Benachrichtigungen und interne Kundennamen prüfen. Bei Aufnahmen aus echten Konten
  gilt: erst freigeben lassen, nicht „ist ja nur kurz zu sehen".
- Test-Platzhalter im Bild („Hi David das ist ein Test", Modelle namens „asdf") sind auf einer
  Kundenseite ein Qualitätsproblem, auch wenn sie datenschutzrechtlich harmlos sind.
- Kurz halten: 3–6 Sekunden reichen für einen Loop. Ein Clip soll **eine** Sache zeigen.
  Wenn mehrere Dinge gezeigt werden sollen, mehrere kurze Clips an mehreren Abschnitten
  einsetzen statt eines langen.
