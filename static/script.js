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
function submitFileUpload(){
  document.getElementById('uploadForm2').submit();
}
function redirectToAddEvent(){
  window.location.href = window.location.href + "newevent";
}
function submitEvent(){
  if(document.getElementById('date').value == ""){
    console.log("datum fehlt")
  }else{
    document.getElementById('newevent').submit();
  }
}

function clicked_img(element) {
  console.log(element);
  var socket = io();
  socket.emit('selectTitleImage',{data: element.src})

  element.style = "border: 5px solid #5A5;"
}