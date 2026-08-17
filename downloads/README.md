# Paczki do pobrania

Ten katalog trzyma gotowe ZIP-y modów VCMI, które strona podaje fanom.

## Jak odświeżyć ZIP-y

Z katalogu głównego repozytorium:

```powershell
powershell -File mods-site/scripts/pack-downloads.ps1
```

Skrypt czyta wyłącznie `build/vcmi-hero-portraits-*-v1/` i nie rusza instalacji gry ani plików pipeline’u w `work/`.

## Co jest w ZIP-ie

Każde archiwum ma w korzeniu folder gotowy do wrzucenia do katalogu `Mods` VCMI, np.:

```text
heroes3-new-design-portraits-castle-v1/
  mod.json
  Content/
```

Nazwy folderów odpowiadają wdrożeniom w projekcie nadrzędnym (`Mods/heroes3-new-design-portraits-<frakcja>-v1`).

## Czego tu nie ma

- Bohaterowie specjalni/kampanijni — jeszcze nie zbudowane.
- Piloty UI (`townqvbk`) — nie są publicznym modem fanowskim w v1 strony.
