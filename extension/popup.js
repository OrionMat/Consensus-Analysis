$(function(){

    // displays the statement that is being searched
    // gets statement value from storage to display when popup opened
    chrome.storage.sync.get('statement', function(result){ // can change to array to get more than just title i.e ['title', 'link']
        $('#statementTitle').text("\""+result.statement+"\"");
    });

    // gets number of articles from storage
    chrome.storage.sync.get('num_Articles', function(result){
        var num_Articles = result.num_Articles; 

        var tableHead = "<table><tr><th>Agency</th><th>Article</th><th>Date</th><th>Result</th></tr>";
        var tableMid = ""
        var tableEnd = "</table>";

        var i;
        for(i = 0; i < num_Articles; i++) {
            tableMid += "<tr>"
            tableMid += "<td id=\"agency" + i.toString() + "\"></td>";
            tableMid += "<td><a id=\"title" + i.toString() + "\" href=\"\"  target=\"_blank\"></a></td>";
            tableMid += "<td id=\"date" + i.toString() + "\"></td>";
            tableMid += "<td id=\"result" + i.toString() + "\"></td>";
            tableMid += "</tr>"
        }
        
        var summaryTable = tableHead + tableMid + tableEnd;
        $('#tablePrint').html(summaryTable);
    });

    // displays an article title in the tabel
    // gets title value from storage to display when popup opened
    chrome.storage.sync.get(['titles', 'dates', 'urls', 'agencies'], function(result){ // can change to array to get more than just title i.e ['title', 'link']
        agency_array = JSON.parse(result.agencies)
        title_array = JSON.parse(result.titles)
        date_array = JSON.parse(result.dates)
        url_array = JSON.parse(result.urls)

        var i;
        for(i = 0; i<title_array.length; i++){
            switch(agency_array[i]) {
                case 'NYT':
                    $('#agency' + String(i)).prepend("<img src=\"images\\NYT_image.png\" alt=\"NYT Logo\" width=\"45\" height=\"30\">")
                    break;
                case 'BBC':
                    $('#agency' + String(i)).prepend("<img src=\"images\\BBC_image.png\" alt=\"BBC Logo\" width=\"48\" height=\"48\">")
                    break;
                case 'AP':
                    $('#agency' + String(i)).prepend("<img src=\"images\\AP_image.png\" alt=\"BBC Logo\" width=\"48\" height=\"48\">")
                    break;
                case 'Reuters':
                    $('#agency' + String(i)).prepend("<img src=\"images\\R_image.jpg\" alt=\"BBC Logo\" width=\"48\" height=\"48\">")
                    break;
                default:
                  // code block
              }
            // if(agency_array[i] == 'BBC'){
            //     $('#agency' + String(i)).prepend("<img src=\"images\\BBC_image.png\" alt=\"BBC Logo\" width=\"48\" height=\"48\">")
            // }
            // $('#agency' + String(i)).text();
            $('#title' + String(i)).attr("href", url_array[i]);
            $('#title' + String(i)).text(title_array[i]);
            $('#date' + String(i)).text(date_array[i]);
        }
        // $('#title0').text(json_arr[0]);
        //$('#title1').text(result.reuterstitles[1]);
    });

});

// create a notification
// chrome.notifications.create('tester', {
//     type: 'basic',
//     iconUrl: 'images/blueTick.png',
//     title: 'This makes a sound',
//     message: 'and it appears in the browser!'
// }, function(notificationId) {});