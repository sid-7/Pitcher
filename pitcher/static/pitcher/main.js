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
    span.onclick = function () {modal.style.display = "none";document.getElementById('video').src = '';};
    modal.style.display = "none";
    modal.style.display = "block";

    var all = t.getElementsByTagName('div');
    document.getElementById('title').innerHTML = "<b>Title: </b>" + all[0].innerHTML;
    document.getElementById('status').innerHTML = "<b>Status: </b>" + all[1].innerHTML;
    document.getElementById('date').innerHTML = "<b>Date: </b>" + all[2].innerHTML;
    document.getElementById('gist').innerHTML = "<b>GIST: </b>" + all[3].innerHTML;
    document.getElementById('tags').innerHTML = "<b>Tags: </b>" + all[4].innerHTML;
    document.getElementById('whole').innerHTML = "<b>Description: </b>" + all[5].innerHTML;
    document.getElementById('contributors').innerHTML = "<b>Number of Contributors: </b>" + all[6].innerHTML;
    document.getElementById('investors').innerHTML = "<b>Number of Investors: </b>" + all[7].innerHTML;
        document.getElementById('video').src = all[8].innerHTML;

    var k = document.getElementById('myModal').getElementsByClassName('key');
    var key = t.getElementsByTagName("input")[0].value;
    k[0].setAttribute('value', key);
    k[1].setAttribute('value', key);


    window.onclick = function (event) {
        if (event.target == modal) {modal.style.display = "none";document.getElementById('video').src = '';}
    }
}
function upload(){
    var file = document.getElementById('files').files[0];
    //console.log(file);
    if (file != undefined) {
        const promices = [];
        const upload_task = storage.ref("pitches").put(file);
        promices.push(upload_task);
        upload_task.on('state_changed', snapshot => {
            const progress = (snapshot.bytesTransfered / snapshot.totalBytes)*100;
        }, error =>{
            console.log(error);
        }, () =>{
            upload_task.snapshot.ref.getDownloadURL().then(downloadURL => {
                console.log(downloadURL);
                document.getElementById("url").setAttribute("value", downloadURL);
                document.getElementById("url").value = downloadURL;
                console.log(document.forms['new_pitch']);
                alert("File is uploaded");
            } );
        } );
    }
    else{
        alert("Please add a video!");
        return false;
    }
}
function validate_and_upload_media() {
    if(document.getElementsByName("title")[0].value == ""){
        alert("Title cannot be empty!");
        document.getElementsByName("title")[0].focus();
        return false;
    }
    if(document.getElementsByName("description")[0].value == ""){
        alert("Description cannot be empty!");
        document.getElementsByName("description")[0].focus();
        return false;
    }
    return true;
}

function edit_pitch(){
    div = document.getElementById("edit-pitch");
}

/////////// chat  ////////
var element;
var toAdd = document.createDocumentFragment();
var chatId;
function initiate_chat() {
    chatId = document.getElementById("chatId").value;
    element = document.getElementById("maindiv");
    //database polling for new child
    firebase.database().ref("users/chatrooms/" + chatId + "/messages").on('child_added', function (snapshot) {
            snapshot.forEach(function (childSnapshot) {
                addMessage(childSnapshot.key, childSnapshot.val());
            })
        }
    );
        document.getElementById("messagearea").addEventListener("keyup", function(event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        document.getElementById("chatbutton").click();
      }
    });
}

function addMessage(key, message) {
    var newDiv = document.createElement('div');
    newDiv.innerHTML = message;
    newDiv.className = key;
    toAdd.appendChild(newDiv);
    element.appendChild(toAdd);
    element.scrollTop = element.scrollHeight;
}

function sendMessage() {
    var msg = document.getElementById("messagearea");
    var starCountRef = firebase.database().ref("users/chatrooms/" + chatId + "/messages").push({"pitcher": msg.value});
    document.getElementById("messagearea").value = "";
}
