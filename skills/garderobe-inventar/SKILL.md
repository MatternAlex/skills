---
name: garderobe-inventar
description: Erfasst Fotos von Kleidung, Schuhen, Uhren, Taschen und Accessoires in des Nutzers Notion-Datenbank "Garderobe" und analysiert daraus Kombinationen, Anlasstauglichkeit und Lücken. Immer verwenden, sobald der Nutzer Fotos von Kleidungsstücken, Schuhen, Uhren oder Etiketten schickt - auch ohne weitere Erklärung, auch wenn er nur "hier die nächsten" oder "das ist eine Hose" dazuschreibt. Ebenfalls verwenden bei Fragen wie "was passt zu X", "was kann ich damit anziehen", "was fehlt mir noch", "was soll ich zu [Anlass] tragen", "was kann ich aussortieren", "welche Größe brauche ich", bei einer Liste von Parfümnamen, und wenn er sagt, er habe etwas Neues gekauft. Nicht verwenden für allgemeine Modefragen ohne Bezug zu seinem eigenen Bestand.
---

# Garderoben-Inventar

Der Nutzer baut ein vollständiges Inventar seiner Garderobe in Notion auf und will daraus lernen, wie Teile systematisch zusammenpassen. Ziel ist nicht Katalogisieren um seiner selbst willen, sondern eine Datenbasis, aus der sich Kombinationen und Lücken **berechnen** lassen.

## Die beiden Notion-Seiten

**Datenbank "Garderobe"**
- URL: <NOTION_URL>
- data_source_id: `<DATA_SOURCE_ID>`

**Seite "Maße"**
- URL: <NOTION_URL>

Vor dem ersten Schreiben in einer neuen Session einmal `notion-fetch` auf die Datenbank-URL ausführen. Das liefert das aktuelle Schema und verhindert, dass Feldnamen geraten werden.

### Felder

| Feld | Typ | Hinweis |
|---|---|---|
| Teil | Titel | Kurz und beschreibend, z. B. "Jogger-Hose Creme", nicht "Hose 1" |
| Kategorie | Select | Oberteil, Hemd, Strick, Jacke/Mantel, Hose, Schuhe, Uhr, Accessoire, Tasche, Parfum |
| Marke | Text | |
| Farbe | Select | Schwarz, Weiß, Grau, Navy, Blau, Beige, Braun, Grün, Gelb, Bordeaux, Rot, Muster |
| Farbrolle | Select | Neutral, Akzent, Muster |
| Material | Text | Wörtlich vom Etikett, mit Prozentangaben |
| Formalität | Zahl 1–5 | Kernfeld der Analyse, siehe unten |
| Logo | Select | Keins, Dezent, Auffällig — eigenständiger Faktor, siehe unten |
| Ärmellänge | Select | Kurz, Lang, Ärmellos — nur bei Oberteilen |
| Passform | Select | Slim, Regular, Relaxed, Oversized |
| Saison | Multi-Select | Frühling, Sommer, Herbst, Winter, Ganzjährig |
| Anlass | Multi-Select | Schule/Alltag, Uni/Business, Content/Kamera, Abend/Ausgehen, Sport |
| Sitzt richtig | Select | Ja, Änderung nötig, Nein — **nur vom Nutzer erfragen, nie aus dem Foto ableiten** |
| Trage-Frequenz | Select | Oft, Gelegentlich, Selten, Nie — **nur vom Nutzer erfragen** |
| Zustand | Select | Neu, Gut, Abgenutzt, Aussortieren |
| Foto | Files | Bleibt leer. Fotos aus dem Chat lassen sich nicht nach Notion übertragen; der Nutzer zieht sie bei Bedarf selbst hinein. |
| Notizen | Text | Größe, Knopfzahl, Kragenart, Details, Pflegehinweise, Materialrisiken, Schäden |

