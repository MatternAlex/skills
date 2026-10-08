# Verfahren C: Rahmen als Auflage, Inhalt austauschbar

Fertiger Baukasten für den Fall, dass der Inhalt im Gerät **später ohne Bildbearbeitung
getauscht** werden soll oder ein **Video** statt eines Screenshots gezeigt wird.

Prinzip: Der Geräterahmen ist ein PNG mit **ausgeschnittener Bildschirmfläche** und liegt
per `z-index` ÜBER dem Inhalt. Der Inhalt (`<img>` oder `<video>`) sitzt absolut
positioniert dahinter, in Prozent des Rahmens angegeben, damit beides gemeinsam skaliert.

Tauschen heißt dann: eine Datei ersetzen bzw. ein `src` ändern. Sonst nichts.

## Schritt 1 — Rahmen exportieren und ausmessen

```
python3 scripts/export_frame.py RAHMEN.psd assets/mockups/iphone-frame-transparent.png --aspect 0.6664
```

Das Skript gibt genau die vier Prozentwerte und den `border-radius` aus, die unten in das
CSS eingesetzt werden. **Nicht schätzen** — die Werte sind pro Mockup-Pack unterschiedlich.

`--aspect` nur setzen, wenn das Ergebnis optisch gleich groß wie ein anderes, bereits
vorhandenes Mockup auf derselben Website sein soll (Wert = Breite/Höhe des Vorhandenen).

## Schritt 2 — CSS (einmal pro Projekt)

Die Prozentwerte im Beispiel stammen aus einem iPhone-16-Pack von mockups-design.com und
sind ein realistischer Richtwert, aber **immer die eigene Messung aus Schritt 1 einsetzen**.

```css
/* Rahmen liegt über dem Inhalt; Inhalt sitzt im ausgeschnittenen Bildschirm. */
.device-video { position: relative; width: 100%; max-width: 420px; }
.device-video .device-frame {
  position: relative; z-index: 2;
  width: 100%; height: auto; display: block; pointer-events: none;
}
.device-video video,
.device-video .device-screen {
  position: absolute; z-index: 1;
  left: 16.667%; top: 1.423%; width: 66.736%; height: 96.237%;
  object-fit: cover; display: block; background: #fff;
  /* Bildschirmecken sind stark abgerundet. Als Prozentpaar angeben (X% der Breite /
     Y% der Höhe, beide ergeben denselben absoluten Wert), damit die Ecken beim
     Skalieren kreisrund bleiben. Ohne das schauen die rechteckigen Ecken des
     Inhalts an allen vier Ecken sichtbar über die Rahmen-Silhouette hinaus. */
  border-radius: 16.41% / 7.58%;
}

/* Nur nötig, wenn der Inhalt eine Bildschirmaufnahme mit sichtbarer Dynamic Island ist,
   siehe "Fallstrick Dynamic Island" unten. Maße = Island der Aufnahme, nicht die des Rahmens. */
.device-video .island {
  position: absolute; z-index: 3;
  left: 34.6%; top: 2.6%; width: 29.5%; height: 4.5%;
  background: #000; border-radius: 999px; pointer-events: none;
}
```

## Schritt 3 — HTML

**Variante Screenshot** (der einfache Normalfall, bevorzugen):

```html
<div class="device-video" role="img" aria-label="Kurz beschreiben, was die App hier zeigt.">
  <img class="device-screen" src="assets/img/app-screen.png" alt="">
  <img class="device-frame" src="assets/mockups/iphone-frame-transparent.png" alt="">
</div>
```

**Variante Video** (nur wenn die Bewegung wirklich etwas erklärt):

```html
<div class="device-video" role="img" aria-label="Kurz beschreiben, was die Aufnahme zeigt.">
  <video src="assets/video/app-demo.mp4" poster="assets/img/app-demo-poster.webp"
         muted loop playsinline preload="metadata" aria-hidden="true"></video>
  <img class="device-frame" src="assets/mockups/iphone-frame-transparent.png" alt="">
  <span class="island" aria-hidden="true"></span>
</div>
```

