//setTimeout(function(){
//    console.log("Time: 5s");
//    }, 5000
//    );

setTimeout(function(){
    console.log("Time: 10s");
    var port = chrome.runtime.connectNative('host_manifest'); // runs python script

    port.onMessage.addListener(function(msg) {
      console.log("Received: " + msg.text);
    });

    port.onDisconnect.addListener(function() {
      console.log("Disconnected");
    });

    port.postMessage({ text: "Shares in Boeing fell" });
    console.log("Attempted to send to host.")
    }, 2000
    );