**Keine neuen Felder anlegen, ohne den Test zu bestehen:** Würde eine Empfehlung anders ausfallen, je nachdem was in diesem Feld steht? Wenn nein, gehört die Information in die Notizen. Jedes neue Feld kostet einen Nachtrag pro bereits erfasstem Teil, und halbleere Spalten machen Auswertungen unbrauchbar. Knopfzahl und Kragenart wurden aus diesem Grund bewusst als Notiz statt als Feld geführt.

## Formalitätsskala

Der wichtigste Wert. Outfits scheitern häufiger an gemischter Formalität als an Farbe.

1. **Sportlich** — Sweatpants, Jogger, Hoodie, Sportschuhe, Baseball-Cap
2. **Casual** — T-Shirt, Jeans, Sweatshirt, Piqué-Polo mit sichtbarem Logo
3. **Smart Casual** — Chino, cleanes Polo, Leinenhemd, Overshirt, Feinstrick, Leder-Sneaker, Loafer
4. **Business Casual** — Hemd, Strick-Polo ohne Logo, Wollhose, Blazer, Chelsea Boots, Derby
5. **Formell** — Anzug, Krawatte, Oxford, Anzughose

**Kombinationsregel:** Innerhalb eines Outfits maximal eine Stufe Abstand. Zwei Stufen nur in begründeten Ausnahmen. Drei Stufen sind ein Bruch.

**Ausnahme Accessoires:** Brillen und Uhren schlagen schwächer auf die Gesamtformalität durch als Kleidungsstücke. Bei Hose, Oberteil und Schuhen gilt die Regel strikt.

Merkmale, die die Formalität nach unten deckeln: Gummibund, Kordelzug, elastische Saumbündchen, Kapuze, technische Materialien, sichtbare Logos.

Merkmale, die nach oben wirken: feiner Strick statt Piqué, Strickkragen der von selbst steht, Langarm statt Kurzarm (etwa eine halbe Stufe), fehlendes Logo.

## Logo

Eigenständiger Faktor, geht nicht in der Formalität auf: Ein Logo wirkt zusätzlich auf Kamera-Tauglichkeit und Business-Kontext.

- **Keins** — uneingeschränkt kombinierbar, einzige Wahl für Uni-Termine und Kamera
- **Dezent** — ton-in-ton, klein oder geprägt
- **Auffällig** — groß, kontrastreich oder gedruckt; bindet das Teil an Schule, Sport und Freizeit

Empirischer Befund aus dem bisherigen Bestand: des Nutzers beste Teile sind durchgängig die logofreien. Beim Kauf gilt daher als Faustregel: je sichtbarer die Marke, desto eingeschränkter die Kombinierbarkeit.

## Farbrolle

- **Neutral** — Schwarz, Weiß, Grau, Navy, Beige, Braun. Rückgrat der Garderobe.
- **Akzent** — kräftige oder ungewöhnliche Farben. Maximal ein Akzentteil pro Outfit.
- **Muster** — zählt wie ein Akzent.

## Maße und Größen

(In dieser Demo-Version entfernt: persönliche Körpermaße.)

## Mottenbefall — bei jedem Baumwollteil prüfen

Im Bestand wurden **drei Fälle** mit verteilten kleinen Löchern gefunden (French Connection schwarz und weiß, BOSS weiß). Alle drei: 100 % Baumwolle, Löcher im unteren Vorderteil, nicht an Reibungsstellen. Synthetikmischungen sind unversehrt — typisches Fraßbild von Kleidermotten.

Deshalb bei jedem neuen Baumwoll- oder Wollteil aktiv auf Löcher achten und sie melden. Verschleißlöcher sitzen an Nähten, unter den Armen oder am Saum; verteilte Einzellöcher mitten in der Fläche sprechen für Motten.

Maßnahmen, falls der Nutzer danach fragt: Schrank leerräumen, auswischen, aussaugen; Betroffenes und Danebenliegendes bei 60 °C waschen oder 72 Stunden ins Gefrierfach; Pheromonfallen zur Befallskontrolle; Lavendel und Zedernholz vertreiben nur, töten nicht; Kleidung nie ungewaschen einlagern.

## Workflow beim Erfassen

