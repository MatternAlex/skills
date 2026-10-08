---
name: learncenter-ios-git
description: TRIGGER — immer lesen und danach handeln, wenn im Repo `~/development/LearnCenter-iOS` ein `git commit` erstellt wurde (egal ob Bugfix, Feature, Design-Änderung oder Doku). Auslöser u.a. jede eigene `git commit`-Ausführung in diesem Repo während einer Coding-Session, "committe das", "speichere das", "behebe diese code sachen". Deckt die Pflicht ab, direkt danach auch zu pushen (`git push`), damit der Stand nicht nur lokal liegt, sowie den Zielbranch (`origin/main`) und die Fast-Forward-Sicherheitsprüfung davor.
---

# LearnCenter iOS — Commits gehören nach GitHub (DE)

## Regel
Nach **jedem** `git commit` im Repo `~/development/LearnCenter-iOS` (unabhängig vom Anlass — Bugfix, neues Feature, Design-Anpassung, Algorithmus-Änderung, Dokumentation) direkt im Anschluss `git push` ausführen, damit der Stand auch auf GitHub landet und nicht nur lokal liegen bleibt. Gilt für die gesamte Session, nicht nur für explizit als "fertig" markierte Arbeit — Der Nutzer hat ausdrücklich festgelegt, dass jeder Commit auch tatsächlich in GitHub gespeichert sein soll.

## Zielbranch
- Remote: `origin` → `git@github.com:<owner>/LearnCenter-iOS.git`.
- Push-Ziel ist `main` auf GitHub. Der lokale Arbeitsbranch heißt `Testcode` (historisch gewachsener Name, nicht umbenannt) — er wird mit `git push origin Testcode:main` (bzw. nach `git branch -u origin/main` einfach `git push`) auf `origin/main` gepusht.
- Es existiert zusätzlich ein lokaler Branch `main`, der veraltet/verwaist ist (steht auf einem alten "Initial commit") — **nicht** verwechseln mit `origin/main`. Für Ancestry-Prüfungen immer gegen `origin/main` vergleichen, nie gegen den lokalen `main`-Branch.

## Sicherheitsprüfung vor dem Push
Vor einem Push immer erst prüfen, dass es sich um einen reinen Fast-Forward handelt (keine force-push-Situation):
```
git fetch origin
git merge-base --is-ancestor origin/main HEAD && echo "fast-forward safe"
```
Falls das **nicht** zutrifft (Historien sind auseinandergelaufen), NICHT einfach pushen oder gar force-pushen — das widerspricht der generellen Git-Sicherheitsregel (kein Force-Push ohne explizite Anfrage). Stattdessen der Nutzer kurz informieren und gemeinsam klären, wie die Historien zusammengeführt werden sollen.

## Ablauf
1. Nach dem `git commit` (oder mehreren zusammengehörigen Commits einer Aufgabe): `git fetch origin` + Ancestry-Check wie oben.
2. Bei bestätigtem Fast-Forward: `git push origin Testcode:main`.
3. Kurz bestätigen, dass der Push durchgelaufen ist (z. B. `git log --oneline origin/main -1`).

## Kontext
Am 23.07.2026 wurde festgestellt, dass mehrere Sessions lang ausschließlich lokal auf dem Branch `Testcode` committet wurde, ohne jemals zu pushen — `origin/main` auf GitHub war dadurch 12+ Commits im Rückstand. Nach Rücksprache mit dem Nutzer wurde der volle Stand per Fast-Forward auf `origin/main` gepusht; dieser Skill soll verhindern, dass sich das wiederholt.
