setTimeout(function(){
    console.log("Time: 5s");
    }, 5000
    );

setTimeout(function(){
    console.log("Time: 10s");
    var port = chrome.runtime.connectNative('host_manifest'); // runs python script

    port.onMessage.addListener(function(msg) {
      console.log("Received: " + msg.text);
    });

    port.onDisconnect.addListener(function() {
      console.log("Disconnected");
    });

    port.postMessage({ text: "Hello, my_application. you boii" });
    console.log("Attempted to send to host.")
    }, 10000
    );


setTimeout(function(){
    console.log("Time: 15s");
    }, 15000
    );


setTimeout(function(){
    console.log("Time: 20s");
    var port = chrome.runtime.connectNative('host_manifest');

    port.onMessage.addListener(function(msg) {
      console.log("Received: " + msg.text);
    });

    port.onDisconnect.addListener(function() {
      console.log("Disconnected");
    });

    port.postMessage({ text: "Hello, my_application" });
    console.log("Attempted to send to host.")
    }, 20000
    );


setTimeout(function(){
    console.log("Time: 25s");
    }, 25000
    );