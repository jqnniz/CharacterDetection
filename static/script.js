var socket = io();
console.log("INIT");
console.log(document.getElementById("date1234"));

socket.on('event_update', function(msg) {
    console.log(msg);
    document.getElementById('date1234').value = msg.date_str;
    document.getElementById('event').value = msg.event_str;



  });