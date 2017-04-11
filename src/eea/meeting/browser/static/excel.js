$(document).ready(function() {
  $("#btnExport").click(function(e) {
    e.preventDefault();

    var data_type = 'data:application/vnd.ms-excel';
    var table_div = document.getElementById('table_wrapper');
    var table_html = table_div.outerHTML.replace(/ /g, '%20');

    var a = document.createElement('a');
    a.href = data_type + ', ' + table_html;
    a.download = 'email_archive.xls';
    a.click();
  });
});