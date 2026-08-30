/* Applique Grok Night (19h–7h) ou Grok Day (7h–19h).
 *
 * API : browser.theme.update([windowId,] details)
 *       browser.theme.reset([windowId])
 *       browser.theme.getCurrent([windowId])
 *       browser.theme.onUpdated
 *
 * windowId omis = toutes les fenêtres.
 * Une fenêtre peut avoir son propre thème.
 *
 * Les images doivent être des URL d'extension (relatives au manifest)
 * ou de l'ImageData. Ici on pointe vers le thème statique voisin :
 * ce paquet dynamique n'est PAS autonome — copier theme/images/ + icons
 * à côté, ou charger via about:debugging depuis beyond/dynamic/ après
 * le script scripts/prep-dynamic.sh.
 */

const NIGHT = {
  images: {
    theme_frame: "images/theme_frame.png",
    additional_backgrounds: ["images/glow.png"],
  },
  properties: {
    backgrounds_area: "top_toolbars",
    additional_backgrounds_alignment: ["right top"],
    additional_backgrounds_tiling: ["no-repeat"],
    color_scheme: "dark",
    content_color_scheme: "auto",
  },
  colors: {
    frame: "#0A0A0A",
    frame_inactive: "#0C0C0C",
    tab_background_text: "#9E9E9E",
    tab_background_separator: "#2A2A2A",
    tab_text: "#FCFCFC",
    tab_line: "#FF6B35",
    tab_loading: "#FF6B35",
    tab_selected: "#141414",
    toolbar: "#141414",
    toolbar_text: "#FCFCFC",
    bookmark_text: "#FCFCFC",
    toolbar_field: "#111111",
    toolbar_field_text: "#FCFCFC",
    toolbar_field_border: "#2A2A2A",
    toolbar_field_focus: "#1A1A1A",
    toolbar_field_text_focus: "#FCFCFC",
    toolbar_field_border_focus: "#FF6B35",
    toolbar_field_highlight: "#FF6B35",
    toolbar_field_highlight_text: "#0A0A0A",
    icons: "#FCFCFC",
    icons_attention: "#FF6B35",
    button_background_hover: "#242424",
    button_background_active: "#2A2A2A",
    popup: "#1A1A1A",
    popup_text: "#FCFCFC",
    popup_border: "#2A2A2A",
    popup_highlight: "#FF6B35",
    popup_highlight_text: "#0A0A0A",
    ntp_background: "#0A0A0A",
    ntp_card_background: "#1A1A1A",
    ntp_text: "#FCFCFC",
    sidebar: "#141414",
    sidebar_border: "#2A2A2A",
    sidebar_text: "#FCFCFC",
    sidebar_highlight: "#FF6B35",
    sidebar_highlight_text: "#0A0A0A",
  },
};

const DAY = {
  images: {
    theme_frame: "images/theme_frame_day.png",
  },
  properties: {
    backgrounds_area: "top_toolbars",
    color_scheme: "light",
    content_color_scheme: "auto",
  },
  colors: {
    frame: "#EEEEEE",
    frame_inactive: "#E4E4E4",
    tab_background_text: "#4A4A4A",
    tab_background_separator: "#D0D0D0",
    tab_text: "#141414",
    tab_line: "#CF5200",
    tab_loading: "#FF6B35",
    tab_selected: "#FFFFFF",
    toolbar: "#FFFFFF",
    toolbar_text: "#141414",
    bookmark_text: "#141414",
    toolbar_top_separator: "#EEEEEE",
    toolbar_bottom_separator: "#D0D0D0",
    toolbar_vertical_separator: "#D0D0D0",
    toolbar_field: "#FFFFFF",
    toolbar_field_text: "#141414",
    toolbar_field_border: "#D0D0D0",
    toolbar_field_focus: "#FFFFFF",
    toolbar_field_text_focus: "#141414",
    toolbar_field_border_focus: "#CF5200",
    toolbar_field_highlight: "#FF6B35",
    toolbar_field_highlight_text: "#0A0A0A",
    icons: "#141414",
    icons_attention: "#CF5200",
    button_background_hover: "#E4E4E4",
    button_background_active: "#D0D0D0",
    popup: "#FFFFFF",
    popup_text: "#141414",
    popup_border: "#D0D0D0",
    popup_highlight: "#FF6B35",
    popup_highlight_text: "#0A0A0A",
    ntp_background: "#F5F5F5",
    ntp_card_background: "#FFFFFF",
    ntp_text: "#141414",
    sidebar: "#F5F5F5",
    sidebar_border: "#D0D0D0",
    sidebar_text: "#141414",
    sidebar_highlight: "#FF6B35",
    sidebar_highlight_text: "#0A0A0A",
  },
};

function isDay(date = new Date()) {
  const h = date.getHours();
  return h >= 7 && h < 19;
}

async function apply() {
  await browser.theme.update(isDay() ? DAY : NIGHT);
}

browser.runtime.onStartup.addListener(apply);
browser.runtime.onInstalled.addListener(apply);
browser.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "grok-tick") apply();
});

browser.alarms.create("grok-tick", { periodInMinutes: 15 });
apply();
