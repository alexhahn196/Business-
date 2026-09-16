/* PLAYHEAD — small progressive-enhancement script.
   In Framer these behaviours are native: Appear effects, Accordion component,
   CMS filters, Nav overlay. Kept minimal so the HTML stays a clean reference. */
(function () {
  // Appear on scroll (Framer: Effects → Appear)
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 }) : null;
  document.querySelectorAll('.appear').forEach(function (el) { io ? io.observe(el) : el.classList.add('is-in'); });

  // Mobile nav
  var burger = document.querySelector('.nav-burger');
  var mobile = document.querySelector('.nav-mobile');
  if (burger && mobile) burger.addEventListener('click', function () {
    var open = mobile.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // FAQ accordion (Framer: Accordion component)
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', function () {
      var open = item.classList.toggle('is-open');
      q.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Work filter chips (Framer: CMS filter on a Collection List)
  var chips = document.querySelectorAll('[data-filter]');
  var cards = document.querySelectorAll('[data-format]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('is-active'); });
      chip.classList.add('is-active');
      var f = chip.getAttribute('data-filter');
      cards.forEach(function (card) {
        var show = f === 'all' || card.getAttribute('data-format') === f;
        card.classList.toggle('is-hidden', !show);
      });
      document.querySelectorAll('.work-group').forEach(function (g) {
        g.classList.toggle('is-hidden', !g.querySelector('[data-format]:not(.is-hidden)'));
      });
    });
  });

  // Duplicate marquee track for seamless loop
  document.querySelectorAll('.marquee-track').forEach(function (track) {
    track.innerHTML = track.innerHTML + track.innerHTML;
  });

  // Year in footer
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Demo form: prevent navigation
  document.querySelectorAll('form[data-demo]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); var b = f.querySelector('button[type=submit]'); if (b) { b.textContent = 'Sent — talk soon'; b.disabled = true; } });
  });
})();
