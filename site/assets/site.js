/* The Console: fills the three panels for the chosen trade and city from the keyword universe.
   Everything on the page works without this script; it only updates the numbers in place. */
(function () {
  var trade = document.getElementById('trade'), city = document.getElementById('city');
  if (!trade || !city || !window.fetch) return;
  var data = null;
  function fill() {
    if (!data) return;
    var t = data[trade.value], cityKey = city.value, cityName = city.options[city.selectedIndex].text;
    var tradeName = trade.options[trade.selectedIndex].text;
    var d = (t && t.c && t.c[cityKey]) || null;
    var set = function (sel, text) { document.querySelectorAll(sel).forEach(function (el) { el.textContent = text; }); };
    set('[data-trade-name]', tradeName.toLowerCase());
    set('[data-city-name]', cityName);
    if (d) {
      set('[data-count]', d.n.toLocaleString('en-US'));
      set('[data-ex1]', d.ex[0] || ''); set('[data-ex2]', d.ex[1] || ''); set('[data-kinds]', String(d.k));
    }
    var isPlumb = trade.value === 'plumbers';
    set('[data-confirm-status]', isPlumb ? 'First run' : 'Not run yet');
    set('[data-confirm-big]', isPlumb ? 'In progress' : 'Coming');
    set('[data-confirm-line]', isPlumb ? 'The AI Recommendation Index is being run for plumbers in the launch cities this month. Published when it is done.' : 'The Index runs trade by trade. ' + tradeName + ' in ' + cityName + ' is not published yet; ask to be told when it is.');
  }
  fetch('/assets/console-data.json').then(function (r) { return r.json(); }).then(function (j) { data = j; fill(); }).catch(function () {});
  trade.addEventListener('change', fill); city.addEventListener('change', fill);
})();
