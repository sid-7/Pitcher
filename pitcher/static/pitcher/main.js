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

function edit_pitch(){
    div = document.getElementById("edit-pitch");
}