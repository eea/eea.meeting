function export_excel()
{
  var table = $("#listing-table").tableToJSON();
  JSONToCSVConvertor(table, "Email Archive", true);
}


function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {
    //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

    var CSV = '';

    if (ShowLabel) {
        var row = "";

        for (var index in arrData[0]) {
            //convert each value to string and comma-seprated
            row += index + ',';
        }

        row = row.slice(0, -1);

        //append Label row
        CSV += row + '\r\n';
    }

    //extract each row
    for (var i = 0; i < arrData.length; i++) {
        var row = "";

        //extract each column and convert it in string comma-seprated
        for (var index in arrData[i]) {
            row += '"' + arrData[i][index] + '",';
        }

        row.slice(0, row.length - 1);

        //add a line break after each row
        CSV += row + '\r\n';
    }

    if (CSV == '') {
        alert("Invalid data");
        return;
    }

    //Generate a file name
    var fileName = "Export_";
    //remove the blank-spaces from the title and replace it with an underscore
    fileName += ReportTitle.replace(/ /g,"_");

    //Initialize file format
    var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);

    var link = document.createElement("a");
    link.href = uri;

    link.style = "visibility:hidden";
    link.download = fileName + ".csv";

    //remove the temporary anchor after clicking it
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
