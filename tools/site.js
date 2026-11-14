/* One settings store for the whole lecture, modelled on LA-Helper's i18n.js
   and its theme switch. A single click changes the language or the theme
   everywhere: every element on this page, every dynamic widget, every other
   page, and every other open tab. No page keeps a private copy of the choice.

     lang  "zh" = English sheet + Chinese annotations (default)
           "en" = English-only exam view
     theme follows the OS until the reader picks light/dark explicitly

   Loaded synchronously in <head>, so attributes are set before the first
   paint and a remembered dark mode never flashes white. localStorage keeps
   the choice; the "storage" event is what makes other tabs follow instantly.
   ?lang=en / ?theme=dark give shareable links without overwriting the choice.
*/
(function () {
  "use strict";

  var LANG_KEY = "stats-cheatsheet-lang";
  var THEME_KEY = "stats-cheatsheet-theme";
  // Button labels are NOT written by JS: the nav renders both halves (.zh /
  // .en-only) and CSS picks the right one from data-lang / data-theme. That
  // way the very first paint is already correct, with no text flash.

  function lsGet(k) {
    try { return window.localStorage.getItem(k); } catch (e) { return null; }
  }
  function lsSet(k, v) {
    try { window.localStorage.setItem(k, v); } catch (e) { /* private mode */ }
  }
  function param(name) {
    try { return new URLSearchParams(window.location.search).get(name); } catch (e) { return null; }
  }
  function normLang(v) { return v === "en" ? "en" : "zh"; }
  function normTheme(v) { return v === "dark" || v === "light" ? v : null; }
  function systemTheme() {
    try {
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    } catch (e) { return "light"; }
  }

  var lang = normLang(param("lang") || lsGet(LANG_KEY) || "zh");
  var theme = normTheme(param("theme")) || normTheme(lsGet(THEME_KEY)) || systemTheme();
  var baseTitle = document.title || "Stats Cheat Sheet";
  var listeners = [];
  var uiReady = false;

  function state() { return { lang: lang, theme: theme }; }

  function syncUI() {
    // The visible labels come from CSS; JS only keeps the accessibility state
    // in step with the central store.
    var langBtn = document.getElementById("langToggle");
    if (langBtn) {
      langBtn.setAttribute("aria-pressed", lang === "en" ? "true" : "false");
      langBtn.title = lang === "en"
        ? "Show the Chinese annotations again"
        : "Hide the Chinese annotations (English-only exam view)";
    }
    var themeBtn = document.getElementById("themeToggle");
    if (themeBtn) {
      themeBtn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      themeBtn.title = theme === "dark" ? "Switch to the light theme" : "Switch to the dark theme";
    }
  }

  function apply() {
    var root = document.documentElement;
    root.setAttribute("data-lang", lang);
    root.setAttribute("data-theme", theme);
    root.setAttribute("lang", lang === "zh" ? "zh-CN" : "en");
    document.title = lang === "zh" ? baseTitle + " · 中英对照" : baseTitle;
    if (uiReady) syncUI();
    for (var i = 0; i < listeners.length; i++) {
      try { listeners[i](state()); } catch (e) { /* one bad subscriber must not stop the rest */ }
    }
    if (uiReady && window.CustomEvent) {
      document.dispatchEvent(new CustomEvent("stats:settingschange", { detail: state() }));
    }
  }

  function setLang(v, persist) {
    lang = normLang(v);
    if (persist !== false) lsSet(LANG_KEY, lang);
    apply();
  }
  function toggleLang() { setLang(lang === "en" ? "zh" : "en", true); }
  function setTheme(v, persist) {
    theme = normTheme(v) || systemTheme();
    if (persist !== false) lsSet(THEME_KEY, theme);
    apply();
  }
  function toggleTheme() { setTheme(theme === "dark" ? "light" : "dark", true); }
  function onChange(fn) {
    listeners.push(fn);
    try { fn(state()); } catch (e) {}
  }

  window.StatsSettings = {
    get: state,
    lang: function () { return lang; },
    theme: function () { return theme; },
    setLang: setLang,
    toggleLang: toggleLang,
    setTheme: setTheme,
    toggleTheme: toggleTheme,
    onChange: onChange,
    apply: apply
  };

  apply();   // before first paint

  // Another tab (or another page on this origin) changed the preference.
  window.addEventListener("storage", function (ev) {
    if (ev.key === LANG_KEY) {
      lang = normLang(ev.newValue);
      apply();
    } else if (ev.key === THEME_KEY) {
      theme = normTheme(ev.newValue) || systemTheme();
      apply();
    }
  });

  // Follow the OS appearance until the reader makes an explicit choice.
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  if (mq && mq.addEventListener) {
    mq.addEventListener("change", function (ev) {
      if (normTheme(param("theme")) || normTheme(lsGet(THEME_KEY))) return;
      theme = ev.matches ? "dark" : "light";
      apply();
    });
  }

  function initScrollChrome() {
    var bar = document.createElement("div");
    bar.className = "reading-progress";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);

    var top = document.createElement("button");
    top.className = "back-to-top";
    top.type = "button";
    top.textContent = "↑";
    top.title = "Back to top";
    top.setAttribute("aria-label", "Back to top");
    document.body.appendChild(top);

    function update() {
      var span = document.documentElement.scrollHeight - window.innerHeight;
      var pct = span > 0 ? Math.min(100, (window.scrollY / span) * 100) : 0;
      bar.style.width = pct + "%";
      if (window.scrollY > 600) top.classList.add("is-visible");
      else top.classList.remove("is-visible");
    }
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    top.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    update();
  }

  document.addEventListener("DOMContentLoaded", function () {
    uiReady = true;
    syncUI();
    var langBtn = document.getElementById("langToggle");
    if (langBtn) langBtn.addEventListener("click", toggleLang);
    var themeBtn = document.getElementById("themeToggle");
    if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

    // On a narrow screen the chapter list sits above the sheet instead of
    // beside it, so start it collapsed and let the reader open it.
    var details = document.getElementById("sidebarDetails");
    if (details && window.innerWidth < 1080) details.open = false;

    initScrollChrome();
    apply();   // now that buttons exist, push the state into them too
  });
})();
