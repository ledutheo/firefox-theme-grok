# Soumettre Grok Void — **nouveau compte Mozilla**

L’ancien compte a déjà déposé l’ID `grok-night@ledutheo`. Même supprimé, Mozilla **garde** cet ID. D’où *Duplicate add-on ID found*.

Ce dépôt utilise maintenant :

- **ID** `{509635ca-327f-493d-a156-277548d25172}`
- **Nom AMO** `Grok Void`
- **Version** `2.0.0` (première soumission de *ce* listing)

Ce n’est **pas** une mise à jour de l’ancien thème. C’est un **nouveau** add-on.

## Ordre

1. Connecte-toi avec le **nouveau** compte : https://addons.mozilla.org/developers/
2. **Submit a new add-on** (pas « upload new version » sur l’ancien).
3. Distribution : **On this site**.
4. Type : **Thème**.
5. Fichier : `~/github/firefox-theme-grok/dist/grok-night.xpi`  
   (`cd ~/github/firefox-theme-grok && ./scripts/build.sh` si besoin)
6. Vérifie que l’ID affiché est `{509635ca-327f-493d-a156-277548d25172}`.
7. Colle `amo/listing.md` (nom **Grok Void**, pas Grok Night).
8. Captures : `docs/img/hero.png`, éventuellement `docs/img/menu.png`.
9. Appearance, MIT, pas d’expérience, pas de collecte.
10. Soumets.

Si ça dit encore duplicate ID : tu n’as pas le XPI 2.0.0 (l’ancien ID est encore dans le zip). Rebuild, réessaie.
