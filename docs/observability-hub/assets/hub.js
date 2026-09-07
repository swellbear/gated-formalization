/* Read-only observability hub renderer.
 *
 * Contract with this file, in order of importance:
 *
 *   1. It renders no control. There is no fetch other than the one GET of
 *      data/manifest.json, no POST, no polling, no timer, no websocket.
 *   2. Manifest values reach the DOM through textContent only. Nothing in the
 *      data feed can inject markup or script.
 *   3. If the manifest carries a control-shaped, cash-shaped, or secret-shaped
 *      key, or a secret-shaped value, the hub refuses to render it and says so.
 *      A bad export blanks the panel rather than quietly growing an affordance.
 *   4. A chart is only ever shown when its PNG actually loads. Every other
 *      case -- absent from the manifest, declared unavailable, declared
 *      available but 404, wrong file type, off-site path -- renders
 *      "not yet available". No chart is invented, ever.
 *   5. Only a chart whose PNG loaded is clickable to enlarge. A
 *      "not yet available" slot has no button, no pointer, and no overlay.
 *
 * Keep it dependency-free. No framework, no bundler, no build step.
 */
(function () {
  "use strict";

  var MANIFEST_URL = "data/manifest.json";
  var NOT_YET = "not yet available";
  var CANONICAL_LANES = ["golf", "learning_lane_15m"];

  /* Keys the manifest may never carry. Matched case-insensitively against every
     object key at every depth. Values are not matched here -- prose is allowed
     to say the word "bankroll", a key named bankroll is what we refuse. The
     allowed key set is documented in data/SCHEMA.md. */
  var FORBIDDEN_KEYS = {
    control: [
      "action", "actions", "control", "controls", "button", "buttons",
      "form", "forms", "submit", "endpoint", "endpoints", "api", "api_base",
      "api_url", "api_endpoint", "post", "post_url", "run_url", "ingest",
      "live_run", "shadow_run", "loop", "refresh", "reload", "poll",
      "poll_url", "ws", "ws_url", "websocket", "stream_url", "arm", "arming",
      "armed", "trade", "trades", "trade_url", "order", "orders", "place",
      "place_bet", "cancel", "bet", "bets", "one_tap", "onetap", "autobet",
      "auto_bet"
    ],
    cash: [
      "deposit", "withdraw", "withdrawal", "transfer", "cash", "cash_in",
      "cash_out", "cashout", "cashin", "bankroll", "balance", "funds",
      "wallet", "stake_now", "money", "payout_url"
    ],
    secret: [
      "secret", "secrets", "api_key", "apikey", "api_secret", "token",
      "access_token", "refresh_token", "bearer", "password", "passwd",
      "credential", "credentials", "private_key", "privatekey", "key", "keys",
      "env", "dotenv", "ssh_key", "session", "cookie", "auth",
      "authorization", "kalshi_key", "kalshi_api_key"
    ]
  };

  /* Secret-shaped values. A match is refused rather than redacted: a redacted
     page would still leave the secret sitting in a committed public file. */
  var SECRET_VALUE_PATTERNS = [
    /-----BEGIN [A-Z ]*PRIVATE KEY-----/,
    /\bsk-[A-Za-z0-9_-]{16,}/,
    /\bAKIA[0-9A-Z]{12,}/,
    /\bgh[pousr]_[A-Za-z0-9]{20,}/,
    /\bxox[baprs]-[A-Za-z0-9-]{10,}/,
    /\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\./,
    /(api[_-]?key|api[_-]?secret|access[_-]?token|client[_-]?secret|password|passwd|bearer)\s*[:=]\s*\S{8,}/i
  ];

  var DOC_LINK_PREFIX = "https://github.com/swellbear/gated-formalization/";

  /* ------------------------------------------------------------------ *
   * tiny DOM helpers -- text nodes only; markup is never built from data
   * ------------------------------------------------------------------ */

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) { node.className = className; }
    if (text !== undefined && text !== null && text !== "") {
      node.textContent = String(text);
    }
    return node;
  }

  function isPlainObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function str(value) {
    return typeof value === "string" ? value : "";
  }

  function list(value) {
    return Array.isArray(value) ? value : [];
  }

  /* ------------------------------------------------------------------ *
   * hard-NO audit
   * ------------------------------------------------------------------ */

  function auditManifest(manifest) {
    var violations = [];

    function record(kind, path, detail) {
      if (violations.length < 25) {
        violations.push({ kind: kind, path: path, detail: detail });
      }
    }

    function keyKind(key) {
      var lowered = key.toLowerCase();
      var kinds = Object.keys(FORBIDDEN_KEYS);
      for (var i = 0; i < kinds.length; i += 1) {
        if (FORBIDDEN_KEYS[kinds[i]].indexOf(lowered) !== -1) { return kinds[i]; }
      }
      return null;
    }

    function walk(value, path) {
      if (Array.isArray(value)) {
        value.forEach(function (item, index) {
          walk(item, path + "[" + index + "]");
        });
        return;
      }
      if (isPlainObject(value)) {
        Object.keys(value).forEach(function (key) {
          var childPath = path ? path + "." + key : key;
          var kind = keyKind(key);
          if (kind) {
            record(kind, childPath, "forbidden key \u201c" + key + "\u201d");
          }
          walk(value[key], childPath);
        });
        return;
      }
      if (typeof value === "string") {
        for (var i = 0; i < SECRET_VALUE_PATTERNS.length; i += 1) {
          if (SECRET_VALUE_PATTERNS[i].test(value)) {
            record("secret", path, "value looks like a credential");
            return;
          }
        }
      }
    }

    walk(manifest, "");
    return violations;
  }

  /* ------------------------------------------------------------------ *
   * link + chart path safety
   * ------------------------------------------------------------------ */

  /* Doc links may only point into this repository over https. Anything else --
     javascript:, data:, an unrelated host -- is dropped rather than rendered. */
  function safeDocHref(href) {
    var raw = str(href);
    if (!raw) { return null; }
    var resolved;
    try {
      resolved = new URL(raw, document.baseURI);
    } catch (err) {
      return null;
    }
    if (resolved.protocol !== "https:" && resolved.protocol !== "http:") { return null; }
    if (resolved.href.indexOf(DOC_LINK_PREFIX) === 0) { return resolved.href; }
    if (resolved.origin === window.location.origin && raw.indexOf(":") === -1) {
      return resolved.href;
    }
    return null;
  }

  /* Chart paths must be relative PNGs inside the published tree. A chart that
     fails this check is not shown as a chart -- it is shown as not yet
     available, with the reason stated. */
  function safeChartSrc(path) {
    var raw = str(path);
    if (!raw) { return { src: null, reason: "no path in the manifest" }; }
    if (/^[a-z][a-z0-9+.-]*:/i.test(raw) || raw.indexOf("//") === 0) {
      return { src: null, reason: "off-site chart path rejected. Chart not invented." };
    }
    if (raw.charAt(0) === "/") {
      return { src: null, reason: "absolute chart path rejected. Chart not invented." };
    }
    if (!/\.png$/i.test(raw)) {
      return { src: null, reason: "non-PNG viz file ignored. Chart not invented." };
    }
    var resolved;
    try {
      resolved = new URL(raw, document.baseURI);
    } catch (err) {
      return { src: null, reason: "unreadable chart path. Chart not invented." };
    }
    if (resolved.origin !== window.location.origin) {
      return { src: null, reason: "off-site chart path rejected. Chart not invented." };
    }
    return { src: resolved.href, reason: null };
  }

  /* ------------------------------------------------------------------ *
   * lightbox -- a bigger look at a PNG already on the page
   * ------------------------------------------------------------------ */

  var lightbox = (function () {
    var root = document.getElementById("lightbox");
    var titleNode = document.getElementById("lightbox-title");
    var captionNode = document.getElementById("lightbox-caption");
    var imageNode = document.getElementById("lightbox-image");
    var stageNode = document.getElementById("lightbox-stage");
    var zoomBtn = document.getElementById("lightbox-zoom");
    var closeBtn = document.getElementById("lightbox-close");
    var opener = null;

    if (!root || !imageNode || !stageNode || !zoomBtn || !closeBtn) {
      return { open: function () {}, available: false };
    }

    function setZoom(mode) {
      root.setAttribute("data-zoom", mode);
      var actual = mode === "actual";
      zoomBtn.setAttribute("aria-pressed", actual ? "true" : "false");
      zoomBtn.textContent = actual ? "Fit to screen" : "Actual size";
      if (!actual) {
        stageNode.scrollTop = 0;
        stageNode.scrollLeft = 0;
      }
    }

    function close() {
      if (root.hidden) { return; }
      root.hidden = true;
      document.body.classList.remove("lightbox-open");
      imageNode.removeAttribute("src");
      imageNode.alt = "";
      setZoom("fit");
      if (opener && typeof opener.focus === "function") { opener.focus(); }
      opener = null;
    }

    function open(chart, imgNode, triggerNode) {
      opener = triggerNode || null;
      titleNode.textContent = str(chart.title) || "Chart";
      imageNode.src = imgNode.currentSrc || imgNode.src;
      imageNode.alt = imgNode.alt;

      var captionParts = [];
      if (str(chart.subline)) { captionParts.push(str(chart.subline)); }
      if (str(chart.pixel_size)) { captionParts.push(str(chart.pixel_size) + " px"); }
      if (str(chart.note)) { captionParts.push(str(chart.note)); }
      captionParts.push(
        "Enlarged view only. Press Esc, or click outside the image, to close."
      );
      captionNode.textContent = captionParts.join(" \u00b7 ");

      setZoom("fit");
      root.hidden = false;
      document.body.classList.add("lightbox-open");
      closeBtn.focus();
    }

    closeBtn.addEventListener("click", close);

    zoomBtn.addEventListener("click", function () {
      setZoom(root.getAttribute("data-zoom") === "actual" ? "fit" : "actual");
    });

    /* Fit view: clicking anywhere on the stage closes, the image included.
       Actual size: clicking the image is panning, so only the surround closes. */
    stageNode.addEventListener("click", function (event) {
      if (root.getAttribute("data-zoom") !== "actual" || event.target === stageNode) {
        close();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (root.hidden) { return; }
      if (event.key === "Escape") {
        event.preventDefault();
        close();
        return;
      }
      if (event.key !== "Tab") { return; }
      var stops = [zoomBtn, closeBtn, stageNode];
      var index = stops.indexOf(document.activeElement);
      var next = event.shiftKey ? index - 1 : index + 1;
      if (index === -1) { next = 0; }
      if (next < 0) { next = stops.length - 1; }
      if (next >= stops.length) { next = 0; }
      event.preventDefault();
      stops[next].focus();
    });

    return { open: open, available: true };
  }());

  /* ------------------------------------------------------------------ *
   * section builders
   * ------------------------------------------------------------------ */

  function badgeList(badges, className) {
    var ul = el("ul", "badges " + (className || ""));
    ul.setAttribute("aria-label", "Lane posture");
    list(badges).forEach(function (badge) {
      if (str(badge)) { ul.appendChild(el("li", "badge", badge)); }
    });
    return ul;
  }

  function rowList(rows) {
    var wrap = el("div", "rows");
    list(rows).forEach(function (row) {
      if (!isPlainObject(row)) { return; }
      var line = el("div", "row");
      line.appendChild(el("span", "row-label", str(row.label)));
      line.appendChild(el("span", "row-value", str(row.value)));
      if (str(row.note)) {
        line.appendChild(el("span", "row-note", str(row.note)));
      }
      wrap.appendChild(line);
    });
    return wrap;
  }

  function noteList(notes, title) {
    if (!list(notes).length) { return null; }
    var frag = document.createDocumentFragment();
    if (title) { frag.appendChild(el("p", "notes-title", title)); }
    var ul = el("ul", "notes");
    list(notes).forEach(function (note) {
      if (str(note)) { ul.appendChild(el("li", null, note)); }
    });
    frag.appendChild(ul);
    return frag;
  }

  function linkList(links) {
    if (!list(links).length) { return null; }
    var ul = el("ul", "links");
    var shown = 0;
    list(links).forEach(function (link) {
      if (!isPlainObject(link)) { return; }
      var href = safeDocHref(link.href);
      if (!href) { return; }
      var li = el("li");
      var anchor = el("a", null, str(link.label) || href);
      anchor.href = href;
      anchor.rel = "noopener noreferrer";
      li.appendChild(anchor);
      ul.appendChild(li);
      shown += 1;
    });
    return shown ? ul : null;
  }

  function card(title, statusText, statusKind, headline) {
    var section = el("section", "card");
    var heading = el("h3", null, title);
    section.appendChild(heading);
    if (str(statusText)) {
      var chip = el("span", "status-chip is-" + (statusKind || "absent"), statusText);
      heading.appendChild(document.createTextNode(" "));
      heading.appendChild(chip);
    }
    if (str(headline)) {
      section.appendChild(el("p", "card-headline", headline));
    }
    return section;
  }

  function unavailable(message) {
    var box = el("div", "chart-missing");
    box.appendChild(el("strong", null, NOT_YET));
    box.appendChild(el("span", null, message || "Nothing has been published for this slot yet."));
    return box;
  }

  /* ------------------------------------------------------------------ *
   * lane sections
   * ------------------------------------------------------------------ */

  function laneHeader(lane) {
    var head = el("div", "lane-head");
    head.appendChild(el("p", "lane-id", "Lane " + str(lane.lane_id)));
    head.appendChild(el("h2", null, str(lane.label) || str(lane.lane_id)));
    head.appendChild(badgeList(lane.badges, "lane-badges"));
    if (str(lane.summary_line)) {
      head.appendChild(el("p", "lane-summary", str(lane.summary_line)));
    }
    if (str(lane.source_kind)) {
      head.appendChild(el("p", "lane-source", "Source: " + str(lane.source_kind)));
    }
    if (str(lane.lane_scope_note)) {
      head.appendChild(el("p", "scope-note", str(lane.lane_scope_note)));
    }
    return head;
  }

  function lastRunSection(lastRun) {
    var data = isPlainObject(lastRun) ? lastRun : {};
    var status = str(data.status) || NOT_YET;
    var kind = status === NOT_YET ? "absent" : "off";
    var section = card("Last run — honesty", status, kind, str(data.headline));
    if (list(data.fields).length) {
      section.appendChild(rowList(data.fields));
    } else {
      section.appendChild(unavailable("No run has been published for this lane, so no run detail is shown."));
    }
    var notes = noteList(data.notes, "Read this as");
    if (notes) { section.appendChild(notes); }
    return section;
  }

  function settleSection(settle) {
    var data = isPlainObject(settle) ? settle : {};
    var state = str(data.banner_state);
    var label;
    var kind;
    if (state === "pending") {
      label = str(data.banner) || "SETTLE_PENDING";
      kind = "pending";
    } else if (state === "off") {
      label = "settle banner off";
      kind = "off";
    } else {
      label = NOT_YET;
      kind = "absent";
    }

    var section = card("Settle banner", label, kind, str(data.headline));

    if (list(data.counts).length) {
      section.appendChild(rowList(data.counts));
    } else {
      section.appendChild(unavailable("No settle summary has been published for this lane."));
    }

    if (isPlainObject(data.observation)) {
      var obs = el("div", "observation");
      obs.appendChild(el("span", "observation-label", str(data.observation.label)));
      obs.appendChild(el("span", "observation-value", str(data.observation.value)));
      var chips = el("ul", "chips");
      list(data.observation.chips).forEach(function (chip) {
        if (str(chip)) { chips.appendChild(el("li", "chip", chip)); }
      });
      if (chips.childNodes.length) { obs.appendChild(chips); }
      if (str(data.observation.note)) {
        obs.appendChild(el("p", "row-note", str(data.observation.note)));
      }
      section.appendChild(obs);
    }

    if (list(data.sources).length) {
      section.appendChild(el("p", "notes-title", "Settle sources"));
      section.appendChild(rowList(data.sources));
    }

    if (list(data.residual).length) {
      section.appendChild(el("p", "notes-title", "Residual — still pending, named, not invented"));
      section.appendChild(rowList(data.residual));
    }

    var notes = noteList(data.notes, "Read this as");
    if (notes) { section.appendChild(notes); }
    return section;
  }

  function paperSection(ledger) {
    var data = isPlainObject(ledger) ? ledger : {};
    var status = str(data.status) || NOT_YET;
    var section = card(
      "Paper ledger summary",
      status,
      status === NOT_YET ? "absent" : "off",
      str(data.headline)
    );

    if (list(data.rows).length) {
      section.appendChild(rowList(data.rows));
    } else {
      section.appendChild(unavailable("No paper ledger summary has been published for this lane."));
    }

    if (list(data.absent_fields).length) {
      section.appendChild(el("p", "notes-title", "Absent from the export"));
      var ul = el("ul", "absent-list");
      list(data.absent_fields).forEach(function (field) {
        if (str(field)) { ul.appendChild(el("li", null, field)); }
      });
      section.appendChild(ul);
    }

    var notes = noteList(data.notes, "Read this as");
    if (notes) { section.appendChild(notes); }
    return section;
  }

  function recordsSection(lane) {
    var records = list(lane.records);
    var section = card(
      "Weekly operating record",
      records.length ? String(records.length) + " on file" : NOT_YET,
      records.length ? "pending" : "absent",
      records.length
        ? "Dated records for this lane. A dated FAIL stays a FAIL; it is not rewritten."
        : str(lane.records_note)
    );

    if (!records.length) {
      section.appendChild(unavailable(
        str(lane.records_note) || "No weekly operating record has been published for this lane."
      ));
      return section;
    }

    records.forEach(function (record) {
      if (!isPlainObject(record)) { return; }
      var box = el("div", "record");
      if (str(record.verdict)) {
        box.appendChild(el("span", "verdict", str(record.record_id) + " " + str(record.verdict)));
      }
      if (str(record.lean)) {
        box.appendChild(el("span", "verdict-lean", str(record.lean)));
      }
      box.appendChild(el("h4", null, str(record.title)));
      if (str(record.lane_scope_note)) {
        box.appendChild(el("p", "scope-note", str(record.lane_scope_note)));
      }
      if (list(record.rows).length) { box.appendChild(rowList(record.rows)); }
      if (list(record.hard_nos).length) {
        box.appendChild(el("p", "hard-nos-title", "Hard NOs on this record"));
        var ul = el("ul", "hard-nos");
        list(record.hard_nos).forEach(function (item) {
          if (str(item)) { ul.appendChild(el("li", null, item)); }
        });
        box.appendChild(ul);
      }
      var links = linkList(record.links);
      if (links) { box.appendChild(links); }
      section.appendChild(box);
    });

    return section;
  }

  /* A chart is drawn only once its PNG has actually loaded. Until then, and on
     any failure, the slot reads "not yet available". Only a loaded chart gets
     the enlarge button. */
  function chartBlock(chart) {
    var box = el("div", "chart");
    box.appendChild(el("h4", null, str(chart.title) || str(chart.slot_id)));
    if (str(chart.subline)) {
      box.appendChild(el("p", "chart-subline", str(chart.subline)));
    }
    if (list(chart.badges).length) {
      box.appendChild(badgeList(chart.badges, "lane-badges"));
    }

    var declared = str(chart.status);
    if (declared !== "available") {
      box.appendChild(unavailable(
        str(chart.note) || "Illustrator owns regeneration. No chart generated."
      ));
      return box;
    }

    var checked = safeChartSrc(chart.path);
    if (!checked.src) {
      box.appendChild(unavailable(checked.reason));
      return box;
    }

    /* Placeholder first, swapped for the figure on a successful load. A 404 or a
       broken file therefore degrades to "not yet available" instead of showing a
       broken image next to a claim that the chart exists. */
    var pending = unavailable("Checking the published file\u2026");
    box.appendChild(pending);

    var img = new Image();
    img.alt = (str(chart.title) || str(chart.slot_id)) +
      " \u2014 read-only chart. Enlarge for detail.";

    img.addEventListener("load", function () {
      var figure = el("figure", "chart-figure");
      figure.appendChild(img);

      var caption = el("figcaption");
      var captionBits = [];
      if (str(chart.pixel_size)) { captionBits.push(str(chart.pixel_size) + " px"); }
      if (str(chart.note)) { captionBits.push(str(chart.note)); }
      caption.textContent = captionBits.join(" \u00b7 ");
      figure.appendChild(caption);

      var mounted = figure;
      if (lightbox.available) {
        var trigger = el("button", "chart-zoom");
        trigger.type = "button";
        trigger.setAttribute(
          "aria-label",
          "Enlarge chart: " + (str(chart.title) || str(chart.slot_id))
        );
        trigger.appendChild(figure);
        trigger.appendChild(el("span", "zoom-hint", "Click to enlarge"));
        trigger.addEventListener("click", function () {
          lightbox.open(chart, img, trigger);
        });
        mounted = trigger;
      }

      var docLink = safeDocHref(chart.doc_href);
      box.replaceChild(mounted, pending);
      if (docLink) {
        var linkWrap = el("ul", "links");
        var li = el("li");
        var anchor = el("a", null, "What this board does and does not claim");
        anchor.href = docLink;
        anchor.rel = "noopener noreferrer";
        li.appendChild(anchor);
        linkWrap.appendChild(li);
        box.appendChild(linkWrap);
      }
    });

    img.addEventListener("error", function () {
      box.replaceChild(
        unavailable(
          "the manifest lists this chart, but the file is not in the published tree. " +
          "Nothing is drawn in its place."
        ),
        pending
      );
    });

    img.src = checked.src;
    return box;
  }

  function chartsSection(lane) {
    var charts = list(lane.charts);
    var section = card(
      "Charts",
      charts.length ? String(charts.length) + " slots" : NOT_YET,
      charts.length ? "off" : "absent",
      charts.length
        ? "Read-only PNGs when present. Missing charts stay not yet available \u2014 never invented."
        : str(lane.charts_note)
    );
    if (!charts.length) {
      section.appendChild(unavailable(
        str(lane.charts_note) || "No charts have been published for this lane."
      ));
      return section;
    }
    charts.forEach(function (chart) {
      if (isPlainObject(chart)) { section.appendChild(chartBlock(chart)); }
    });
    return section;
  }

  function docsSection(lane) {
    var links = linkList(lane.docs);
    if (!links) { return null; }
    var section = card("Read further", null, null,
      "Source documents in the repository. Reading, not operating.");
    section.appendChild(links);
    return section;
  }

  function renderLane(lane, mount) {
    mount.textContent = "";
    mount.appendChild(laneHeader(lane));
    mount.appendChild(lastRunSection(lane.last_run));
    mount.appendChild(settleSection(lane.settle));
    mount.appendChild(paperSection(lane.paper_ledger));
    mount.appendChild(recordsSection(lane));
    mount.appendChild(chartsSection(lane));
    var docs = docsSection(lane);
    if (docs) { mount.appendChild(docs); }
  }

  /* ------------------------------------------------------------------ *
   * notices
   * ------------------------------------------------------------------ */

  function showNotice(node, kind, heading, paragraphs, items) {
    node.className = "notice notice-" + kind;
    node.textContent = "";
    if (heading) { node.appendChild(el("h2", null, heading)); }
    list(paragraphs).forEach(function (text) {
      node.appendChild(el("p", null, text));
    });
    if (list(items).length) {
      var ul = el("ul");
      list(items).forEach(function (item) { ul.appendChild(el("li", null, item)); });
      node.appendChild(ul);
    }
    node.classList.remove("is-hidden");
  }

  /* ------------------------------------------------------------------ *
   * boot
   * ------------------------------------------------------------------ */

  var statusNode = document.getElementById("hub-status");
  var contentNode = document.getElementById("lane-content");
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".lane-tab"));
  var panel = document.getElementById("lane-panel");

  function laneFromHash() {
    var hash = window.location.hash.replace(/^#/, "");
    return CANONICAL_LANES.indexOf(hash) !== -1 ? hash : null;
  }

  function wire(manifest) {
    var lanes = list(manifest.lanes).filter(function (lane) {
      return isPlainObject(lane) && CANONICAL_LANES.indexOf(str(lane.lane_id)) !== -1;
    });

    if (!lanes.length) {
      showNotice(statusNode, "warn", null, [
        "The manifest declares no lane with a canonical id (" +
          CANONICAL_LANES.join(" or ") + "), so there is nothing to show.",
        "That is reported rather than patched over. No lane view is guessed."
      ]);
      return;
    }

    var byId = {};
    lanes.forEach(function (lane) { byId[str(lane.lane_id)] = lane; });

    function select(laneId, updateHash) {
      var lane = byId[laneId] || lanes[0];
      var activeId = str(lane.lane_id);
      document.body.setAttribute("data-lane", activeId);
      tabs.forEach(function (tab) {
        var isActive = tab.getAttribute("data-lane-id") === activeId;
        tab.setAttribute("aria-selected", isActive ? "true" : "false");
        if (isActive) { panel.setAttribute("aria-labelledby", tab.id); }
      });
      renderLane(lane, contentNode);
      if (updateHash && window.location.hash !== "#" + activeId) {
        window.history.replaceState(null, "", "#" + activeId);
      }
    }

    tabs.forEach(function (tab) {
      var laneId = tab.getAttribute("data-lane-id");
      if (!byId[laneId]) {
        tab.disabled = true;
        tab.title = "This lane is not in the published manifest.";
        return;
      }
      tab.addEventListener("click", function () {
        select(laneId, true);
        panel.focus();
      });
    });

    window.addEventListener("hashchange", function () {
      var laneId = laneFromHash();
      if (laneId && byId[laneId]) { select(laneId, false); }
    });

    if (str(manifest.hub && manifest.hub.source_kind) === "fixture") {
      showNotice(statusNode, "warn", null, [
        "This page is rendering the checked-in fixture, not a fresh export. " +
          str((manifest.hub && manifest.hub.source_note) || ""),
        "Systems replaces data/manifest.json to publish real exports. Until it does, " +
          "every figure here is traceable to a file already committed in this repository."
      ]);
    } else {
      statusNode.classList.add("is-hidden");
    }

    select(laneFromHash() || str(lanes[0].lane_id), false);
  }

  fetch(MANIFEST_URL, { cache: "no-store" })
    .then(function (response) {
      if (!response.ok) { throw new Error("HTTP " + response.status); }
      return response.json();
    })
    .then(function (manifest) {
      var violations = auditManifest(manifest);
      if (violations.length) {
        showNotice(
          statusNode,
          "refusal",
          "Refused to render this manifest",
          [
            "data/manifest.json carries content this hub is not allowed to display, so " +
              "none of it was rendered. This page stays read-only even when its feed " +
              "stops being read-only.",
            "Fix the export and re-publish. Nothing is shown from a manifest that fails " +
              "this check, and nothing is filled in from memory."
          ],
          violations.map(function (violation) {
            return violation.kind + ": " + violation.path + " \u2014 " + violation.detail;
          })
        );
        return;
      }
      wire(manifest);
    })
    .catch(function (error) {
      showNotice(statusNode, "warn", null, [
        "Could not read data/manifest.json (" + error.message + ").",
        "Nothing is drawn in its place. Everything this page would have shown is " +
          "not yet available until the manifest loads. If you opened this file " +
          "directly from disk, serve the directory over http instead."
      ]);
    });
}());
