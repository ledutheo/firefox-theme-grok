<p align="center">
  <img src="docs/img/icon-128.png" width="96" height="96" alt="Grok Night">
</p>

<h1 align="center">GROK NIGHT</h1>

<p align="center">
  L’appli <a href="https://grok.com">Grok</a>. Dans Firefox.<br>
  Pour les fans — et pour ceux qui n’ont pas encore compris.
</p>

<p align="center">
  <img src="docs/img/hero.png" alt="Grok Night dans Firefox" width="100%">
</p>

<p align="center">
  <a href="https://ledutheo.github.io/firefox-theme-grok/">landing + vidéo</a>
  ·
  <a href="https://github.com/ledutheo/firefox-theme-grok/releases">XPI</a>
</p>

## Installer

1. `about:debugging#/runtime/this-firefox`
2. **Charger un module temporaire**
3. `theme/manifest.json`

```bash
git clone git@github.com:ledutheo/firefox-theme-grok.git
cd firefox-theme-grok
```

Permanent : `./scripts/build.sh` → `dist/grok-night.xpi` sur [AMO](https://addons.mozilla.org/developers/). Texte prêt : [`amo/listing.md`](amo/listing.md). XPI déjà coupé : [Releases](https://github.com/ledutheo/firefox-theme-grok/releases) (Firefox Release le refuse non signé ; ESR / Dev / `about:debugging` OK).

Aller plus loin dans le chrome : `./scripts/install-userchrome.sh`

## Le chrome

Void `#0A0A0A`. Barres `#141414`. Texte `#FCFCFC`. Une étincelle `#FF6B35`.  
Pas un sticker sur chaque fenêtre : étoiles, halo, petite marque. Grok est du silence — le navigateur aussi.

Les sites restent les sites. Le chrome Firefox, lui, est à nous.

## Plus loin

Un thème statique s’arrête aux couleurs. Le reste est dans [`beyond/`](beyond/) : jour/nuit à l’horloge, `theme_experiment`, `userChrome`, Fennec.

## English

Grok, in Firefox. For fans — and for anyone who hasn’t figured it out yet.  
Load `theme/manifest.json` from `about:debugging`.

## Licence

MIT · [ledutheo](https://github.com/ledutheo) · [preview](https://ledutheo.github.io/firefox-theme-grok/)  
Fan theme. Not an xAI release.
