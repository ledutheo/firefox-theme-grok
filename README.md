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

Permanent : **nouveau compte Mozilla** — ID `{509635ca-327f-493d-a156-277548d25172}`, nom AMO **Grok Void**. Marche : [`amo/SOUMETTRE.md`](amo/SOUMETTRE.md). Ne plus utiliser `grok-night@ledutheo` (compte supprimé, ID déjà pris).

Aller plus loin dans le chrome : `./scripts/install-userchrome.sh`

## Le chrome

Chrome **noir / blanc**, comme le style du logo. La seule couleur, c’est le **trou noir** (disque d’accrétion) à droite des onglets et en icône.

Un thème ne peut **pas** coller un fond + du texte sur `about:newtab`. Pour ça : second module `beyond/newtab/` (raccourcis grok.com / Grok Build). Même `about:debugging`, fichier `beyond/newtab/manifest.json`.

Les sites restent les sites. Le chrome Firefox, lui, est à nous.

## Plus loin

Un thème statique s’arrête aux couleurs. Le reste est dans [`beyond/`](beyond/) : jour/nuit à l’horloge, `theme_experiment`, `userChrome`, Fennec.

## English

Grok, in Firefox. For fans — and for anyone who hasn’t figured it out yet.  
Load `theme/manifest.json` from `about:debugging`.

## Licence

MIT · [ledutheo](https://github.com/ledutheo) · [preview](https://ledutheo.github.io/firefox-theme-grok/)  
Fan theme. Not an xAI release.
