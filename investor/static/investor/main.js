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

function pitch_click(t) {
    var modal = document.getElementById("myModal");
    var btn = t;
    var span = document.getElementsByClassName("close")[0];
    var all = t.getElementsByTagName('div');
    //console.log(all)
    document.getElementById('title').innerHTML = all[0].innerHTML;
    document.getElementById('status').innerHTML = all[1].innerHTML;
    document.getElementById('date').innerHTML = all[2].innerHTML;
    document.getElementById('gist').innerHTML = all[3].innerHTML;
    document.getElementById('tags').innerHTML = all[4].innerHTML;
    document.getElementById('whole').innerHTML = all[5].innerHTML;
    document.getElementById('contributors').innerHTML = all[6].innerHTML;
    document.getElementById('investors').innerHTML = all[7].innerHTML;
    document.getElementById('video').getElementsByTagName('source')[0].setAttribute("src", all[7].innerHTML);

    var k = document.getElementById('myModal').getElementsByClassName('pitch_key');
    var pitch_key = t.getElementsByTagName("input")[0].value;
    var pitcher_key = t.getElementsByTagName("input")[1].value;

    k[0].setAttribute('value', pitch_key);
    document.getElementById('myModal').getElementsByClassName('pitcher_key')[0].setAttribute('value', pitcher_key)

    var interested = t.getElementsByTagName("input")[2].value;
    console.log(interested);
    if(interested=="True"){
        document.getElementById("interested_button").value = "Interested!";
        document.getElementById("interested_button").setAttribute("onclick","not_interested(this)");
    }
    else{
        document.getElementById("interested_button").value = "Show Interest?";
        document.getElementById("interested_button").setAttribute("onclick", "interested(this)");
    }

    btn.onclick = function () {modal.style.display = "block";}
    span.onclick = function () {modal.style.display = "none";}
    window.onclick = function (event) {
        if (event.target == modal) {modal.style.display = "none";}
    }
}

function not_interested(t){
    t.value = "Show Interest?"
    t.setAttribute("onclick", "interested(this)");
}

function interested(t){
    var pitcherId = document.getElementById("myModal").getElementsByClassName("pitcher_key")[0].value;
    var investorId = document.getElementById("myModal").getElementsByClassName("investor_key")[0].value;
    var pitchId = document.getElementById("myModal").getElementsByClassName("pitch_key")[0].value;
    console.log("Investor: ");
    console.log(pitcherId, investorId, pitchId);
    t.value = "Interested!";
    t.setAttribute("onclick","not_interested(this)");

    chatroom_id = firebase.database().ref("users/chatrooms").push({'investor_id':investorId, 'pitcher_id':pitchId}).key;
    // for pitch
    firebase.database().ref("users/pitches/"+pitcherId+"/"+pitchId).child("investors").push({"investor_id":investorId});

    //for pitcher
    firebase.database().ref("users/pitchers/"+pitcherId+"/chatrooms").once("value", function(snapShot){
        current_chatrooms = snapShot.val();
        firebase.database().ref("users/pitchers/"+pitcherId).update({'chatrooms':current_chatrooms+1});

        //chatroom_id = investorId+pitcherId;
        firebase.database().ref("users/pitchers/"+pitcherId+"/chatrooms_ids").push({"key":chatroom_id, "investor_id":investorId});
        firebase.database().ref("users/pitches/"+pitcherId+"/interested_investors").push({"investor_id":investorId});
    });

    //for investor
    firebase.database().ref("users/investors/"+investorId+"/chatrooms").once("value", function(snapShot){
        current_chatrooms = snapShot.val();
        firebase.database().ref("users/investors/"+investorId).update({'chatrooms':current_chatrooms+1});

        //chatroom_id = investorId+pitcherId;
        firebase.database().ref("users/investors/"+ investorId+"/chatrooms_ids").push({"key":chatroom_id, "pitcher_id":pitcherId});
        firebase.database().ref("users/investors/"+ investorId+"/interested_pitches").push({"pitch_id":pitchId});
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
}
function addMessage(key, message) {
    var newDiv = document.createElement('div');
    newDiv.innerHTML = message;
    newDiv.className = 'demo';
    toAdd.appendChild(newDiv);
    element.appendChild(toAdd);
}

function sendMessage() {
    var msg = document.getElementById("messagearea");
    var starCountRef = firebase.database().ref("users/chatrooms/" + chatId + "/messages").push({"investor": msg.value});
}