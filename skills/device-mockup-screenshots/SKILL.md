---
name: device-mockup-screenshots
description: TRIGGER — immer lesen, wenn ein App-/Webapp-Screenshot ODER eine Bildschirmaufnahme auf einer Website in einem Geräte-Mockup (v.a. iPhone) gezeigt werden soll, und immer, wenn der Inhalt in einem bestehenden Mockup ausgetauscht wird. Auslöser u.a. "Screenshot in ein Handy einbauen", "iPhone-Mockup", "Handy-Rahmen", "App im Rahmen zeigen", "Bildschirm reinsetzen", "Dynamic Island", "Device Mockup", "wie sieht das im Handy aus", "mehrere Handys auf der Seite", "Bild im Handy austauschen", "Video/Bildschirmaufnahme auf der Website einbauen", "Clip soll beim Scrollen starten", "App-Demo zeigen", generell wenn über eine App/Webapp gesprochen wird und dafür etwas Visuelles gezeigt werden soll. Deckt drei Verfahren ab (transparentes Rahmen-PNG, PSD-Mockup-Pack, und Rahmen-als-Auflage mit austauschbarem Inhalt für Screenshots UND Videos), fertige Python-Skripte, den kompletten Copy-Paste-Code für HTML/CSS/Scroll-Steuerung, ffmpeg-Rezepte zum Zuschneiden von Bildschirmaufnahmen sowie bekannte Fallstricke (Dynamic Island bei Aufnahmen, abgerundete Bildschirmecken, täuschende Headless-Screenshots). SKIP für normale Foto-/Stock-Bilder auf einer Website (siehe `client-website-standards`) — dieser Skill ist nur für "App-Inhalt in einem Gerät zeigen".
---

# Device-Mockup-Screenshots (DE)

Ziel: ein App-/Webapp-Screenshot soll auf einer Website wie ein **echtes Foto/Render eines Geräts** aussehen — ohne dass ein sichtbarer Tisch/Studio-Hintergrund mitkommt, und ohne dass es wie ein selbstgebauter CSS-Rahmen wirkt (das fällt Kunden auf und wirkt unfertig).

## Ziel-Qualität (Checkliste, bevor ein Ergebnis als fertig gilt)
- **Kein Hintergrund**: Ergebnis ist ein PNG/WebP mit Alphakanal — nur Gerät + weicher Schlagschatten, transparent sonst. Funktioniert dadurch auf jeder Seitenfarbe.
- **Bündiger Bildschirm**: Screenshot-Inhalt sitzt exakt in der (oft abgerundeten) Bildschirmfläche, keine Kante/Naht sichtbar, nichts guckt an den Ecken raus.
- **Dynamic Island korrekt**: bei iPhones mit Dynamic Island ist das EINE durchgezogene Pille (Kamera-Punkt ist Teil derselben Form), NICHT zwei getrennte Formen nebeneinander — das ist ein häufiger Fehler bei billigen/kostenlosen Rahmen-Assets. Vor Verwendung eines neuen Rahmens visuell prüfen.
- **Nativ hochauflösend**: mindestens ~1200px Bildschirm-Breite im Quellmaterial. Hochskalieren eines kleinen Rahmens (z.B. 392×800px) glättet nur, erzeugt keine echten Details — sieht auf großen Screens/Retina-Displays weich/unscharf aus.
- **Statusleiste sichtbar lassen**: Uhrzeit/WLAN/Akku im Screenshot drinlassen, das wirkt wie ein echter Screenshot. Ausnahme: Falls der Screenshot selbst schon eine eigene, selbstgezeichnete Notch/Dynamic-Island-Grafik enthält, genau diese Stelle vorher mit der Hintergrundfarbe der App übermalen — sonst liegen zwei Pillen übereinander (die eigene aus dem Screenshot + die echte vom Rahmen).

## Erst entscheiden: Screenshot oder Video?

**Standard ist der Screenshot.** Er ist leichter, schärfer, braucht keine Freigabe-Prüfung von
bewegtem Material und lässt sich in einer Minute austauschen. Ein Video nur dann, wenn die
**Bewegung selbst** etwas erklärt, was ein Standbild nicht kann (z.B. ein Modell drehen, eine
Karte aufklappen, zwischen zwei Ergebnissen wechseln).

Wenn Video: **ein Clip zeigt genau eine Sache**, 3–6 Sekunden, als Loop. Nicht eine lange
Aufnahme mit fünf Themen an einer Stelle einbauen, sondern mehrere kurze Clips an den
jeweils passenden Abschnitten. Details: `references/screencast-clip-recipes.md`.

Desktop-/Web-App-Ansichten gehören **nicht** in einen Handy-Rahmen, sondern in einen
schlichten Bildschirm-Rahmen (fertiges CSS dafür in `references/frame-overlay-component.md`).

## Drei Verfahren

Verfahren A und B rechnen den Screenshot **fest** in ein flaches Ergebnisbild. Verfahren C
lässt den Bildschirm ein echtes Loch und legt den Inhalt per CSS dahinter — nur damit ist der
Inhalt später **ohne Bildbearbeitung austauschbar**, und nur damit sind Videos möglich.

