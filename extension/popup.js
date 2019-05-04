$(function(){
    // gets title value to display when popup opened
    chrome.storage.sync.get('title', function(result){ // can change to array to get more than just title i.e ['title', 'link']
        $('#title').text(result.title);
    });

    chrome.storage.sync.get('statement', function(result){ // can change to array to get more than just title i.e ['title', 'link']
        $('#statementTitle').text(result.statement);
    });
});

// create a notification
// chrome.notifications.create('tester', {
//     type: 'basic',
//     iconUrl: 'blueTick.png',
//     title: 'This makes a sound',
//     message: 'and it appears in the browser!'
// }, function(notificationId) {});