`muted` ist Pflicht, sonst verweigern Browser das automatische Abspielen. `playsinline`
verhindert, dass iOS das Video im Vollbild öffnet. Die Beschreibung gehört als
`aria-label` auf den Container, nicht als `alt` auf den Rahmen (der Rahmen ist Dekoration).

## Schritt 4 — Abspielen erst beim Hineinscrollen

Im Seitenfuß, zusätzlich zu bereits vorhandenen Scroll-Skripten:

```html
<script>
(function () {
  var videos = document.querySelectorAll('.device-video video, .screen-video video');
  if (!videos.length) return;

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion || !('IntersectionObserver' in window)) return; // Poster bleibt stehen

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var v = entry.target;
      if (entry.isIntersecting) {
        var p = v.play();
        if (p && p.catch) { p.catch(function () {}); } // Autoplay-Sperre: Poster bleibt stehen
      } else if (!v.paused) {
        v.pause();
        v.currentTime = 0;
      }
    });
  }, { threshold: 0.35, rootMargin: '200px 0px 200px 0px' });

  videos.forEach(function (v) { io.observe(v); });
})();
</script>
```

`rootMargin` gibt dem Video Vorlauf zum Laden, `currentTime = 0` sorgt dafür, dass es beim
Zurückscrollen von vorne beginnt statt unbemerkt durchzulaufen. Immer ein `poster` setzen:
das ist gleichzeitig die Anzeige für „Bewegung reduzieren", blockiertes Autoplay und die
Zeit bis zum Laden.

## Anordnung mehrerer Geräte auf einer Seite

Vorgabe des Nutzers, nachdem eine Dreier-Reihe mit Text darunter verworfen wurde:

- **Abwechselnd links und rechts**, nicht nebeneinander in einer Reihe. Also Text links /
  Gerät rechts, dann Gerät links / Text rechts, und so weiter. Der Text steht **daneben**,
  nicht darunter.
- **Alle Geräte gleich groß.** Breite über eine einzige CSS-Variable steuern (z.B.
  `--device-w: 380px`) und überall dieselbe verwenden, auch im Hero. Sonst wirken die
  Abschnitte unruhig.
- **Beim Stapeln auf dem Handy immer erst das Gerät, dann der Text**, unabhängig davon, ob
  die Reihe am Desktop umgedreht war:
  ```css
  @media (max-width: 860px) {
    .device-story.reverse .feature-media { order: -1; }
  }
  ```
- **Kurze Texte.** Pro Gerät eine Überschrift und ein bis zwei knappe Sätze. Lange Absätze
  neben einem Gerät liest niemand.
- **Textposition richtet sich nach dem Geräteformat:** Beim **hochkant stehenden Handy** steht
  der Text **daneben** (die Spalte daneben ist sonst leer). Beim **breiten Gerät wie einem
  MacBook** steht der Text **darunter**, weil daneben zu wenig Platz bleibt und die
  Bedienoberfläche im Video sonst zu klein wird.
- **Pro Geräteklasse eine einheitliche Größe:** eine Variable für alle Handys
  (`--device-w`), eine für alle MacBooks. Nicht pro Abschnitt einzeln setzen.

### Text und Bild wirklich verbinden

Kritik des Nutzers: „Man hat irgendwie nicht so Lust, ihn zu lesen, man muss es
irgendwie mehr verbinden." Ein Absatz, der neben einem Gerät steht, wird als getrennter
Textblock wahrgenommen und übersprungen. Was hilft:

1. **Beschriftungen direkt am Bildelement** (kurze Labels mit dünner Verbindungslinie auf die
   Stelle im Screenshot). Funktioniert **nur auf einem Standbild**: In einem laufenden Video
   scrollt der Inhalt weg und das Label zeigt nach einer Sekunde ins Leere. Für ein Video also
   nur brauchbar, wenn der Clip an dieser Stelle wirklich stehen bleibt.
