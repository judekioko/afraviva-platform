/*
 * Auto-logs out an idle admin session, the way a banking dashboard would:
 * a warning with a countdown appears before the deadline, then an automatic
 * redirect to the logout page. Timeout comes from the script tag's own
 * data attributes so it stays in sync with settings.ADMIN_IDLE_TIMEOUT_SECONDS
 * (see config/settings.py) without duplicating the number here.
 */
(function () {
  var scriptTag = document.currentScript || document.getElementById("idle-timeout-script");
  if (!scriptTag) return;

  var timeoutSeconds = parseInt(scriptTag.dataset.idleTimeoutSeconds, 10) || 900;
  var logoutUrl = scriptTag.dataset.logoutUrl || "/admin/logout/";
  var warnBeforeSeconds = Math.min(60, Math.floor(timeoutSeconds / 4)) || 30;

  var lastActivity = Date.now();
  var warned = false;
  var modal = null;
  var countdownEl = null;

  function markActive() {
    lastActivity = Date.now();
    if (warned) hideWarning();
  }

  ["mousemove", "mousedown", "keydown", "touchstart", "scroll", "wheel"].forEach(function (evt) {
    window.addEventListener(evt, markActive, { passive: true });
  });

  function buildModal() {
    var overlay = document.createElement("div");
    overlay.setAttribute("role", "alertdialog");
    overlay.setAttribute("aria-live", "assertive");
    overlay.style.cssText =
      "position:fixed;inset:0;background:rgba(27,47,38,0.55);" +
      "display:flex;align-items:center;justify-content:center;z-index:9999;";

    var box = document.createElement("div");
    box.style.cssText =
      "background:#FBF9F2;color:#23291F;padding:24px 28px;border-radius:6px;" +
      "max-width:360px;font-family:-apple-system,'Segoe UI',sans-serif;" +
      "box-shadow:0 12px 40px rgba(0,0,0,0.3);";

    var heading = document.createElement("h2");
    heading.textContent = "Still there?";
    heading.style.cssText = "margin:0 0 8px;font-size:18px;color:#2C4A3B;";

    var body = document.createElement("p");
    body.style.cssText = "margin:0 0 16px;font-size:14px;line-height:1.5;";
    body.appendChild(document.createTextNode("You've been inactive. For security, you'll be signed out in "));
    countdownEl = document.createElement("span");
    countdownEl.style.fontWeight = "600";
    body.appendChild(countdownEl);
    body.appendChild(document.createTextNode(" seconds."));

    var btnRow = document.createElement("div");
    btnRow.style.cssText = "display:flex;gap:10px;justify-content:flex-end;";

    var logoutBtn = document.createElement("button");
    logoutBtn.type = "button";
    logoutBtn.textContent = "Sign out now";
    logoutBtn.style.cssText =
      "background:transparent;color:#6E6A5C;border:1px solid #E3DDC8;" +
      "border-radius:4px;padding:8px 14px;font-size:13px;cursor:pointer;";
    logoutBtn.addEventListener("click", function () {
      window.location.href = logoutUrl;
    });

    var stayBtn = document.createElement("button");
    stayBtn.type = "button";
    stayBtn.textContent = "Stay signed in";
    stayBtn.style.cssText =
      "background:#2C4A3B;color:#FBF9F2;border:none;border-radius:4px;" +
      "padding:8px 14px;font-size:13px;cursor:pointer;";
    stayBtn.addEventListener("click", markActive);

    btnRow.appendChild(logoutBtn);
    btnRow.appendChild(stayBtn);
    box.appendChild(heading);
    box.appendChild(body);
    box.appendChild(btnRow);
    overlay.appendChild(box);
    return overlay;
  }

  function showWarning(secondsLeft) {
    if (!modal) {
      modal = buildModal();
      document.body.appendChild(modal);
    }
    countdownEl.textContent = secondsLeft;
    modal.style.display = "flex";
    warned = true;
  }

  function hideWarning() {
    if (modal) modal.style.display = "none";
    warned = false;
  }

  setInterval(function () {
    var idleSeconds = Math.floor((Date.now() - lastActivity) / 1000);
    var secondsLeft = timeoutSeconds - idleSeconds;

    if (secondsLeft <= 0) {
      window.location.href = logoutUrl;
      return;
    }
    if (secondsLeft <= warnBeforeSeconds) {
      showWarning(secondsLeft);
    }
  }, 1000);
})();
