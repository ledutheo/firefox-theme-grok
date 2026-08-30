# Grok Night

Thème Firefox aux couleurs de [grok.com](https://grok.com) : chrome noir, texte blanc, accent orange. Simple à installer, écrit pour aller jusqu’au bout du format.

Pas un produit xAI. Marque originale (étoile + noyau orange).

## Installer (30 secondes)

Firefox Release refuse un XPI non signé en permanent. Le chargement temporaire marche toujours :

1. `about:debugging#/runtime/this-firefox`
2. **Charger un module temporaire**
3. choisir `theme/manifest.json`

Ou :

```bash
cd ~/github/firefox-theme-grok
./scripts/build.sh          # régénère images + dist/grok-night.xpi
./scripts/install-firefox.sh
```

Pour du permanent : soumettre `dist/grok-night.xpi` sur [addons.mozilla.org](https://addons.mozilla.org/developers/) (thème listé ou unlisted signé).

Preview hors Firefox : ouvrir `preview.html`.

## Ce que le thème fait

Tout ce que le schéma officiel `theme.json` (Firefox 154 / searchfox) autorise sur un thème **statique** :

| Clé | Rôle |
|-----|------|
| `theme.colors.*` | les 40 couleurs chrome (onglets, toolbar, urlbar, popups, ntp, sidebar) |
| `theme.images.theme_frame` | header 3000×200 |
| `theme.images.additional_backgrounds` | halo orange (max 15 calques) |
| `theme.properties.color_scheme` | `dark` pour about: / chrome |
| `theme.properties.content_color_scheme` | `auto` — les sites restent les sites |
| `dark_theme` | même nuit si l’OS est sombre |
| `gecko` + `gecko_android` | desktop **et** Fennec / Firefox Android |
| `_locales/fr` + `en` | nom / description |

Les commentaires `//` dans `theme/manifest.json` documentent chaque propriété, y compris celles qu’on n’active pas (gradients CSS, `headerURL` mort depuis FF70, `toolbar_field_separator` ignoré depuis FF89).

Couleurs : `src/palette.json`. Images : `python3 src/generate.py`.

## Ce qu’un thème statique ne peut pas faire

Dès que `"theme"` est dans le manifest, Firefox **ignore** scripts et permissions. Les étages au-dessus sont dans `beyond/` :

1. **`beyond/dynamic/`** — extension (permission `theme`) qui appelle `browser.theme.update()` Jour/Nuit selon l’heure.
2. **`beyond/theme_experiment/`** — Nightly, pref `extensions.experiments.enabled`. Accroche n’importe quel sélecteur chrome.
3. **`beyond/userChrome/`** — CSS de profil, pref `toolkit.legacyUserProfileCustomizations.stylesheets`.
4. **`beyond/android/`** — Fennec : `gecko_android` est obligatoire pour AMO, l’effet chrome y reste mince.

## Android / Fennec

Le manifest déclare `gecko_android` (min 120). Sur Fennec F-Droid ça autorise l’install depuis AMO. Le chrome Fenix n’est pas Proton : n’attends pas le header 3000×200. Détail : `beyond/android/FENNEC.md`.

## AMO

- Type : **Thème** (pas extension).
- ID figé : `grok-night@ledutheo`.
- ZIP = contenu de `theme/`, pas le dossier parent (`scripts/build.sh` le fait).
- `theme_experiment` volontairement **absent** du paquet listé.

## Licence

MIT. Couleurs observées sur grok.com / xAI, pas une charte officielle.
