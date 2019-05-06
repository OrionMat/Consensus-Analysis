var contextMenuItem = {
  "id" : "check_statement",
  "title" : "Check Statement",
  "contexts" : ["selection"]
};
chrome.contextMenus.create(contextMenuItem)

function is_valid_statement(text){
  // checks text is valid
  return true
}

chrome.contextMenus.onClicked.addListener(function(clickedData){
  if (clickedData.menuItemId == "check_statement" && clickedData.selectionText){
    if (is_valid_statement(clickedData.selectionText)){

      chrome.storage.sync.set({'statement': clickedData.selectionText});
      var port = chrome.runtime.connectNative('host_manifest'); // runs python script

      port.onMessage.addListener(function(msg) {
        if(msg.name == 'articleNumbers'){
          chrome.storage.sync.set({'num_Articles': msg.num_Articles}); 
        }
        if(msg.name == 'articleAgencies'){
          chrome.storage.sync.set({'agencies': msg.agencies});
        }
        if(msg.name == "articleTitles"){
          chrome.storage.sync.set({"titles" : msg.titles});
        }
        if(msg.name == "articleDates"){
          chrome.storage.sync.set({"dates" : msg.dates});
        }
        if(msg.name == "articleURLs"){
          chrome.storage.sync.set({"urls" : msg.urls});
        }
        if(msg.name == "articleResults"){
          console.log(msg.results)
          chrome.storage.sync.set({"results" : msg.results})
        }
      });

      port.onDisconnect.addListener(function() {
        console.log("Disconnected");
      });
      port.postMessage({ text: clickedData.selectionText });
      console.log("Attempted to send to host.")
    }
  }
});

chrome.storage.onChanged.addListener(function(changes, storageName){
  // create a notification
  var notifOptions = {
    type: "basic",
    iconUrl: "images/blueTick.png",
    title: "Done!",
    message: "The results are in, check em out."
  };
  chrome.notifications.create('doneNotif', notifOptions);
  //alert("Done!")
});