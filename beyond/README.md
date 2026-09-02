# Au-delà du thème statique

Un thème Firefox signé **ne peut pas** embarquer de scripts. La clé `"theme"` dans `manifest.json` classifie l'addon comme thème : le reste (background, permissions, content scripts) est ignoré.

Ce dossier montre les trois vrais étages au-dessus, dans l'ordre de violence :

| Étage | Où | Pour qui | Plafond |
|-------|----|----------|---------|
| 1. Thème statique | `theme/` | tout le monde | couleurs + images + `dark_theme` |
| 2. `browser.theme` | `beyond/dynamic/` | extension signée, permission `theme` | changer le thème à l'heure, par fenêtre |
| 3. `theme_experiment` | `beyond/theme_experiment/` | Nightly / pref `extensions.experiments.enabled` | n'importe quelle variable CSS chrome |
| 4. `userChrome.css` | `beyond/userChrome/` | un profil, `toolkit.legacyUserProfileCustomizations.stylesheets` | tout le chrome, hors AMO |

Android (Fennec) : `beyond/android/`.

**Nouvel onglet** (`beyond/newtab/`) : un thème ne peut pas remplacer `about:newtab`. Second module, `chrome_url_overrides`.