| | Inhalt tauschen | Video möglich | Aufwand |
|---|---|---|---|
| A / B (eingerechnet) | Skript erneut laufen lassen | nein | gering |
| C (Rahmen als Auflage) | eine Datei ersetzen | ja | einmalig ausmessen |

### A — Einfaches transparentes PNG (schnell, Qualität variiert)
Quelle z.B. **webmobilefirst.com/en/mockups/**: passendes Modell suchen, Button "Transparent", PNG laden — keine Registrierung nötig, Lizenz i.d.R. frei für kommerzielle Nutzung (auf der jeweiligen Downloadseite selbst gegenprüfen und Lizenzhinweis dokumentieren, siehe unten). Nachteil: kostenlose Standardgröße oft klein (z.B. 392×800px), und die Dynamic Island ist bei manchen Modellen falsch als zwei getrennte Formen statt einer durchgezogenen Pille eingezeichnet — gegen die Checkliste oben prüfen, bevor der Rahmen verwendet wird.

### B — PSD-Mockup-Pack (empfohlen für Hero-/Schlüsselbilder)
Quelle z.B. **mockups-design.com** ("Free ... Mockup"-Pakete, Lizenz-PDF liegt im Download bei — i.d.R. Royalty Free, private und kommerzielle Nutzung erlaubt, aber die PSD-Datei selbst darf nicht weiterverteilt/verkauft werden, nur das fertige Ergebnisbild). Deutlich höhere Auflösung (oft 4000×3000px) und fotorealistischer, weil eigene Schatten-/Licht-Reflex-/Foto-Rausch-Ebenen mitgeliefert werden. Braucht einmalig `pip3 install psd-tools scikit-image`.

## Das Skript: `scripts/frame_screenshot.py`
Deckt beide Verfahren ab. In das jeweilige Projekt kopieren (z.B. `<projekt>/tools/frame_screenshot.py`) und von dort aufrufen:

```
python3 tools/frame_screenshot.py --frame RAHMEN.png --screenshot SCREENSHOT.png --output ERGEBNIS.png
python3 tools/frame_screenshot.py --psd RAHMEN.psd --screenshot SCREENSHOT.png --output ERGEBNIS.png --design-group Design
```

- **Modus A** (`--frame`): erkennt das transparente Bildschirm-Loch automatisch per Flood-Fill vom Bildrand aus, skaliert den Screenshot per "cover" hinein und maskiert exakt auf die (ggf. abgerundete) Loch-Form — nicht nur auf deren rechteckige Bounding-Box.
- **Modus B** (`--psd`): erwartet die bei mockups-design.com übliche Ebenen-Struktur — eine Gruppe "Mockup" mit einer Bildschirm-Ebenengruppe (Standardname "Design", per `--design-group` anpassbar, falls ein anderes Pack andere Namen nutzt), deren Ebenenmaske die abgerundete Bildschirm-Form vorgibt. Blendet automatisch Hilfs-Ebenen wie "Delete this layer" (Wasserzeichen-Hinweis), "Background" und "Highlights" aus, damit das Ergebnis transparent bleibt.

Das Skript selbst liegt in diesem Skill unter `scripts/frame_screenshot.py`. Wie ein Aufruf in der Praxis aussieht, steht dort im Kopfkommentar. In einem Projekt, das das Verfahren schon benutzt, sind die gemessenen Werte im Design-Dokument des Projekts festgehalten, nicht hier: sie gelten nur für das jeweilige Mockup-Pack.

### C — Rahmen als Auflage, Inhalt austauschbar (für Screenshots UND Videos)

Der Bildschirm bleibt ein echtes Loch, der Rahmen liegt per `z-index` darüber, der Inhalt
(`<img>` oder `<video>`) sitzt in Prozent positioniert dahinter. Tauschen = eine Datei
ersetzen. Zwei Schritte:

```
python3 scripts/export_frame.py RAHMEN.psd assets/mockups/iphone-frame-transparent.png --aspect 0.6664
```

Das Skript liefert den transparenten Rahmen **und** die exakten CSS-Prozentwerte für Position
und Eckenradius des Bildschirms. Diese Werte nie schätzen, sie sind pro Mockup-Pack anders.

Den kompletten Copy-Paste-Baukasten (CSS-Komponente, HTML für Screenshot- und Video-Variante,
Scroll-Steuerung per `IntersectionObserver`, Bildschirm-Rahmen für Desktop-Ansichten) enthält
**`references/frame-overlay-component.md`**. Dort steht auch der wichtigste Fallstrick:
iOS verbreitert die Dynamic Island während einer Bildschirmaufnahme, weshalb bei Videos eine
zusätzliche schwarze Blende über die Island gelegt werden muss.

Aus einer Rohaufnahme einen tauglichen Clip machen (Bewegungsprofil messen, Totzeit
herausschneiden, beschleunigen, zuschneiden, Poster erzeugen, Datenschutz-Kontrolle):
**`references/screencast-clip-recipes.md`**.

## Nacharbeit
1. Ergebnis auf den tatsächlichen Bildinhalt zuschneiden (bei PSD-Rahmen bleibt oft viel transparenter Leerraum um das Gerät übrig — sonst wirkt das Gerät auf der Seite unnötig klein).
2. Als **WebP mit Alphakanal** exportieren statt PNG — deutlich kleinere Dateigröße bei gleicher Transparenz (Faustregel aus der Praxis: ~70 KB statt ~380 KB), alle gängigen Browser unterstützen das.
3. **Bildnachweis-Pflicht** beachten (siehe [[client-website-standards]]): Rahmen-Quelle, Lizenz und Downloaddatum in der `BILDNACHWEIS.md` des Projekts dokumentieren — genau wie bei einem Stockfoto, auch wenn es "nur" ein Rahmen ist.
4. Im HTML als normales `<img>` einsetzen. Kein CSS-Rahmen-Nachbau (Farbverlauf+Schatten) als Ersatz versuchen — sieht laut Kundenfeedback in der Praxis sichtbar nachgebaut/unprofessionell aus, ein echtes Foto/Render wirkt überzeugender.

## Bekannte Fallstricke (aus der Praxis, schon einmal passiert)
- **Bounding-Box statt echter Loch-Form maskiert** → an abgerundeten Ecken schaut der Screenshot-Hintergrund sichtbar raus. Immer die tatsächliche (ggf. runde) Form als Maske benutzen, nicht nur deren Bounding-Box (macht das Skript oben schon richtig).
- **Reihenfolge bei PSD-Rahmen**: Die Bildschirmfläche ist dort oft NICHT transparent, sondern mit einer Platzhalterfarbe gefüllt. Deshalb umgekehrte Reihenfolge zu Modus A: erst der Rahmen, dann der Screenshot oben drauf (nicht wie bei einem echten Loch: erst Screenshot, dann Rahmen oben drauf).
- **Volltransparente/-opake Hilfs-Ebenen in PSDs** (z.B. eine "Highlights"-Ebene mit Screen-Blend-Modus, randlos, ohne eigene Maske) verhindern Transparenz im Endergebnis, selbst wenn die Hintergrund-Ebene schon ausgeblendet ist. Auf Ebenen ohne eigene Maske UND ohne eigenen Alphakanal-Verlauf achten — die müssen mit ausgeblendet werden.
- **Unsichtbare Duplikat-Ebenen**: Ein reiner Namens-Filter beim Ebenen-Rendern reicht nicht — `visible` explizit mitprüfen, sonst werden eigentlich ausgeblendete Duplikat-Ebenen (gleicher Name) versehentlich mitgerendert und der Bildschirminhalt erscheint doppelt/verschoben.
- **Bei Verfahren C: abgerundete Bildschirmecken nicht vergessen** → sonst schauen die
  rechteckigen Ecken des Inhalts an allen vier Ecken über die Rahmen-Silhouette hinaus. Der
  `border-radius` muss als Prozentpaar angegeben werden (X% der Breite / Y% der Höhe), damit
  die Ecken beim Skalieren kreisrund bleiben. Werte liefert `scripts/export_frame.py`.
- **Bei Verfahren C mit Video: Dynamic Island der Aufnahme ist breiter als die des Rahmens**,
  weil iOS sie während der Aufnahme für den roten Punkt verbreitert. Lösung ist eine schwarze
  CSS-Blende darüber, nicht Übermalen im Video und nicht Wegschneiden der Statusleiste — die
  Begründung dazu in `references/frame-overlay-component.md`.
- **Headless-Screenshots mit `--window-size=390` täuschen** bei der Mobile-Prüfung: das Layout
  rendert breiter, nur der Screenshot wird beschnitten. Sieht wie ein Overflow-Bug aus, ist
  keiner. Stattdessen iframe-Wrapper mit fester Breite benutzen, siehe
  `references/screencast-clip-recipes.md`.
- **Screenshot komplett croppen wirkt schlechter als erwartet**: Erst-Instinkt war, die Statusleiste (Uhrzeit etc.) im Screenshot ganz wegzuschneiden, um Konflikte mit dem echten Rahmen zu vermeiden. Kundenfeedback: das sieht unrealistischer aus als eine sichtbare Uhrzeit. Besser: nur die eigene Notch-Grafik übermalen (siehe Ziel-Qualität oben), Rest vom Screenshot drinlassen.

## Andere Blickwinkel (schräg, Hand hält Gerät, Vorder-+Rückseite)
PSD-Packs enthalten oft mehrere Szenen. Das Skript oben geht von einer **flachen/frontalen** Bildschirmfläche aus (Rechteck bzw. runde Form ohne Perspektive). Bei angewinkelten Szenen ist die Bildschirmfläche perspektivisch verzerrt — dafür fehlt aktuell eine perspektivische Entzerrung/Warp-Erweiterung im Skript (bei Bedarf ergänzen: 4-Punkt-Homographie von Screenshot-Rechteck auf die vier Eckpunkte der verzerrten Bildschirmfläche, analog zur Perspective-Warp-Logik, die für ein foto-basiertes Hand-Mockup in einer früheren Iteration schon einmal gebaut wurde).
