(function () {
  var sections = Array.prototype.slice.call(document.querySelectorAll(".docs-section"));
  var topLinks = {};
  document.querySelectorAll(".docs-nav-top").forEach(function (link) {
    topLinks[link.getAttribute("href").slice(1)] = link;
  });

  var active = null;
  var line = 120;
  var ticking = false;

  function setActive(id) {
    if (id === active) return;
    if (active && topLinks[active]) topLinks[active].classList.remove("active");
    if (id && topLinks[id]) topLinks[id].classList.add("active");
    active = id;
  }

  function update() {
    ticking = false;
    var current = sections[0].id;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].getBoundingClientRect().top <= line) {
        current = sections[i].id;
      } else {
        break;
      }
    }
    setActive(current);
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
})();
