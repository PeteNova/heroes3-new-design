# Heroes III — New Design

Fanowski remaster wizualny portretów bohaterów Heroes of Might and Magic III na **VCMI**. Ta sama gra, odświeżona oprawa.

- **Strona:** https://petenova.github.io/heroes3-new-design/
- **Repozytorium:** https://github.com/PeteNova/heroes3-new-design

To repozytorium to **publiczna strona dystrybucji** (katalog `mods-site/` z projektu nadrzędnego). Pipeline artystyczny — mastery, oryginalne ekstrakty z gry, skrypty i playtest — zostaje lokalnie i nie jest tu publikowany.

To **nie jest pipeline artystyczny** i nie zmienia mechaniki gry. Służy do prezentacji i pobierania gotowych, wizualnych modów VCMI.

## Dla kogo

Fani Heroes of Might and Magic III, którzy grają na **VCMI** i chcą odświeżonych portretów bez ruszania rozgrywki.

## Co oddajemy

Statyczną stronę internetową (v1 bez backendu):

- prezentacja każdego moda (frakcja, zawartość, contact sheet, skład);
- pobieranie paczek ZIP gotowych do wrzucenia do katalogu `Mods` VCMI;
- kopia, którą można otworzyć lokalnie (`index.html`) albo oglądać na GitHub Pages.

Zasady artystyczne nadal obowiązują w projekcie nadrzędnym. Ta strona pokazuje skończone paczki VCMI i wybrane contact sheety — nie zawiera źródeł pipeline’u.

## Relacja do projektu nadrzędnego

| To repozytorium | Projekt nadrzędny (lokalnie) |
|---|---|
| strona, ZIP-y, copy dla fanów | `CONCEPT.md`, mastery, skrypty, playtest, deploy |
| katalog danych `mods.json` | `build/` + `docs/*_PORTRAITS_V1.md` |
| nie rusza instalacji GOG | pipeline F1 i dalej |

Gdy nowa frakcja przejdzie akceptację i paczkę VCMI, dopisujesz ją w `mods.json`, kopiujesz contact sheet do `assets/sheets/` i odpalasz:

```powershell
powershell -File scripts/sync-mods-data.ps1
powershell -File scripts/pack-downloads.ps1
```

Skrypt ZIP-ów czyta paczki z katalogu nadrzędnego `build/` (lokalny pipeline). W samym klonie GitHuba tych źródeł nie ma — tu leżą już gotowe `downloads/*.zip`.

## Uruchomienie

Otwórz w przeglądarce:

```text
index.html
```

Albo wejdź na https://petenova.github.io/heroes3-new-design/. Działa offline (ścieżki względne, dane w `js/mods-data.js`).

## Struktura

```text
index.html
mods.json              źródło katalogu modów
css/site.css
js/app.js
js/mods-data.js        kopia katalogu pod file://
assets/sheets/         contact sheety do prezentacji
downloads/             ZIP-y VCMI
scripts/pack-downloads.ps1
README.md
ROADMAP.md
```

## Uwaga prawna

Fanowski remaster wizualny. Nie jest oficjalnym produktem 3DO / New World Computing / Ubisoft. Użytkownik musi posiadać oryginalne Heroes III oraz VCMI.
