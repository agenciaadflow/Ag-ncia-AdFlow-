/* AdFlow · WhatsApp, rastreamento e formulário do diagnóstico */
var WHATS_NUMERO = "5545999407123";

/* Rastreamento: quando os IDs forem instalados no <head> (fbq e gtag), os eventos passam a ser enviados. */
function track(evento, dados) {
  try { if (typeof window.fbq === "function") window.fbq("track", evento, dados || {}); } catch (e) {}
  try { if (typeof window.gtag === "function") window.gtag("event", evento === "Contact" ? "contact" : evento, dados || {}); } catch (e) {}
}

function whatsLink(msg) {
  return "https://wa.me/" + WHATS_NUMERO + "?text=" + encodeURIComponent(msg);
}

function whats(msg) {
  track("Contact", { origem: msg });
  var w = window.open(whatsLink(msg), "_blank", "noopener");
  if (!w) window.location.href = whatsLink(msg);
}

document.addEventListener("DOMContentLoaded", function () {
  /* Todo elemento com data-whats vira um link de WhatsApp com a mensagem pronta. */
  document.querySelectorAll("[data-whats]").forEach(function (el) {
    var msg = el.getAttribute("data-whats");
    if (el.tagName === "A") {
      el.href = whatsLink(msg);
      el.target = "_blank";
      el.rel = "noopener";
      el.addEventListener("click", function () { track("Contact", { origem: msg }); });
    } else {
      el.addEventListener("click", function () { whats(msg); });
    }
  });

  /* FAQ em acordeão: abre um por vez. */
  document.querySelectorAll(".faq").forEach(function (faq) {
    faq.querySelectorAll("details").forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (!d.open) return;
        faq.querySelectorAll("details[open]").forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  });


  /* Brilho que acompanha o mouse (no celular, flutua devagar). */
  var glow = document.querySelector(".glow");
  var reduz = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (glow && !reduz) {
    var tx = window.innerWidth / 2, ty = window.innerHeight * 0.3, x = tx, y = ty, mexeu = false;
    window.addEventListener("pointermove", function (e) {
      if (e.pointerType === "mouse") { tx = e.clientX; ty = e.clientY; mexeu = true; }
    }, { passive: true });
    var t0 = Date.now();
    (function loop() {
      if (!mexeu) {
        var t = (Date.now() - t0) / 1000;
        tx = window.innerWidth * (0.5 + 0.3 * Math.sin(t / 4));
        ty = window.innerHeight * (0.35 + 0.2 * Math.cos(t / 5));
      }
      x += (tx - x) * 0.08; y += (ty - y) * 0.08;
      glow.style.transform = "translate3d(" + x + "px," + y + "px,0)";
      requestAnimationFrame(loop);
    })();
  }

  /* Ampliar print dos resultados. */
  var zoom = document.getElementById("zoom");
  if (zoom && typeof zoom.showModal === "function") {
    var zimg = zoom.querySelector("img");
    document.querySelectorAll("[data-zoom]").forEach(function (b) {
      b.addEventListener("click", function () { zimg.src = b.getAttribute("data-zoom"); zoom.showModal(); });
    });
    zoom.querySelector(".zclose").addEventListener("click", function () { zoom.close(); });
    zoom.addEventListener("click", function (e) { if (e.target === zoom) zoom.close(); });
  }

  /* Formulário do diagnóstico: monta a mensagem e abre o WhatsApp. */
  var form = document.getElementById("form-diagnostico");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };
      var anuncia = form.querySelector('input[name="anuncia"]:checked');
      var disposto = form.querySelector('input[name="disposto"]:checked');
      var linhas = [
        "Olá, Josânia! Quero agendar o diagnóstico gratuito do meu marketing.",
        "Nome: " + (v("d-nome") || "-"),
        "Empresa: " + (v("d-empresa") || "-"),
        "Segmento: " + (v("d-segmento") || "-"),
        "Cidade: " + (v("d-cidade") || "-"),
        "Instagram: " + (v("d-instagram") || "-"),
        "Já investe em anúncios? " + (anuncia ? anuncia.value : "-"),
        "Está disposto a investir em anúncios? " + (disposto ? disposto.value : "-")
      ];
      whats(linhas.join("\n"));
    });
  }
});
