function fnExcelReport() {
    var tab_text = '<html xmlns:x="urn:schemas-microsoft-com:office:excel">';
    tab_text = tab_text + '<head><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>';

    tab_text = tab_text + '<x:WorksheetOptions><x:Panes></x:Panes></x:WorksheetOptions></x:ExcelWorksheet>';
    tab_text = tab_text + '</x:ExcelWorksheets></x:ExcelWorkbook></xml></head><body>';

    tab_text = tab_text + "<table border='1px'>";

    // remove sortdisplay spans from excel output in order to avoid strange characters
    // from showing up within the excel export
    var $display_email = $('.display-email');
    var $sort_direction = $display_email.find('.sortdirection').detach();

    tab_text = tab_text + $display_email.html();
    tab_text = tab_text + '</table></body></html>';

    var data_type = 'data:application/vnd.ms-excel';

    var ua = window.navigator.userAgent;
    var msie = ua.indexOf("MSIE ");

    if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)) {
        if (window.navigator.msSaveBlob) {
            var blob = new Blob([tab_text], {
                type: "application/csv;charset=utf-8;"
            });
            navigator.msSaveBlob(blob, 'Email_archive.xls');
        }
    } else {
        $('#email_download').attr({'href': data_type + ', ' + encodeURIComponent(tab_text),
            'download': 'Email_archive.xls'});
    }
    var $email_th = $display_email.find('.display-email-th');
    $email_th.each(function (idx, el) {
       $sort_direction.eq(idx).appendTo($(el));
    });

}