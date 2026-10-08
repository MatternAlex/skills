---
name: software-project-workflow
description: TRIGGER — immer lesen, wenn an einem Software-Projekt vom Nutzer gearbeitet wird (App, Backend, Webapp, Website als Code) — neu anlegen, Features bauen, Fehler beheben, committen, pushen, Branches, "zurückgehen", "den alten Stand wiederherstellen", README/Screenshots aktualisieren. Auslöser u.a. "bau eine App", "neues Projekt", "committe das", "speichere das auf GitHub", "geh zum alten Stand zurück", "was ist ein Branch", "wie sichern wir das", "Screenshots aktualisieren". Deckt den Standard-Ablauf ab (ein Ordner = ein privates Repo, nach jeder Änderung committen + pushen, README/STATUS/Screenshots mitpflegen), die Erklärung von Branches und Zurückgehen in einfachen Worten (der Nutzer ist kein erfahrener Coder, er kennt sich mit KI aus), sowie Sicherheitsregeln (nie Force-Push, keine Geheimnisse im Repo). Ergänzt `learncenter-ios-git` (Sonderfall LearnCenter-iOS). SKIP für Kundenwebsites (liegen in iCloud, siehe `client-website-standards`).
---

# Software-Projekt-Ablauf (DE)

Der Nutzer baut Software mit KI und ist kein erfahrener Coder. Git/GitHub nimmt Claude ihm ab. Er will aber, dass **jeder Stand gesichert ist, man jederzeit zurückgehen kann und Claude immer weiß, wie das funktioniert**. Dieser Skill ist die feste Vorgehensweise dafür.

## Grundregeln
1. **Ein Ordner = ein Projekt = ein Repo**, direkt unter `~/development/<Projektname>/`. Siehe Memory `project_dev_structure`.
2. **Repos sind privat.** Öffentlich wird nur, was der Nutzer ausdrücklich freigibt (derzeit höchstens das Profil-Repo `<owner>/<profile-repo>`). Siehe Memory `feedback_github_visibility`.
3. **Lokal ist die Arbeitskopie, GitHub ist Sicherung und Verlauf.** Xcode und Co. bauen aus dem lokalen Ordner. Nie vorschlagen, einen lokalen Ordner zu löschen, nur weil er gepusht ist. Auf einem neuen Rechner: `git clone` holt alles zurück.
4. **Sprache im Projekt: Englisch** (README, Docs, Commit-Texte, Beschreibungen). Mit dem Nutzer wird Deutsch gesprochen. Siehe Memory `feedback_english_projects`.
5. **Kein Geheimnis im Repo** (API-Keys, `.env`, `.p8`, Passwörter). `.env` und Schlüsseldateien in `.gitignore`, im Repo nur `.env.example`. Vor dem ersten Push mit `git ls-files` und einer Suche nach `sk-`, `BEGIN PRIVATE KEY`, `.env`, `.p8` prüfen.

## Neues Projekt anlegen
1. Ordner unter `~/development/<Name>/`, `git init -b main`.
2. `.gitignore` passend zum Stack (Xcode: `build/`, `DerivedData`, `xcuserdata`; Node: `node_modules`, `.env`).
3. `README.md` (was, Stack, Starten, Stand) und `docs/STATUS.md` (Tabelle Implemented / Concept / Gap).
4. Erster Commit, dann `gh repo create <owner>/<Name> --private --source=. --push`. Beschreibung und Topics setzen (`ios`, `swiftui`, `nextjs`, `website` usw.). Websites erhalten das Topic `website` und, wenn eigenes Repo, den Namenspräfix `web-`.
5. Eintrag in Notion (Skill `notion-task-logging`) und Memory ergänzen.

## Im laufenden Projekt: nach jeder abgeschlossenen Änderung
1. `git status` ansehen, nur Gewolltes hinzufügen (kein blindes `git add -A`, wenn Fremddateien herumliegen).
2. Commit: kurze Zeile im Imperativ auf Englisch, am Ende die Co-Authored-By-Zeile aus dem aktuellen Attributions-Hinweis.
3. **Sofort pushen** (`git push`). Vorher Fast-Forward prüfen: `git fetch origin` und `git merge-base --is-ancestor origin/<branch> HEAD`. Nicht erfüllt: nicht pushen, der Nutzer informieren.
4. **Nie `--force`**, nie die Historie umschreiben, ohne dass der Nutzer es ausdrücklich verlangt.
5. Wenn sich ein sichtbares Feature ändert: `docs/STATUS.md` mitpflegen. Bei wesentlicher Änderung der Oberfläche die Screenshots im README erneuern.
6. Nach dem Push kurz bestätigen (`git log --oneline origin/<branch> -1`).

## Branches und Zurückgehen: so erklärt man es dem Nutzer
- **Commit** = ein gespeicherter Stand mit Beschreibung. Wie ein Speicherpunkt im Spiel. Jeder bleibt erhalten.
- **Branch ("Strang")** = eine parallele Linie von Ständen. `main` ist der stabile Hauptstrang. Für Experimente oder größere Umbauten einen eigenen Branch anlegen (`git switch -c experiment-name`), damit `main` heil bleibt. Gefällt das Ergebnis, wird der Branch in `main` zusammengeführt (merge), sonst wird er verworfen.
- **Tag** = ein Lesezeichen auf einem wichtigen Stand, z.B. `v1.0-testflight-build-11`. Vor großen Umbauten und bei jedem TestFlight-/Store-Upload einen Tag setzen und pushen.
- **Zurückgehen ohne etwas zu verlieren:**
  - Einen einzelnen schlechten Commit rückgängig machen: `git revert <commit>` (legt einen neuen Commit an, der Verlauf bleibt).
  - Nur ansehen, wie es früher war: `git switch --detach <commit-oder-tag>`, danach `git switch -` zurück.
  - Ab einem alten Stand neu weiterarbeiten: neuen Branch von dort anlegen (`git switch -c retry <commit-oder-tag>`).
  - Verboten ohne ausdrückliche Bitte: `git reset --hard` und Force-Push. Sie können Arbeit endgültig löschen.
- Vor jedem riskanten Schritt kurz sagen, was passiert und dass nichts verloren geht, in einfachen Worten und mit konkretem Vorher/Nachher.

## Sonderfälle
- **LearnCenter-iOS:** lokaler Branch heißt `Testcode`, Push mit `git push origin Testcode:main`. Siehe Skill `learncenter-ios-git`.
- **GFP-Calculator:** `main` = Web-Prototyp, `ios-native` = SwiftUI-Rewrite. Vor Commits den aktiven Branch prüfen.
- **Kundenwebsites und Akquise-Demos:** nicht in GitHub-Projekt-Repos, siehe `client-website-standards`. Eine private Sicherung ist als Aufgabe geplant (Notion).
- **Skills und KI-Setup:** liegen in iCloud (`AI/Claude/Skills`) als Original; die Kopie im privaten Repo wird mit einem Sync-Skript einseitig nachgezogen (iCloud → Repo), nie umgekehrt.
