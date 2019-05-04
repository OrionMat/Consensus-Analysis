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
        console.log("Received: " + msg.text);
        chrome.storage.sync.set({'title': msg.text});

        chrome.storage.sync.set({'numArticles': "7"});
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
    iconUrl: "blueTick.png",
    title: "Done!",
    message: "The results are in, check em out."
  };
  chrome.notifications.create('doneNotif', notifOptions);
  //alert("Done!")
});