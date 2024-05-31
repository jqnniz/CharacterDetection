var socket = io();
console.log("INIT");
socket.emit('init_connection', {data: 'connected!'});
console.log("INIT Connnection sent.");

socket.on('event_update', function(msg) {
    //console.log(msg);
    //document.getElementById('date1234').value = msg.date_str;
    //document.getElementById('event').value = msg.event_str;



  });


  socket.on('init_date_selection', function(msg) {
    //$('#textBox').append('<p>Received: ' + msg.data + '</p>'
    var options = "";
    options += "<option selected>Datum auswählen</option>";
    console.log(msg.data)
    var result = msg.data.replaceAll("(","");
    result = result.replaceAll(")","");
    result = result.replaceAll("]","");
    result = result.replaceAll("[","");
    result = result.replaceAll(",, ",",");
    result = result.replaceAll("'","");
    result = result.replaceAll(" ","");
    const myArray = result.split(",");
    console.log(myArray)

    for(var i = 0; i < myArray.length; i++){
      console.log(myArray[i]);
      if(myArray[i].length > 0){
        options += "<option value="+ myArray[i]+">"+ myArray[i] +"</option>";

      }
    }
    document.getElementById('selectDate').innerHTML = options;
    document.getElementById('gallery').style.display = 'None';

  });

// Funktion zum Öffnen des Bildes in der Überlagerung
function clicked_img(element) {
  var overlay = document.querySelector('.overlay');
  var topImage = document.getElementById('top');
  var closeButton = document.getElementById('close');

  topImage.src = element.src;
  overlay.style.display = 'flex';
  topImage.hidden = false;
  closeButton.hidden = false;
}

// Funktion zum Schließen der Überlagerung
function do_close() {
  var overlay = document.querySelector('.overlay');
  var topImage = document.getElementById('top');
  var closeButton = document.getElementById('close');

  overlay.style.display = 'none';
  topImage.hidden = true;
  closeButton.hidden = true;
}

// Event-Listener für das Schließen der Überlagerung, wenn außerhalb des Bildes geklickt wird
document.querySelector('.overlay').addEventListener('click', function(event) {
  if (event.target === this) {
      do_close();
  }
});

// Event-Listener für die automatische Übermittlung des Formulars nach Auswahl einer Datei
document.getElementById('fileInput').addEventListener('change', function() {
  document.getElementById('uploadForm').submit();
});

// Event-Listener für die automatische Übermittlung des Formulars nach Auswahl einer Datei
document.getElementById('fileInput2').addEventListener('change', function() {
  document.getElementById('uploadForm2').submit();
});


function submitDate(){
  document.getElementById('uploadForm').submit();
}
function submitFileUpload(){
  document.getElementById('uploadForm2').submit();
}
function submitEvent(){

  if(document.getElementById('date').value == ""){
    console.log("datum fehlt")
  }else{
    document.getElementById('newevent').submit();

  }

}

function selectDate(){
  document.getElementById('date').value = document.getElementById('selectDate').value;

  socket.emit('select_date', {date: document.getElementById('date').value});
  //setTimeout(window.location.replace("/gallery"),2000);
  //window.location.replace("/gallery");

  //document.getElementById('gallery').style.visibility = true;
  document.getElementById('gallery').style.display = 'Block';
}

