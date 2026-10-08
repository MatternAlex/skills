---
name: testflight-upload
description: TRIGGER — immer lesen, wenn ein neuer Build von LearnCenter iOS an TestFlight hochgeladen werden soll. Auslöser u.a. "/testflight-upload", "TestFlight hochladen", "neuen Build hochladen", "Beta hochladen", "LearnCenter für TestFlight bauen", "Upload zu App Store Connect". Deckt den kompletten Ablauf über die fastlane-Lane `beta` ab (Build-Nummer erhöhen, Archivieren/Signieren via App-Store-Connect-API-Key statt Apple-ID-Login, Export als .ipa, Upload via pilot) sowie das Troubleshooting für fehlende App-ID-Capabilities (`sync_capabilities`-Lane).
---

# TestFlight-Upload für LearnCenter iOS

## Projekt
`~/development/LearnCenter-iOS/LearnCenter_iOS` (seit der Ordner-Reorg vom 2026-07-09 — Repo-Root ist `LearnCenter-iOS/`, Xcode-Projekt liegt eine Ebene tiefer)

App-ID: `<bundle-id>` · Team-ID: `<TEAM_ID>` · fastlane-Setup in `fastlane/Fastfile`.

## Voraussetzung (einmalig, sollte bereits erledigt sein)
- App Store Connect API Key liegt unter `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`.
- Key ID (`<KEY_ID>`) und Issuer ID sind in `fastlane/Fastfile` hinterlegt (`API_KEY_ID`, `ISSUER_ID`).
- Optionale `.secrets`-Datei im Projekt-Root (für `scripts/testflight-upload.sh`) ist in `.gitignore` eingetragen — nie committen.

## Ablauf
1. In den Projektordner wechseln.
2. `fastlane beta` ausführen (oder `./scripts/testflight-upload.sh`).
3. Die Lane macht automatisch:
   - `increment_build_number` (Build-Nummer = Anzahl Commits + 5, bzw. `GITHUB_RUN_NUMBER` in CI).
   - `gym`: Archiv + Export im Release-Modus, **automatische Signierung über den App-Store-Connect-API-Key** (`-authenticationKeyPath/-authenticationKeyID/-authenticationKeyIssuerID` in `xcargs`) — bewusst kein interaktiver Apple-ID-Login, da der in der Vergangenheit mit einer alten/abgelehnten Apple-ID fehlgeschlagen ist.
   - `pilot`: Upload der `.ipa` nach TestFlight, Changelog = letzte Commit-Message.
4. fastlane baut vom **aktuellen Arbeitsverzeichnis-Stand**, nicht von einem Commit — uncommittete Änderungen werden mit eingebaut. Bei Bedarf vorher fragen, ob committet werden soll.

## Troubleshooting: „Provisioning profile doesn't include …“
Wenn der Archiv-Schritt mit einer Meldung wie
`Provisioning profile "..." doesn't include the com.apple.developer.applesignin entitlement`
fehlschlägt, fehlt eine Capability auf der App-ID in App Store Connect (z. B. weil ein neues Entitlement wie Sign-in-with-Apple im Xcode-Projekt hinzugekommen ist, aber auf der Bundle-ID noch nicht freigeschaltet wurde).

Fix: `fastlane ios sync_capabilities` ausführen (eigene Lane in `Fastfile`, nutzt `Spaceship::ConnectAPI::BundleIdCapability.create` mit dem API-Key). Aktuell schaltet sie „Sign In with Apple“ frei. Falls weitere Entitlements dazukommen, die Lane entsprechend um weitere `capability_type`/`settings`-Blöcke erweitern (Referenz für die Settings-Struktur: `produce/lib/produce/service.rb` im fastlane-Gem, Methode `build_settings_for`).

Wichtig: Für Capability-Änderungen funktioniert nur `Spaceship::ConnectAPI::BundleIdCapability.create` rein mit API-Key-Auth. Die vermeintlich naheliegende `bundle_id.update_capability(...)`-Methode (PATCH) ruft intern noch die alte, Cookie-basierte `Spaceship::Client#team_id` auf und verlangt einen Apple-ID-Login — dort daher nicht nutzen.

## Sonstige Fehlerbilder
- „Unable to log in with account '...'" beim Archivieren → die `-authenticationKey*`-Flags fehlen in `xcargs` oder zeigen auf eine falsche/fehlende `.p8`-Datei.
- `fastlane ios setup` einmalig ausführen, falls die App noch nicht in App Store Connect existiert.