2. **Gerät und Text in einer gemeinsamen Karte** (ein Rahmen, ein Hintergrund) statt in zwei
   weit auseinanderliegenden Spalten. Billigste und robusteste Variante.
3. **Überschrift als Aussage, nicht als Etikett.** „Ein Wert für den Tag" wird gelesen,
   „Erholungsindex" wird überflogen.
4. **Ein Gedanke pro Gerät.** Wer zwei Dinge erklären will, nimmt zwei Geräte.

## Lizenz und Ablage der Quelldateien (Pflicht)

Die kostenlosen Mockup-Packs (mockups-design.com, ls.graphics und vergleichbare) erlauben
private und kommerzielle Nutzung sowie Änderungen, meist ohne Namensnennung. Sie verbieten
aber ausdrücklich, **die Quelldatei selbst weiterzugeben oder öffentlich zugänglich zu
machen**. Erlaubt ist nur das fertige Bildergebnis.

Daraus folgt eine harte Ablageregel:

- **PSD- und Sketch-Dateien nie im Website-Ordner ablegen.** Am 04.09.2026 lagen genau deshalb
  in einem Projekt zwei Packs im Website-Ordner und mussten heraus.

  **Warum das die Lizenz bricht, auch ohne Absicht:** Der Website-Ordner wird beim Hochladen
  komplett auf den Server kopiert. Eine PSD, die dort liegt, ist danach unter ihrer Adresse
  für jeden direkt herunterladbar, auch wenn nirgends ein Link darauf zeigt: Verzeichnisse und
  Dateinamen sind erratbar, und Suchmaschinen finden solche Dateien. Juristisch ist das eine
  öffentliche Bereitstellung, also genau der Fall, den die Lizenzen verbieten. Es genügt
  nicht, die Datei einfach nicht zu verlinken.
- Quelldateien in einen **Nachbarordner außerhalb der Website** legen, z.B.
  `Projekte/<Projekt>/Mockup-Quellen/`.
- Im Website-Ordner liegen nur die **exportierten PNG-Rahmen**.
- Lizenz im Bildnachweis belegen: Anbieter, Produktname, Downloaddatum, erlaubte Nutzung und
  die Einschränkung zur Quelldatei. Bei einem Streit muss das nachweisbar sein, ein
  „war kostenlos" reicht nicht.

## Web-App-Ansichten ohne Geräterahmen

Desktop-Ansichten gehören nicht in ein Handy. Dafür reicht ein schlichter Bildschirm-Rahmen,
und wichtig: **keine feste Höhe mit `object-fit: cover`**, sonst wird die Bedienoberfläche
angeschnitten und unlesbar.

```css
.screen-video {
  position: relative; width: 100%;
  border-radius: 20px; overflow: hidden;
  border: 1px solid #d8e2de;
  box-shadow: 0 24px 48px -24px rgba(20,48,44,.35);
  background: #fff;
}
.screen-video video { width: 100%; height: auto; display: block; }
```

## MacBook: fertige Werte und Dateien

Getestet mit dem kostenlosen **MacBook Pro 16** von **ls.graphics** (im Download liegen `MacBook Pro 16.psd` und eine Sketch-Version). Dieses Pack ist brauchbar, weil der Hintergrund eine eigene abschaltbare Farbfläche ist und pro Gerätefarbe eine Gruppe existiert. **Nicht** brauchbar war das „M5 MacBook Pro" von goodmockups.com: dort steckt das Gerät selbst in der Hintergrund-Ebene, ohne Hintergrund ist auch das MacBook weg.

Ebenenstruktur bei ls.graphics: oberste Ebene `[BG] Change Color` (Hintergrund), dann je Farbe eine Gruppe `Space Gray` und `Silver`, darin `Shadow`, `MacBook Pro 16` und das Smart Object `Change This` (die Bildschirmfläche).

Export:

```
python3 scripts/export_frame.py "MacBook Pro 16.psd" assets/mockups/macbook16-frame-transparent.png \
  --mockup-group "Space Gray" --design-group "Change This" --hide Silver --width 1400
```

