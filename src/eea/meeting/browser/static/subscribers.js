/* globals DataTable */
/* jslint:disable */

(function(){
  function isVisible(e) {
    return !!( e.offsetWidth || e.offsetHeight || e.getClientRects().length );
  }

  function setup_datatable(selector){
    var table = new DataTable(
      document.querySelector(selector), {
        perPage: 25,
        perPageSelect: [25, 50, 100, 500]
    });

    // Don't sort first column.
    var checkbox_sorter = table.table.querySelector('.dataTable-sorter');
    checkbox_sorter.parentNode.appendChild(checkbox_sorter.firstChild);
    checkbox_sorter.parentNode.removeChild(checkbox_sorter);
  }

  function setup_checkboxes() {
    var chk_all = document.querySelector('[data-role="select-all"]');

    if (chk_all) {
      chk_all.addEventListener('change', function(evt){
        var checkboxes = [].slice.call(
          document.querySelectorAll(
            '[data-role="select-subscriber"]'
          )
        ).filter(isVisible);
        checkboxes.forEach(function(chk){
          chk.checked = chk_all.checked;
        });
      });
    }

  }

  window.subscribers = {
    setup: function(selector) {
      setup_datatable(selector);
      setup_checkboxes();
    }
  };
})();
