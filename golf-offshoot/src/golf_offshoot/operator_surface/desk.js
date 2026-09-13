/* 8765 desk: views, in-place watch patch, lightbox, catalog lazy load. */
(function () {
  var body = document.body;
  var lane = body.getAttribute("data-lane") || "golf";
  var views = document.querySelectorAll(".desk-views [data-view-id]");
  var storeKey = "desk-view:" + lane;

  function setView(id) {
    if (!id) id = "home";
    body.setAttribute("data-view", id);
    views.forEach(function (btn) {
      var on = btn.getAttribute("data-view-id") === id;
      btn.classList.toggle("active", on);
      btn.setAttribute("aria-current", on ? "true" : "false");
    });
    try {
      sessionStorage.setItem(storeKey, id);
    } catch (e) {}
  }

  var initial = "home";
  try {
    initial = sessionStorage.getItem(storeKey) || "home";
  } catch (e) {}
  if (!document.querySelector('.desk-view-' + initial)) initial = "home";
  setView(initial);

  views.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setView(btn.getAttribute("data-view-id"));
    });
  });

  var gen = null;
  var hash = null;
  var reloading = false;
  function tick() {
    if (reloading) return;
    var url = "/api/watch?lane=" + encodeURIComponent(lane);
    fetch(url, { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("hub " + r.status);
        return r.json();
      })
      .then(function (s) {
        if (gen === null) {
          gen = s.generation;
          hash = s.hash;
          return;
        }
        if (s.generation !== gen) {
          reloading = true;
          location.reload();
          return;
        }
        if (s.hash && s.hash !== hash) {
          hash = s.hash;
          var sess = document.getElementById("desk-session");
          var blot = document.getElementById("desk-blotter");
          if (sess && s.session_html) sess.outerHTML = s.session_html;
          if (blot && s.blotter_html) blot.outerHTML = s.blotter_html;
        }
      })
      .catch(function () {});
  }
  setInterval(tick, 1500);
  tick();
})();

(function () {
  var box = document.getElementById("viz-lightbox");
  if (!box) return;
  var shown = document.getElementById("viz-lightbox-img");
  var caption = document.getElementById("viz-lightbox-title");
  var hint = document.getElementById("viz-lightbox-hint");
  var ZOOM_HINT_FIT = "Click the chart for full size · Esc or click outside to close";
  var ZOOM_HINT_FULL = "Click the chart to fit it on screen · Esc or click outside to close";
  function setFull(on) {
    box.classList.toggle("full", on);
    if (hint) hint.textContent = on ? ZOOM_HINT_FULL : ZOOM_HINT_FIT;
    box.scrollTop = 0;
  }
  function openBox(href, title) {
    shown.setAttribute("src", href);
    shown.setAttribute("alt", title);
    caption.textContent = title;
    setFull(false);
    box.hidden = false;
    document.body.classList.add("viz-zoomed");
  }
  function closeBox() {
    if (box.hidden) return;
    box.hidden = true;
    shown.setAttribute("src", "");
    document.body.classList.remove("viz-zoomed");
  }
  document.addEventListener("click", function (ev) {
    if (!box.hidden) {
      if (ev.target === shown) setFull(!box.classList.contains("full"));
      else closeBox();
      return;
    }
    if (ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    var link = ev.target && ev.target.closest ? ev.target.closest("a.zoom") : null;
    if (!link) return;
    ev.preventDefault();
    openBox(link.getAttribute("href"), link.getAttribute("data-viz-title") || "");
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" || ev.key === "Esc") closeBox();
  });
})();

(function () {
  document.addEventListener(
    "toggle",
    function (ev) {
      var el = ev.target;
      if (!el || !el.classList || !el.open) return;
      if (el.getAttribute("data-loaded") === "1") return;
      if (el.classList.contains("gk-series")) {
        var st = el.getAttribute("data-series");
        var slot = el.querySelector(".gk-series-body");
        if (!st || !slot) return;
        slot.textContent = "Loading markets…";
        fetch("/golf-catalog/series?ticker=" + encodeURIComponent(st), { cache: "no-store" })
          .then(function (r) {
            if (!r.ok) throw new Error("series");
            return r.text();
          })
          .then(function (html) {
            slot.innerHTML = html;
            el.setAttribute("data-loaded", "1");
          })
          .catch(function () {
            slot.textContent = "Markets not available.";
          });
        return;
      }
      if (el.classList.contains("gk-unmatched")) {
        var body = el.querySelector(".gk-unmatched-body");
        if (!body) return;
        body.textContent = "Loading unmatched…";
        fetch("/golf-catalog/unmatched", { cache: "no-store" })
          .then(function (r) {
            if (!r.ok) throw new Error("unmatched");
            return r.text();
          })
          .then(function (html) {
            body.innerHTML = html;
            el.setAttribute("data-loaded", "1");
          })
          .catch(function () {
            body.textContent = "Unmatched not available.";
          });
      }
    },
    true
  );
})();

(function () {
  function bindPager(pager) {
    var wrap = pager.nextElementSibling;
    if (!wrap) return;
    var status = pager.querySelector(".book-page-status");
    var prev = pager.querySelector(".book-page-prev");
    var next = pager.querySelector(".book-page-next");
    function show(page) {
      var size = parseInt(pager.getAttribute("data-page-size") || "24", 10) || 24;
      var rows = wrap.querySelectorAll("tbody tr.book-row");
      var total = rows.length;
      if (!total) return;
      var pages = Math.max(1, Math.ceil(total / size));
      if (page < 0) page = 0;
      if (page > pages - 1) page = pages - 1;
      pager.setAttribute("data-page", String(page));
      rows.forEach(function (row, i) {
        row.hidden = i < page * size || i >= (page + 1) * size;
      });
      var start = page * size + 1;
      var end = Math.min(total, (page + 1) * size);
      if (status) {
        status.textContent = "Page " + (page + 1) + " of " + pages + " · " + start + "–" + end + " of " + total;
      }
      if (prev) prev.disabled = page === 0;
      if (next) next.disabled = page >= pages - 1;
    }
    pager._showBookPage = show;
    if (prev) {
      prev.addEventListener("click", function () {
        show((parseInt(pager.getAttribute("data-page") || "0", 10) || 0) - 1);
      });
    }
    if (next) {
      next.addEventListener("click", function () {
        show((parseInt(pager.getAttribute("data-page") || "0", 10) || 0) + 1);
      });
    }
    show(parseInt(pager.getAttribute("data-page") || "0", 10) || 0);
  }
  document.querySelectorAll(".book-pager").forEach(bindPager);
})();
