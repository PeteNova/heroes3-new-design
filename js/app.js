(function () {
  "use strict";

  var app = document.getElementById("app");
  var navLinks = document.querySelectorAll("[data-nav]");

  function data() {
    return window.H3ND_MODS;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function availableCount() {
    return data().mods.filter(function (m) { return m.status === "available"; }).length;
  }

  function setNav(name) {
    navLinks.forEach(function (link) {
      link.classList.toggle("is-active", link.getAttribute("data-nav") === name);
    });
  }

  function statusLabel(mod) {
    return mod.status === "available" ? "Do pobrania" : "Wkrótce";
  }

  function versionedUrl(path, version) {
    if (!path) return path;
    if (!version) return path;
    return path + (path.indexOf("?") >= 0 ? "&" : "?") + "v=" + encodeURIComponent(version);
  }

  function rosterSpriteUrl(mod) {
    return "assets/portraits/" + mod.slug + "-roster.png";
  }

  function flattenRoster(mod) {
    if (!mod.roster) return [];
    return Object.keys(mod.roster).reduce(function (acc, klass) {
      return acc.concat(mod.roster[klass]);
    }, []);
  }

  function portraitVersion(mod) {
    var suffix = mod.slug === "fortress" ? "-hd4-voy-v8" : "-hd4";
    return (mod.version || "") + suffix;
  }

  function thumbHtml(mod) {
    var src = rosterSpriteUrl(mod);
    var names = flattenRoster(mod);
    var portraits = names.map(function (name, index) {
      var col = index % 4;
      var row = Math.floor(index / 4);
      var x = col * (100 / 3);
      var y = row * (100 / 3);
      return (
        '<span class="gallery-portrait">' +
          '<span class="gallery-face" style="' +
            "background-image:url('" +
            escapeHtml(versionedUrl(src, portraitVersion(mod))) +
            "');background-position:" + x + "% " + y + '%"></span>' +
          "<i>" + escapeHtml(name) + "</i>" +
        "</span>"
      );
    }).join("");
    return (
      '<div class="portrait-gallery" role="img" aria-label="Portrety — ' +
      escapeHtml(mod.faction) + '">' + portraits + "</div>"
    );
  }

  function packsReadyLabel(count) {
    var n = Number(count);
    var noun = n === 1 ? "paczka gotowa" : n >= 2 && n <= 4 ? "paczki gotowe" : "paczek gotowych";
    return "<div><b>" + n + "</b>" + noun + "</div>";
  }

  function cardDownloadHtml(mod) {
    if (mod.status === "available" && mod.download) {
      var size = mod.downloadSize ? " · " + escapeHtml(mod.downloadSize) : "";
      return (
        '<a class="cta cta-card" href="' +
        escapeHtml(versionedUrl(mod.download, mod.version)) +
        '" download>Pobierz' + size + "</a>"
      );
    }
    return '<span class="cta cta-card disabled" aria-disabled="true">Wkrótce</span>';
  }

  function renderHome() {
    setNav("home");
    var project = data().project;
    var cards = data().mods.map(function (mod) {
      var soon = mod.status !== "available";
      return (
        '<article class="mod-card frame' + (soon ? " is-soon" : "") +
        '">' +
          '<div class="mod-card-content">' +
            '<div class="thumb">' +
              thumbHtml(mod) +
              '<span class="badge' + (soon ? " soon" : "") + '">' + statusLabel(mod) + "</span>" +
            "</div>" +
            '<div class="card-body">' +
              "<h3>" + escapeHtml(mod.faction) +
              '<span class="card-summary">' +
              (mod.version ? " · v" + escapeHtml(mod.version) : "") + "</span></h3>" +
            "</div>" +
          "</div>" +
          '<div class="card-actions">' + cardDownloadHtml(mod) + "</div>" +
        "</article>"
      );
    }).join("");

    app.innerHTML =
      '<section class="hero frame">' +
        '<div class="ornament" aria-hidden="true"></div>' +
        "<h1>" + escapeHtml(project.name) + "</h1>" +
        '<p class="en">' + escapeHtml(project.taglineEn) + "</p>" +
        "<p>" + escapeHtml(project.pitch) + "</p>" +
        '<div class="stats">' +
          packsReadyLabel(availableCount()) +
          "<div><b>VCMI " + escapeHtml(project.vcmiMin) + "+</b>wymagane środowisko</div>" +
          "<div><b>tylko grafika</b>bez zmian mechaniki</div>" +
        "</div>" +
      "</section>" +
      '<div class="section-head">' +
        "<h2>Mody portretów</h2>" +
        "<p>Każda frakcja to osobny, opcjonalny mod VCMI do pobrania.</p>" +
      "</div>" +
      '<div class="mod-grid">' + cards + "</div>" +
      '<section class="landing-info">' +
        '<div><h2>Instalacja</h2>' +
          '<p>Pobierz ZIP, rozpakuj go i skopiuj zawarty folder do <code>Mods</code> VCMI. Następnie włącz mod w launcherze.</p></div>' +
        '<div><h2>Dane techniczne</h2>' +
          '<p>Wymagane: legalna kopia Heroes III oraz VCMI ' + escapeHtml(project.vcmiMin) +
          '+.</p><p>Paczki zmieniają wyłącznie portrety: HPL 1× (58×64) i HPS 1× (48×32), plus warianty HD VCMI 2× / 3× / 4×.</p></div>' +
      "</section>";
  }

  function renderInstall() {
    setNav("instalacja");
    app.innerHTML =
      '<section class="article frame">' +
        '<div class="ornament" aria-hidden="true"></div>' +
        "<h1>Instalacja</h1>" +
        "<p>Mody działają w <strong>VCMI</strong> jako nakładka graficzna. Nie podmieniają plików oryginalnej instalacji GOG/CD.</p>" +
        "<h2>Wymagania</h2>" +
        "<ul>" +
          "<li>Własna kopia <strong>Heroes of Might and Magic III</strong> (Complete / Shadow of Death).</li>" +
          "<li><strong>VCMI</strong> " + escapeHtml(data().project.vcmiMin) + " lub nowszy — <a href=\"https://vcmi.eu/\" target=\"_blank\" rel=\"noopener\">vcmi.eu</a>.</li>" +
        "</ul>" +
        "<h2>Kroki</h2>" +
        "<ol class=\"steps\">" +
          "<li>Pobierz ZIP wybranej frakcji ze strony głównej.</li>" +
          "<li>Rozpakuj archiwum. W środku jest jeden folder, np. <code>heroes3-new-design-portraits-castle-v1</code>, z plikiem <code>mod.json</code>.</li>" +
          "<li>Skopiuj ten folder do katalogu modów VCMI. Na Windowsie bywa to m.in. <code>Dokumenty\\My Games\\vcmi\\Mods</code> albo folder <code>Mods</code> obok instalacji VCMI.</li>" +
          "<li>Uruchom launcher VCMI, włącz mod i zacznij grę. Portrety powinny zastąpić oryginały w oknie bohatera i na liście.</li>" +
        "</ol>" +
        "<h2>Kilka frakcji naraz</h2>" +
        "<p>Każda frakcja to osobny mod. Możesz włączyć Zamek, Inferno i Lochy niezależnie — nie nadpisują się nawzajem.</p>" +
        "<h2>Odinstalowanie</h2>" +
        "<p>Wyłącz mod w launcherze albo usuń jego folder z <code>Mods</code>. Oryginalna gra pozostaje nietknięta.</p>" +
      "</section>";
  }

  function renderAbout() {
    setNav("o-projekcie");
    app.innerHTML =
      '<section class="article frame">' +
        '<div class="ornament" aria-hidden="true"></div>' +
        "<h1>O projekcie</h1>" +
        "<p><strong>Heroes of Might and Magic III — Graphic Mods</strong> odświeża wyłącznie warstwę wizualną klasyka. Gameplay, balans, muzyka i rozpoznawalny klimat świata zostają. Ta strona służy do <em>prezentacji i dystrybucji</em> gotowych modów VCMI dla fanów — nie zastępuje pipeline’u artystycznego.</p>" +
        "<h2>Co dostajesz</h2>" +
        "<ul>" +
          "<li>Portrety bohaterów w skali gry (HPL/HPS) oraz, tam gdzie paczka v1.1 to obejmuje, warianty HD 2×/3×/4×.</li>" +
          "<li>Te same kadry, sylwetki i palety frakcji co w oryginale — czytelniejsze światło i detal.</li>" +
          "<li>Opcjonalne mody: włączasz tylko te frakcje, które chcesz.</li>" +
        "</ul>" +
        "<h2>Czego tu nie ma</h2>" +
        "<p>Nie zmieniamy jednostek, czarów, ekonomii ani map. Nie jest to remake ani oficjalna edycja HD.</p>" +
        "<h2>Uwaga prawna</h2>" +
        '<div class="legal">' +
          "<p>Heroes of Might and Magic III oraz powiązane znaki towarowe należą do ich właścicieli (historycznie 3DO / New World Computing, obecnie m.in. Ubisoft). Ten projekt jest <strong>nieoficjalną, fanowską pracą wizualną</strong> i nie jest powiązany z wymienionymi podmiotami.</p>" +
          "<p>Paczki nie zawierają gry. Żeby z nich skorzystać, musisz posiadać legalną kopię Heroes III oraz środowisko VCMI. Rozpowszechniamy wyłącznie własne, odświeżone portrety jako mod graficzny.</p>" +
        "</div>" +
      "</section>";
  }

  function route() {
    var hash = (location.hash || "#/").replace(/^#/, "");
    var parts = hash.split("/").filter(Boolean);
    if (parts[0] === "instalacja") {
      renderInstall();
    } else if (parts[0] === "o-projekcie") {
      renderAbout();
    } else {
      renderHome();
    }
    if (app && typeof app.focus === "function") app.focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }

  window.addEventListener("hashchange", route);
  route();
})();
