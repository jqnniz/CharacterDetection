var socket = io();
console.log("INIT");
console.log(document.getElementById("date1234"));

socket.on('event_update', function(msg) {
    //console.log(msg);
    //document.getElementById('date1234').value = msg.date_str;
    //document.getElementById('event').value = msg.event_str;



  });


  function clicked_img(img,fp){
    console.log(img.src);

    var top=document.getElementById('top')

    top.src = img.src;

    top.hidden=false;


    if (img.naturalWidth<screen.width*0.6 && img.naturalHeight<screen.height*0.6) {

      top.width=img.naturalWidth;
      top.height=img.naturalHeight;

    } else {

      top.width=screen.width*0.6;
      top.height=img.naturalHeight/img.naturalWidth*top.width;

    }

    document.getElementById('close').hidden = false;
}


function do_close(){
document.getElementById('top').hidden=true;
document.getElementById('close').hidden=true;
}