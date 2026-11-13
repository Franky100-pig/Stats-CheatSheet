/* Language switch for the bilingual lecture site.
   Loaded synchronously in <head> so the choice is applied before the first
   paint -- otherwise a remembered English-only mode flashes Chinese text.

   "both" shows the English sheet plus the injected Chinese annotations;
   "en" hides every .zh element, leaving exactly the exam-facing English sheet.
   The preference is remembered locally, like the theme in LA-Helper. */
(function () {
  "use strict";

  var KEY = "stats-cheatsheet-lang";
  var LABELS = { both: "双语 · 切到 EN", en: "EN · 显示中文" };
  var mode = "both";
  try {
    if (window.localStorage.getItem(KEY) === "en") mode = "en";
  } catch (e) { /* private mode: just stay bilingual */ }
  // ?lang=en is a shareable English-only (exam view) link; it wins over the
  // remembered preference for this page load without overwriting it.
  try {
    if (new URLSearchParams(window.location.search).get("lang") === "en") mode = "en";
  } catch (e) {}

  function apply() {
    document.documentElement.setAttribute("data-lang", mode);
    var btn = document.getElementById("langToggle");
    if (!btn) return;
    btn.textContent = LABELS[mode];
    btn.setAttribute("aria-pressed", mode === "en" ? "true" : "false");
    btn.title = mode === "en"
      ? "Show the Chinese annotations again"
      : "Hide the Chinese annotations (English-only exam view)";
  }

  apply();                                        // no flash
  document.addEventListener("DOMContentLoaded", apply);   // button now exists
  document.addEventListener("click", function (ev) {
    if (!ev.target || ev.target.id !== "langToggle") return;
    mode = mode === "en" ? "both" : "en";
    try { window.localStorage.setItem(KEY, mode); } catch (e) {}
    apply();
  });
})();
