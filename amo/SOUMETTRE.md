# Envoyer Grok Night sur AMO — dans l’ordre

Compte : le même que Firefox Sync (compte Mozilla). Si tu n’en as pas : https://accounts.firefox.com

1. Ouvre https://addons.mozilla.org/developers/addon/submit/distribution
2. Choisis **On this site** (listé sur AMO) — c’est ça qui donne l’install en un clic.
3. Type de module : **Thème** (Theme), pas Extension.
4. Envoie le fichier `dist/grok-night.xpi`  
   (si tu n’en as pas : `cd ~/github/firefox-theme-grok && ./scripts/build.sh`)
5. L’ID doit rester `grok-night@ledutheo`. Ne le change pas.
6. Colle le texte de `amo/listing.md` :
   - nom : Grok Night
   - résumé FR / EN
   - description FR / EN
   - homepage : `https://github.com/ledutheo/firefox-theme-grok`
7. Captures (1280×800) : `docs/img/hero.png`, puis `docs/img/menu.png` si ça en demande une 2e.
8. Catégorie : Appearance. Licence : MIT (déjà dans le dépôt).
9. **Non** : theme experiment, collecte de données, code source séparé (un thème n’en a pas besoin).
10. Soumets.

Ensuite Mozilla scanne et signe. Thème sans scripts = revue courte, souvent automatique. Tu reçois un mail. L’URL publique ressemblera à :

`https://addons.mozilla.org/firefox/addon/…`

Si un reviewer bloque le mot « Grok » (marque) : réponds que c’est un fan theme, disclaimer dans la fiche, marque originale (étoile), pas le logo xAI. Si ça ne passe pas, on renomme (ex. Night Spark) et on republie — l’ID peut rester.

Firefox Release n’installera le thème **en permanent** qu’après cette signature.
