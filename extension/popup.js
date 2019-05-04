$(function(){

    // displays the statement that is being searched
    // gets statement value from storage to display when popup opened
    chrome.storage.sync.get('statement', function(result){ // can change to array to get more than just title i.e ['title', 'link']
        $('#statementTitle').text(result.statement);
    });

    // gets number of articles from storage
    chrome.storage.sync.get('numArticles', function(result){
        var numArticles = result.numArticles; 
        $('#artNum').text(numArticles);

        var tableHead = "<table><tr><th>Agency</th><th>Article</th><th>Date</th><th>Result</th><th>Link</th></tr>";
        var tableMid = ""
        var tableEnd = "</table>";

        var i;
        for(i = 0; i < numArticles; i++) {
            tableMid += "<tr>"
            tableMid += "<td id=\"agency" + i.toString() + "\">ag</td>";
            tableMid += "<td id=\"title" + i.toString() + "\">tit</td>";
            tableMid += "<td id=\"date" + i.toString() + "\">dat</td>";
            tableMid += "<td id=\"result" + i.toString() + "\">res</td>";
            tableMid += "<td id=\"link" + i.toString() + "\">lin</td>";
            tableMid += "</tr>"
        }
        
        var summaryTable = tableHead + tableMid + tableEnd;
        $('#tablePrint').html(summaryTable);
    });

    // displays an article title in the tabel
    // gets title value from storage to display when popup opened
    chrome.storage.sync.get(['titles', 'dates'], function(result){ // can change to array to get more than just title i.e ['title', 'link']
        titles_array = JSON.parse(result.titles)
        dates_array = JSON.parse(result.dates)

        var i;
        for(i = 0; i<titles_array.length; i++){
            $('#title' + String(i)).text(titles_array[i]);
            $('#date' + String(i)).text(dates_array[i]);
        }
        // $('#title0').text(json_arr[0]);
        //$('#title1').text(result.reuterstitles[1]);
    });

});

// create a notification
// chrome.notifications.create('tester', {
//     type: 'basic',
//     iconUrl: 'blueTick.png',
//     title: 'This makes a sound',
//     message: 'and it appears in the browser!'
// }, function(notificationId) {});