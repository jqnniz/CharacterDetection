var socket = io();
console.log("INIT");
socket.emit('init_connection', {data: 'connected!'});
console.log("INIT Connnection sent.");

// var dataPoints = [
//   { label: "Learning Colors", y: 4.91 },
//   { label: "Uptown Funk", y: 4.96 },
//   { label: "Wheels on the Bus", y: 5.36 },
//   { label: "Phonics Song with Two Words", y: 5.36 },
//   { label: "See You Again", y: 5.94 },
//   { label: "Shape of You", y: 6.02 },
//   { label: "Bath Song", y: 6.26 },
//   { label: "Johny Johny Yes Papa", y: 6.73 },
//   { label: "Despacito", y: 8.20 },
//   { label: "Baby Shark Dance", y: 13.01 }
// ]
var yVal  = 0;
var xVal  = 0;

var dataPoints = []
//   { label: "Learning Colors", y: 4.91 },
//   { label: "Uptown Funk", y: 4.96 },
//   { label: "Wheels on the Bus", y: 5.36 },
//   { label: "Phonics Song with Two Words", y: 5.36 },
//   { label: "See You Again", y: 5.94 },
//   { label: "Shape of You", y: 6.02 },
//   { label: "Bath Song", y: 6.26 },
//   { label: "Johny Johny Yes Papa", y: 6.73 },
//   { label: "Despacito", y: 8.20 },
//   { label: "Baby Shark Dance", y: 13.01 }
// ]
var chart = new CanvasJS.Chart("chartContainer", {
  theme: "dark2", // "light1", "light2", "dark1"
  animationEnabled: true,
  exportEnabled: true,
  title: {
    text: "Anzahl Konzerte je Künstler"
  },
  axisX: {
    margin: 20,
    labelPlacement: "inside",
    tickPlacement: "inside"
  },
  axisY2: {
    title: "Konzerte",
    titleFontSize: 14,
    includeZero: true,
    suffix: ""
  },
  data: [{
    type: "bar",
    yValueFormatString: "#",
    indexLabel: "{y}",
    axisYType: "secondary",
    dataPoints: dataPoints
  }]
});


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
socket.on('artist_values', function(msg) {
  
  for (var j = 0; j < 10; j++) {
    yVal = yVal +  Math.round(5 + Math.random() *(-5-5));
    dataPoints.push({
      label: "Test",
      y: yVal
    });
    xVal++;
  }
  chart.render();

});



window.onload = function () {



  chart.render();
  
  }