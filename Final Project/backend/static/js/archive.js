const todoItemsList = document.querySelector('.archive_items');


getArchiveItems()

//Function to retreive entries from flask backend (for planner items)
function getArchiveItems() {
    const url = 'http://127.0.0.1:5000/getArch'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        archivedItems = json; 
        archivedItems.sort(function(a,b){
            return new Date(a.completed) - new Date(b.completed);
        });
        console.log(archivedItems);
        displayArch(archivedItems);
    })
    
  }

//   console.log(archivedItems)

//Function to display archived items 
function displayArch(archivedItems){  
    todoItemsList.innerHTML = '';
    // console.log(items)
    for(let i = 0; i<archivedItems.length; i++){
      const li = document.createElement('li');
      
      
      li.setAttribute('class', 'item' + " " + archivedItems[i].color);
      li.setAttribute('id', archivedItems[i].id);
      li.setAttribute('data-key', archivedItems[i].id);
      
      tmp = (archivedItems[i].completed).split(" ");
      out = tmp[1] + " " + tmp[2] + " " + tmp[3] 
  
      li.innerHTML = `
      ${out} &emsp; ${archivedItems[i].class}: ${archivedItems[i].name}
      
      <button type="submit" class='delete-archive' >-</button>
      <a href="http://127.0.0.1:5000/arch&id=${archivedItems[i].id}" role="button" class='recover-archive' name="restore_button" value="planItem"><i class='fas fa-redo-alt fa-spin fa-3x'></a>`;
      todoItemsList.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }

// //Function 'deletes' item from the list (still in the database/archive)
// async function deleteArch(id) {
//     const url = 'http://127.0.0.1:5000/delete'
//     data = {value: id, type: "archItem"};
  
//     const xhr = new XMLHttpRequest();
//     sender = JSON.stringify(data)
//     xhr.open('POST', url);
//     xhr.send(sender);
    
//     await sleep(300);
  
//     window.location.reload()
// }

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function deleteDB(id){
    const url = 'http://127.0.0.1:5000/delete'
    data = {value: id, type: "archItem"};
    
    const xhr = new XMLHttpRequest();
    sender = JSON.stringify(data)
    xhr.open('POST', url);
    xhr.send(sender);
  
    await sleep(300);

    window.location.reload()
}

async function recoverItem(id){
    console.log("PENIS")
    const url = `http://127.0.0.1:5000/arch/recover&id=${id}`
    
    const xhr = new XMLHttpRequest();
    // sender = JSON.stringify(data)
    xhr.open('POST', url);
    xhr.send(null);
  
    await sleep(300);

    window.location.reload()
}

//Event listener for 'done' and 'delete' buttons
todoItemsList.addEventListener('click', function(event) {
    // check if the event is on checkbox
    // check if that is a delete-button
    if (event.target.classList.contains('delete-archive')) {
        // get id from data-key attribute's value of parent <li> where the delete-button is present
        deleteDB(event.target.parentElement.getAttribute('data-key'));
    }
    // if (event.target.classList.contains('recover-archive')) {
    //     // get id from data-key attribute's value of parent <li> where the delete-button is present
    //     recoverItem(event.target.parentElement.getAttribute('data-key'));
    // }
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