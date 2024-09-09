var socket = io();
console.log("INIT");
socket.emit('init_connection', {data: 'connected!'});
console.log("INIT Connnection sent.");


function selectThisDate(date){
  socket.emit('select_date', {date: date});
  window.location.href = "http://192.168.0.9:5000/gallery";
}

