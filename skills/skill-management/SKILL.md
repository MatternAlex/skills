---
name: skill-management
description: TRIGGER — immer lesen, wenn ein neuer Claude-Code-Skill erstellt, umbenannt, verschoben wird oder die Skill-Speicherstruktur selbst verändert wird (Arbeiten an ~/.claude/skills/, SKILL.md-Dateien, Trigger-Beschreibungen). GILT AUCH für jede rm/mv/cp-Operation auf Pfaden unter "Library/Mobile Documents" (iCloud Drive), nicht nur für Skills. Auslöser u.a. "Skill erstellen", "neuen Skill", "SKILL.md", "Skill umbenennen/verschieben", "Ordner in iCloud verschieben/löschen". Deckt Speicherort/Symlink-Setup, Pflichtformat für SKILL.md, Pflicht zum passenden CLAUDE.md-Trigger-Absatz sowie eine harte Sicherheitsregel für Datei-Operationen in iCloud Drive ab (nach einem konkreten Datenverlust-Vorfall am 05.07.2026).
---

# Skill-Verwaltung (DE)

## Speicherort
Drei Ebenen, jede mit einer klaren Aufgabe:
1. **Original:** Alle Skills liegen physisch in einem synchronisierten Cloud-Ordner (zum Beispiel `iCloud Drive/AI/Claude/Skills/`). So sind sie auf allen Geräten gleich.
2. **Lesepfad:** `~/.claude/skills` ist ein **Symlink** auf diesen Ordner. Claude Code liest ganz normal über den lokalen Pfad, für alle Tools transparent. Neue Skills werden unter `~/.claude/skills/<skill-name>/SKILL.md` angelegt, ein direktes Arbeiten im Cloud-Pfad ist nicht nötig.
3. **Sicherung und Verlauf:** Ein Sync-Skript kopiert die Skills **einseitig** (Cloud → privates Git-Repo). Das Repo ist Backup und Verlauf und macht das Setup für andere KI-Tools lesbar, es wird nie zurück in die Cloud geschrieben.


## Pflichtformat einer SKILL.md
- YAML-Frontmatter mit `name:` (kebab-case, identisch zum Ordnernamen) und `description:`.
- `description:` beginnt mit `TRIGGER — `, gefolgt von einer präzisen Beschreibung, wann der Skill automatisch gelesen werden soll, inkl. konkreter Auslöser-Formulierungen ("Auslöser u.a. ..."). Darüber werden Skills automatisch erkannt, ohne dass der Nutzer einen Slash-Befehl tippen muss.
- Lange Rechtstexte/Vorlagen/Templates: in `references/*.md` auslagern, im SKILL.md nur kurz verlinken — hält die SKILL.md selbst kompakt.

## Trigger-Beschreibung so schreiben, dass der Skill sich zuverlässig selbst aktiviert
Ein Skill nützt nichts, wenn er nur bei perfekt formulierten Anfragen anspringt. Beim Formulieren der `description:` deshalb:

1. **Sowohl Fachbegriff als auch Alltagsformulierung abdecken.** Der Nutzer fragt selten mit dem exakten Fachwort — er sagt eher "kannst du auf der Restaurant-Seite das Bild austauschen" als "Website-Content ändern". Auslöser-Liste entsprechend mit konkreten, realistischen Beispielsätzen füllen, nicht nur mit Fachbegriffen.
2. **Auch indirekte/beiläufige Fälle einschließen**, nicht nur den offensichtlichen Hauptfall. Beispiel: `client-website-standards` greift nicht nur bei "neue Website bauen", sondern auch bei "auch bei kleinen, scheinbar unrelated Änderungen" an einer bestehenden Kundenseite.
3. **SKIP-Fälle explizit benennen**, wenn der Skill in einem ähnlich klingenden, aber falschen Kontext nicht feuern soll (verhindert Fehlalarm-Trigger).
4. **Gegenprobe nach dem Schreiben:** die Situation, die gerade zur Skill-Erstellung geführt hat, gedanklich als Prompt durchspielen — hätte genau diese Formulierung den Trigger ausgelöst? Falls unsicher: Auslöser-Liste konkreter machen statt abstrakter.
5. **Nach dem Anlegen verifizieren**, dass der Skill tatsächlich in der Liste der verfügbaren Skills auftaucht (erscheint automatisch als `<system-reminder>` in der nächsten Nachricht) — das ist die einzige direkte Bestätigung, dass er registriert wurde.

## Automatisches Triggern zusätzlich absichern
Ein Skill wird zuverlässiger automatisch angewendet, wenn zusätzlich ein kurzer Absatz in `~/.claude/CLAUDE.md` existiert, der explizit darauf verweist (Muster: "Bei jeder Arbeit an X IMMER zuerst den Skill `<name>` beachten (`~/.claude/skills/<name>/SKILL.md`)"). Bei jedem neuen Skill also auch `~/.claude/CLAUDE.md` ergänzen — die SKILL.md-Beschreibung allein ist der primäre, der CLAUDE.md-Absatz der redundante/verstärkende Mechanismus. Trotzdem bleibt beides eine Anweisung an mich, keine hart erzwungene Systemregel — bei mehrdeutigen Formulierungen kann ein Trigger trotzdem verpasst werden.

## Vor dem Anlegen: Überschneidung prüfen
Bevor ein neuer Skill entsteht: kurz die bestehende Skill-Liste (System-Reminder mit verfügbaren Skills, oder `~/.claude/skills/`) durchsehen, ob ein Thema schon abgedeckt ist oder sich mit einem geplanten neuen Skill überschneiden würde. Im Zweifel lieber einen bestehenden Skill um einen Abschnitt erweitern, als ein zweites, teilweise überlappendes Regelwerk zu schaffen — zwei Skills mit ähnlichem Trigger können sich gegenseitig stören oder widersprechen.

