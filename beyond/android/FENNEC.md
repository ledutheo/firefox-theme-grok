# Android / Fennec

Bill utilise **Fennec F-Droid** (`org.mozilla.fennec_fdroid`) sur TCL 60 SE.

## Ce que Firefox Android fait vraiment

Le chrome Fenix n’est **pas** le chrome desktop. Un thème WebExtension :

- doit déclarer `browser_specific_settings.gecko_android` sinon AMO ne le liste pas pour Android ;
- **doit** utiliser `#RRGGBB` ou des tableaux RGB — pas `black`, pas `#FFF`, pas `#RRGGBBAA` ;
- ne repeint qu’une petite partie de l’UI (souvent `frame` / barre, parfois `tab_*` selon le fork et la version) ;
- ignore `theme_experiment`, `userChrome.css`, `additional_backgrounds` dans la pratique Fenix ;
- n’a pas de sidebar, pas de `about:newtab` desktop, pas de proton toolbars.

Fennec F-Droid (fork Fenix) est plus souple sur **les extensions**, pas sur le moteur de thèmes. Ne pas attendre un clone du header 3000×200.

## Installer le thème sur Fennec

1. Publier le thème sur AMO (signé) **avec** `gecko_android`, puis l’ouvrir depuis addons.mozilla.org version desktop dans Fennec.
2. Ou, en debug : `web-ext run -t firefox-android --firefox-apk org.mozilla.fennec_fdroid` (câble + `adb`).

Sans signature Mozilla, Fennec release refuse l’XPI comme Firefox desktop release.

## Ce que Fenix theme lui-même

Le dark/light de Fennec, c’est `FirefoxTheme` côté app (Kotlin/Compose), pas le manifest d’un addon. On ne le remplace pas avec ce dépôt.

`images/android_status.png` est un bandeau 1080×80 au cas où un fork appliquerait `theme_frame`. Inoffensif s’il est ignoré.
