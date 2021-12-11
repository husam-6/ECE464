const notifsList = document.querySelector('.notif_items');
const snoozeList = document.querySelector('.snooze_items');


getArchiveItems()

// import dispNotif from 'test.js'
// import displaySnooze from 'test.js'

//Function to retreive entries from flask backend
function getArchiveItems() {
    const url = 'http://127.0.0.1:5000/getNotifs'
    const url2 = 'http://127.0.0.1:5000/getNotifs/snooze'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        notifs = json;
        notifs.sort(function(a,b){
            return new Date(a.date) - new Date(b.date);
        }); 
        console.log(notifs);
        dispNotif(notifs);
    })
    fetch(url2)
    .then(response => response.json())
    .then(json => {
        snoozes = json;
        snoozes.sort(function(a,b){
            return new Date(a.date) - new Date(b.date);
        }); 
        console.log(snoozes);
        displaySnooze(snoozes);
    })
    
  }

//   console.log(notifs)

// Function to display archived items 
function dispNotif(notifs){  
    notifsList.innerHTML = '';
    // console.log(items)
    for(let i = 0; i<notifs.length; i++){
      const li = document.createElement('li');
      
      
      li.setAttribute('class', 'item' + " " + notifs[i].color);
      li.setAttribute('id', notifs[i].id);
      li.setAttribute('data-key', notifs[i].id);
      
      tmp = (notifs[i].date).split(" ");
      out = tmp[1] + " " + tmp[2] + " " + tmp[3] 
  
      li.innerHTML = `
      ${out} &emsp; ${notifs[i].class}: ${notifs[i].name}
      
      <button type="submit" class='delete-notifs' >-</button>`;
      notifsList.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }

function displaySnooze(snooze){  
    snoozeList.innerHTML = '';
    // console.log(items)
    for(let i = 0; i<snooze.length; i++){
      const li = document.createElement('li');
      
      li.setAttribute('class', 'item');
      li.setAttribute('id', snooze[i].id);
      li.setAttribute('data-key', snooze[i].id);
      
      tmp = (snooze[i].date).split(" ");
      out = tmp[1] + " " + tmp[2] + " " + tmp[3] 
  
      li.innerHTML = `
      ${out} &emsp; ${snooze[i].class}: ${snooze[i].desc}
      
      <button type="submit" class='delete-snooze' >-</button>`;
      snoozeList.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }



function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function deleteNotif(id,tmp){
    const url = 'http://127.0.0.1:5000/delete'
    data = {value: id, type: tmp};
    
    const xhr = new XMLHttpRequest();
    sender = JSON.stringify(data)
    xhr.open('POST', url);
    xhr.send(sender);
  
    await sleep(300);

    window.location.reload()
}

//Event listener for 'done' and 'delete' buttons
notifsList.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-notifs')) {
      // get id from data-key attribute's value of parent <li> where the delete-button is present
      deleteNotif(event.target.parentElement.getAttribute('data-key'), "notif");
    }
});

snoozeList.addEventListener('click', function(event) {

  if (event.target.classList.contains('delete-snooze')) {
    // console.log("DELETE")
    // get id from data-key attribute's value of parent <li> where the delete-button is present
    deleteNotif(event.target.parentElement.getAttribute('data-key'), "snooze");
  }
});

//Get the button:
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}