## Sprachkonvention
Alle Skills werden auf Deutsch verfasst (des Nutzers Arbeitssprache), unabhängig davon, dass Namen/Frontmatter-Keys auf Englisch bleiben (`name`, `description`, Ordnername in kebab-case). Ausnahme nur, wenn ein Skill explizit für einen fremdsprachigen Kontext gedacht ist.

## Skills sind lebende Dokumente
Ein Skill ist nie "fertig geschrieben und dann unangetastet". Sobald bei der Arbeit auffällt, dass eine Regel im Skill lückenhaft, mehrdeutig oder veraltet ist (wie z.B. die "–"-Mehrdeutigkeit in `acquisition-list-standards` oder das fehlende Trigger-Schreibkapitel hier), den Skill direkt an Ort und Stelle nachbessern statt die Lücke nur im Gespräch zu erwähnen. Der Skill selbst ist die Quelle der Wahrheit, nicht der Chatverlauf.

## Menschenlesbarer Überblick (INDEX.md)
Zusätzlich zum automatischen Skill-Erkennungsmechanismus von Claude Code gibt es `~/.claude/skills/INDEX.md` — eine reine Übersichtsliste aller Skills mit Ein-Zeilen-Beschreibung, für der Nutzer selbst zum Durchklicken in Finder/iCloud, unabhängig davon, ob gerade eine Claude-Session läuft. Bei jedem Anlegen/Löschen/inhaltlichen Ändern eines Skills `INDEX.md` mit aktualisieren (kurzer Eintrag, kein Duplikat der ganzen SKILL.md).

## Checkliste "Skill fertig" (Definition of Done)
Vor Abschluss einer Skill-Erstellung/-Änderung immer durchgehen:
1. SKILL.md mit korrektem Frontmatter (`name`, `description` beginnend mit `TRIGGER — `, konkrete Auslöser-Beispiele)?
2. Lange Inhalte in `references/*.md` ausgelagert, SKILL.md selbst kompakt?
3. Überschneidung mit bestehenden Skills geprüft (siehe oben)?
4. Passender Absatz in `~/.claude/CLAUDE.md` ergänzt?
5. `~/.claude/skills/INDEX.md` aktualisiert?
6. Verifiziert, dass der Skill in der Liste der verfügbaren Skills auftaucht (nächster System-Reminder)?

## Sicherheitsregel für Datei-Operationen in iCloud Drive (Pflicht)
Am 05.07.2026 ist bei einer Skill-Migration echter Datenverlust entstanden: Ein Ordner in iCloud, der wie ein simples lokales Duplikat aussah, war tatsächlich das Ziel eines lokalen Symlinks — die echten Dateien lagen nur in iCloud. `rm -rf` darauf hat die echten Daten gelöscht (kein Papierkorb bei CLI-`rm` auf iCloud-Drive-Pfaden); ein nachfolgendes `mv` erzeugte zusätzlich einen kaputten, auf sich selbst zeigenden Symlink. Zwei von drei Dateien eines Skills gingen dabei unwiederbringlich verloren.

**Deshalb bei jeder Datei-Operation unter `~/Library/Mobile Documents/` (iCloud Drive) — nicht nur bei Skills:**
1. Vor `rm`/`mv`/`cp` auf einen Ordner/eine Datei: immer zuerst mit `ls -la` auf den **Eintrag im Elternverzeichnis** (nicht auf dessen Inhalt) prüfen, ob es ein Symlink ist (`l` am Zeilenanfang der Rechte) oder ein echtes Verzeichnis/Datei.
2. Bei einem Symlink: `readlink` benutzen und das tatsächliche Ziel ansehen, bevor irgendetwas gelöscht/verschoben wird. Nie annehmen "das ist bestimmt nur eine Kopie" — das war genau der Fehler.
3. Vor einer echten Löschung (`rm -rf`) mit Inhalt: wenn möglich umbenennen/verschieben (Backup-Suffix, z.B. `-ALT-<Datum>`) statt hart zu löschen. `rm` auf iCloud-Drive-Pfaden landet nicht im normalen Papierkorb und ist nicht ohne Weiteres wiederherstellbar.
4. Bei Verschiebe-Operationen mit Wildcards (`mv ordner/* ziel/`) zwischen zwei Pfaden unter `Mobile Documents`, oder wenn einer der beteiligten Pfade ein Symlink sein könnte: einzeln Schritt für Schritt prüfen statt mehrere Elemente in einem Rutsch zu verschieben.
5. Nach jeder solchen Operation das Ergebnis mit `find -L` bzw. `readlink` gegenprüfen, nicht nur den Exit-Code des Befehls vertrauen.

## GitHub-Sicherung der Skills (Pflicht nach jeder Änderung)
Die Skills werden zusätzlich in einem **privaten** Repo gesichert (`~/development/ai-workspace`, GitHub `<owner>/ai-workspace`). iCloud bleibt das Original, das Repo ist Verlauf und Backup. Nach jedem Anlegen, Ändern oder Löschen eines Skills (und von `~/.claude/CLAUDE.md` sowie nach jeder neuen oder geänderten Memory-Notiz über der Nutzer): `./sync.sh` im Repo ausführen (kopiert einseitig iCloud → Repo, schreibt nie nach iCloud), `git status` prüfen, committen und pushen. Das Repo darf nie öffentlich werden.
