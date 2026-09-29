// Keskpuur – shared script (all pages)
(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Open/closed banner, computed in Tallinn time whatever the visitor's timezone.
  // EDIT: days the space is open (0 = Sunday ... 6 = Saturday) and hours.
  var OPEN_DAYS = [0, 1, 2, 3, 4, 5, 6];
  var OPEN = 11 * 60, CLOSE = 15 * 60;
  var el = document.getElementById('status');
  if (!el) return;
  try {
    var p = {};
    new Intl.DateTimeFormat('en-GB', {timeZone: 'Europe/Tallinn', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false})
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var day = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(p.weekday);
    var mins = (+p.hour % 24) * 60 + +p.minute;
    var open = OPEN_DAYS.indexOf(day) > -1 && mins >= OPEN && mins < CLOSE;
    el.className = 'status' + (open ? ' is-open' : '');
    el.innerHTML = open
      ? '<b>Open now</b> until 15:00'
      : '<b>Closed now</b> · open 11:00–15:00 and by appointment';
  } catch (e) {}
})();