Ergebnisse dieses Packs (bei `--width 1400` ein PNG mit 1400×715):

```css
.mac-video { position: relative; width: 100%; max-width: 980px; margin: 0 auto; }
.mac-video .device-frame { position: relative; z-index: 2; width: 100%; height: auto; display: block; pointer-events: none; }
.mac-video video {
  position: absolute; z-index: 1;
  left: 14.729%; top: 2.164%; width: 69.017%; height: 86.157%;
  object-fit: contain; background: #fff; display: block;
  border-radius: 1.27% / 1.99%;
}
```

Zwei Punkte, die beim MacBook anders sind als beim iPhone:

- **Kein Dynamic-Island-Problem**, dafür ein deutlich breiteres Format (Bildschirm-Seitenverhältnis 1,569).
- **`object-fit: contain` statt `cover`**, weil Bildschirmaufnahmen vom Desktop meist breiter sind als 1,569 und `cover` sonst die äußeren Spalten der Web-App abschneidet. Damit die Restränder nicht auffallen, den Clip vorher **auf das App-Fenster zuschneiden**, dann sind seine Ränder hell und passen zum weißen Hintergrund. Bei einem Modalfenster über abgedunkelter Seite: Fenstergrenzen ausmessen (helle Fläche suchen) und exakt darauf schneiden, sonst liegt oben ein dunkler und unten ein weißer Balken.
- **Text gehört beim MacBook unter das Gerät**, nicht daneben (siehe Regel oben).

## Fallstrick Dynamic Island (kostet sonst mehrere Runden)

**iOS verbreitert die Dynamic Island während einer Bildschirmaufnahme**, um den roten
Aufnahme-Punkt darin anzuzeigen. Diese verbreiterte Island der Aufnahme ist damit **breiter
als die normale Island des Mockup-Rahmens** und schaut beidseitig heraus: zwei leicht
versetzte, unterschiedlich dunkle Formen übereinander.

Reihenfolge der Lösungsversuche, mit Ergebnis:

1. **Island-Zone im Video mit der App-Hintergrundfarbe übermalen** (`drawbox`) — funktioniert
   nur, wenn hinter der Statusleiste durchgehend dieselbe Farbe liegt. Scrollt dort eine weiße
   Karte durch, sieht man ein hartkantiges Rechteck. **Meist untauglich.**
2. **Statusleiste komplett wegschneiden** (`crop`) — sauber, aber der Inhalt rutscht nach oben
   und wird oben angeschnitten, und die Uhrzeit fehlt. Wirkt laut Praxisfeedback weniger echt.
3. **Schwarze Pille per CSS über die Island der Aufnahme legen** (`.island` oben) — **beste
   Lösung**: Statusleiste bleibt vollständig, nichts wird angeschnitten, es ist nur eine Island
   sichtbar, und der rote Aufnahme-Punkt verschwindet als Nebeneffekt mit.

Maße für die Pille aus einem Einzelbild der Aufnahme ausmessen (nicht raten): Luminanz-Profil
einer Zeile mitten durch die Island legen und die Kanten der dunklen Fläche ablesen, dann auf
die Rahmen-Prozente umrechnen. Der rote Punkt liegt INNERHALB der Island, nicht daneben.

## Prüfen, bevor es als fertig gilt

- An allen vier Bildschirmecken nachsehen, ob Inhalt über die Rahmen-Silhouette hinausschaut
  (passiert ohne den `border-radius` aus Schritt 2 immer).
- Statusleiste im Detail vergrößern: genau eine Island, keine doppelte Form, keine graue Kante.
- Mobile Darstellung mit einer echten Viewport-Breite prüfen, siehe Fallstrick in
  `screencast-clip-recipes.md` (Headless-Screenshots mit `--window-size` täuschen hier).
- Bildnachweis pflegen: Rahmen-Quelle und Lizenz, und bei Aufnahmen aus echten Konten den
  Freigabe-Status, siehe [[client-website-standards]].
