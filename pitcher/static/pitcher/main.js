var firebaseConfig = {
     apiKey: 'AIzaSyBTlSwWe6lD6NLi8OrDPe49qWIllNgttMI',
    authDomain: 'pitcher-275100.firebaseapp.com',
    databaseURL: 'https://pitcher-275100.firebaseio.com',
    projectId: 'pitcher-275100',
    storageBucket: 'pitcher-275100.appspot.com',
    messagingSenderId: '1008306122255',
    appId: '1:1008306122255:web:58559788fa73c384fcbd7a',
    measurementId: 'G-GPL016L81F',
    };

var fb= firebase.initializeApp(firebaseConfig);

var storage = firebase.storage();

function pitch_click(t) {
    var modal = document.getElementById("myModal");
    var btn = t;
    var span = document.getElementsByClassName("close")[0];
    var all = t.getElementsByTagName('div')
    console.log(all)
    document.getElementById('title').innerHTML = all[0].innerHTML;
    document.getElementById('status').innerHTML = all[1].innerHTML;
    document.getElementById('date').innerHTML = all[2].innerHTML;
    document.getElementById('gist').innerHTML = all[3].innerHTML;
    document.getElementById('tags').innerHTML = all[4].innerHTML;
    document.getElementById('whole').innerHTML = all[5].innerHTML;
    document.getElementById('contributors').innerHTML = all[6].innerHTML;
    document.getElementById('investors').innerHTML = all[7].innerHTML;
    var k = document.getElementById('myModal').getElementsByClassName('key');
    var key = t.getElementsByTagName("input")[0].value;
    k[0].setAttribute('value', key);
    k[1].setAttribute('value', key);


    btn.onclick = function () {modal.style.display = "block";}
    span.onclick = function () {modal.style.display = "none";}
    window.onclick = function (event) {
        if (event.target == modal) {modal.style.display = "none";}
    }
}

function upload_media() {
    var file = document.getElementById('files').files[0];
    //console.log(file);
    if (file != undefined) {
        var storageRef = storage.ref("pitches/");
        var thisRef = storageRef.child(file.name).put(file);
        storageRef.child(file.name).getDownloadURL().then(function (url) {
            console.log(url);
            document.getElementById("url").value = url;
        });
    }
    document.getElementById("pitch_form").submit();
}

function edit_pitch(){
    div = document.getElementById("edit-pitch");
}

/////////// chat  ////////
var element = document.getElementById("maindiv");
var toAdd = document.createDocumentFragment();
//database polling for new child
var starCountRef = firebase.database().ref("users/chatrooms/"+ chatId ).on('child_added', function(snapshot){console.log(snapshot.val());snapshot.forEach(function(childSnapshot){addMessage(childSnapshot.key, childSnapshot.val());})});

function addMessage(key,message){
      var newDiv = document.createElement('div');
      newDiv.innerHTML = message;
      newDiv.className = 'demo';
      toAdd.appendChild(newDiv);
      element.appendChild(toAdd);
}
function sendMessage(){
      var msg = document.getElementById("messagearea");
      console.log(msg.value);
      var starCountRef = firebase.database().ref("users/chatrooms/"+ chatId ).push({"investor":msg.value});
}