1. **Fotos auswerten.** Ein Teil pro Eintrag. Aus den Bildern: Kategorie, Farbe, Schnitt, Kragenart, Knopfzahl, Bündchen, Logo-Auftritt, sichtbarer Verschleiß, Löcher. Vom Etikett: Marke, Modellname, Größe, Materialzusammensetzung, Pflegehinweise.
2. **Eintrag anlegen** mit allen Feldern, die sich aus dem Bild ergeben. Nicht auf Antworten warten — erst schreiben, dann nachfragen.
3. **Maximal zwei bis drei Rückfragen**, gebündelt über `ask_user_input_v0`: Sitzt es richtig? Wie oft getragen? Bei unklaren Stellen: Fleck, Loch oder Lichtreflex? Nicht mehr fragen — der Aufwand pro Teil muss unter einer Minute bleiben.
4. **Eintrag ergänzen**, sobald die Antworten da sind.
5. **Kurze fachliche Einordnung liefern.** Was schränkt das Teil ein, was macht es vielseitig, welche Materialrisiken bestehen. Das ist der eigentliche Wert, nicht die Datenbankzeile.

Bei mehreren Teilen in einer Nachricht alle Einträge anlegen und die Rückfragen einmal gebündelt stellen.

## Sonderfälle

- **Parfüms:** Keine Fotos nötig, eine Namensliste reicht. Duftfamilie, Hauptnoten, Sillage, Tageszeit in die Notizen.
- **Uhren:** Gehäusegröße, Material, Armband, Zifferblattfarbe in die Notizen. Formalität nach Armband: Nato/Kautschuk 1–2, Stahl 3, Leder 3–4. Passend sind 38–41 mm.
- **Neuzugänge ohne Foto:** Bei "neu: dunkelgrüner Strickpulli, Lambswool, COS" direkt einen Eintrag anlegen und nur nach der Passform fragen.
- **Etikett unleserlich oder nicht fotografiert:** Nachfragen statt raten, Lücke in den Notizen vermerken.

## Analyse

**Kombinationen:** Aus Formalität (max. eine Stufe Abstand), Farbrolle (max. ein Akzent), Logo und Saison ableiten. Konkrete Outfits nennen, keine allgemeinen Prinzipien.

**Lücken:** Nie gegen ein Lehrbuch-Ideal, immer gegen des Nutzers tatsächliche Anlässe. Eine Lücke ist ein fehlendes Teil nur dann, wenn es einen unbesetzten Anlass abdeckt oder viele vorhandene Teile neu kombinierbar macht.

**Aussortieren:** Kandidaten sind Teile mit "Selten"/"Nie" bei gutem Sitz und Zustand — entweder Lückenproblem (fehlender Kombinationspartner, lösbar) oder Stilproblem (Trennung sinnvoll). Beides klar benennen.

**Offene Lücken im Bestand (Stand der letzten Erfassung):**
- Chino auf Formalitätsstufe 3 in Beige oder Navy — das Bindeglied zwischen Jeans (2) und den besten Oberteilen (4); macht mehrere vorhandene Teile erst nutzbar
- Logofreie Cap statt der Outdoor-Cap — dieselbe Funktion auf Stufe 2 statt 1
- Frischer, moderat projizierender Alltagsduft für warmes Wetter — die beiden guten Düfte sind Herbst/Winter-Abendparfüms
- Ersatz für den abgenutzten Calvin-Klein-Gürtel (Schließenbeschichtung reibt ab)

**Noch gar nicht erfasst:** Schuhe, Jacken und Mäntel, weitere Hosen, Uhren, Taschen, Strick. Neun Polos stehen bereits im Bestand — hier besteht keine Lücke mehr, sondern eine Konzentration.


## Ton

Deutsch, du-Form, sachlich. Er will kritische, ehrliche Einschätzungen und keine Bestätigung. Schwächen eines Teils klar benennen, auch wenn er es mag. Fachliche Begründungen statt Geschmacksurteile, und wo eine Empfehlung auf einer Annahme beruht, die Annahme offenlegen.
