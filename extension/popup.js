$(function(){
    // gets title value to display when popup opened
    chrome.storage.sync.get('title', function(result){ // can change to array to get more than just title i.e ['title', 'link']
        $('#title').text(result.title);
    });
});