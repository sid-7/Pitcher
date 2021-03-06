var firebaseConfig = {
     apiKey: '',
    authDomain: '',
    databaseURL: '',
    projectId: '',
    storageBucket: '',
    messagingSenderId: '',
    appId: '',
    measurementId: '',
    };
var fb= firebase.initializeApp(firebaseConfig);

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
    document.getElementById('whole').innerHTML = "<b>Description: </b>" + all[4].innerHTML;
    document.getElementById('contributors').innerHTML = "<b>Number of Contributors: </b>" + all[5].innerHTML;
    document.getElementById('investors').innerHTML = "<b>Number of Investors: </b>" + all[6].innerHTML;
    document.getElementById('video').src = all[7].innerHTML;

    var k = document.getElementById('myModal').getElementsByClassName('pitch_key');
    var pitch_key = t.getElementsByTagName("input")[0].value;
    var pitcher_key = t.getElementsByTagName("input")[1].value;

    k[0].setAttribute('value', pitch_key);
    document.getElementById('myModal').getElementsByClassName('pitcher_key')[0].setAttribute('value', pitcher_key)

    var interested = t.getElementsByTagName("input")[2].value;
    if(interested=="True"){
        document.getElementById("interested_button").value = "Interested!";
        document.getElementById("interested_button").setAttribute("onclick","not_interested(this)");
    }
    else{
        document.getElementById("interested_button").value = "Show Interest?";
        document.getElementById("interested_button").setAttribute("onclick", "interested(this)");
    }

    span.onclick = function () {modal.style.display = "none";}
    window.onclick = function (event) {
        if (event.target == modal) {modal.style.display = "none";document.getElementById('video').src = '';}
    }
}

function not_interested(t){
    t.value = "Show Interest?"
    t.setAttribute("onclick", "interested(this)");
    var pitcher_Id = document.getElementById("myModal").getElementsByClassName("pitcher_key")[0].value;
    var investorId = document.getElementById("myModal").getElementsByClassName("investor_key")[0].value;
    var pitch_Id = document.getElementById("myModal").getElementsByClassName("pitch_key")[0].value;
    console.log(pitcher_Id, investorId, pitch_Id);
    // deleting related chatrooms
    firebase.database().ref("users/investors/"+investorId+"/chatrooms_ids").once("value", function(snapShot){
        snapShot.forEach(function(childSnapshot){
            console.log(childSnapshot.val()['pitch_id']);
            if(childSnapshot.val()['pitch_id'] == pitch_Id){
                console.log(childSnapshot.val());
                firebase.database().ref("users/chatrooms/" + childSnapshot.val()['key']).remove();
                firebase.database().ref("users/investors/"+investorId+"/chatrooms_ids/"+ childSnapshot.key).remove();
            }
        });
    });
    firebase.database().ref("users/investors/"+investorId+"/interested_pitches").once("value", function(snapShot){
        snapShot.forEach(function(childSnapshot) {
            if(childSnapshot.val()['pitch_id']==pitch_Id){
                firebase.database().ref("users/investors/"+investorId+"/interested_pitches/"+childSnapshot.key).remove();
            }
        });
    });
    firebase.database().ref("users/pitchers/"+ pitcher_Id + "/chatrooms_ids").once("value", function(snapShot) {
        snapShot.forEach(function(childSnapshot) {
            if((childSnapshot.val()['investor_id'] == investorId) && (childSnapshot.val()['pitch_id'] == pitch_Id)){
                firebase.database().ref("users/pitchers/"+ pitcher_Id + "/chatrooms_ids/"+ childSnapshot.key).remove();
            }
        });
    });

    //deleting investors in pitches
    firebase.database().ref("users/pitches/"+ pitcher_Id + "/" + pitch_Id + "/investors").once("value", function(snapShot){
        snapShot.forEach(function(childSnapshot){
            console.log(childSnapshot.val()['investor_id']);
            if(childSnapshot.val()['investor_id'] == investorId){
                console.log(childSnapshot.val());
                firebase.database().ref("users/pitches/"+ pitcher_Id + "/" + pitch_Id + "/investors" + "/" + childSnapshot.key).remove();
            }
        });
    });
    //deleting interested investors from the pitchers
    firebase.database().ref("users/pitchers/"+ pitcher_Id + "/interested_investors").once("value", function(snapShot){
        snapShot.forEach(function(childSnapshot){
            console.log(childSnapshot.val()['investor_id']);
            console.log(childSnapshot.val());
            if((childSnapshot.val()['investor_id'] == investorId) && (childSnapshot.val()['pitch_id'] == pitch_Id)){
                console.log(childSnapshot.val());
                firebase.database().ref("users/pitchers/"+ pitcher_Id + "/interested_investors/" + childSnapshot.key).remove();
            }
        });
    });
}

function interested(t){
    var pitcherId = document.getElementById("myModal").getElementsByClassName("pitcher_key")[0].value;
    var investorId = document.getElementById("myModal").getElementsByClassName("investor_key")[0].value;
    var pitchId = document.getElementById("myModal").getElementsByClassName("pitch_key")[0].value;
    t.value = "Interested!";
    t.setAttribute("onclick","not_interested(this)");

    chatroom_id = firebase.database().ref("users/chatrooms").push({'investor_id':investorId, 'pitcher_id':pitcherId, 'pitch_id':pitchId}).key;
    // for pitch
    firebase.database().ref("users/pitches/"+pitcherId+"/"+pitchId).child("investors").push({"investor_id":investorId});

    //for pitcher
    firebase.database().ref("users/pitchers/"+pitcherId+"/chatrooms").once("value", function(snapShot){
        current_chatrooms = snapShot.val();
        firebase.database().ref("users/pitchers/"+pitcherId).update({'chatrooms':current_chatrooms+1});

        //chatroom_id = investorId+pitcherId;
        firebase.database().ref("users/pitchers/"+pitcherId+"/chatrooms_ids").push({"key":chatroom_id, "investor_id":investorId, 'pitch_id':pitchId});
        firebase.database().ref("users/pitchers/"+pitcherId+"/interested_investors").push({"pitch_id":pitchId, "investor_id":investorId});
    });

    //for investor
    firebase.database().ref("users/investors/"+investorId+"/chatrooms").once("value", function(snapShot){
        current_chatrooms = snapShot.val();
        firebase.database().ref("users/investors/"+investorId).update({'chatrooms':current_chatrooms+1});

        //chatroom_id = investorId+pitcherId;
        firebase.database().ref("users/investors/"+ investorId+"/chatrooms_ids").push({"key":chatroom_id, "pitcher_id":pitcherId, 'pitch_id':pitchId});
        firebase.database().ref("users/investors/"+ investorId+"/interested_pitches").push({"pitch_id":pitchId, 'pitcher_id':pitcherId});
    });
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
    var starCountRef = firebase.database().ref("users/chatrooms/" + chatId + "/messages").push({"investor": msg.value});
    document.getElementById("messagearea").value = "";
}
