var socket = io();
console.log("INIT");
socket.emit('init_connection', {data: 'connected!'});
console.log("INIT Connnection sent.");


function selectThisDate(date){
  socket.emit('select_date', {date: date});
  window.location.href = window.location.href + "gallery?eventdate=" + date;
}
function redirectToAdEvent(){
  window.location.href = window.location.href + "newevent";
}
