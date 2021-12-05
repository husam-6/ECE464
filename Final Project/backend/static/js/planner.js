const todoForm = document.querySelector('.form');

// select the input box
const todoInput = document.querySelector('.plan-inp');
const todoDate = document.querySelector('.due-date');

// select the <ul> with class="todo-items"
const todoItemsList = document.querySelector('.items');
const priority = document.querySelector('.priority') 
const clear = document.querySelector('.button-div')

let items = [];

// todoForm.addEventListener('submit', function(event){
//   addItem(todoInput.value, todoDate.value);
// });


//Function to retreive entries from flask backend (for planner items)
function getCurrentEntries() {
  const url = 'http://127.0.0.1:5000/getEntries'
  fetch(url)
  .then(response => response.json())  
  .then(json => {
      items = json; 
      items.sort(function(a,b){
        return new Date(a.date) - new Date(b.date);
      });
      renderItems(items);
      // console.log(json);
  })
  
}

//Function to display assignment items in planner section
function renderItems(items){

  todoItemsList.innerHTML = '';
  // console.log(items)
  for(let i = 0; i<items.length; i++){
    var checked = items[i].completed ? 'checked': null;
    const li = document.createElement('li');
    
    
    li.setAttribute('class', 'item' + " " + items[i].color);
    li.setAttribute('id', items[i].id);
    li.setAttribute('data-key', items[i].id);
    li.setAttribute('draggable', true);
    if(items[i].completed === true){
      li.classList.add('checked');
    }
    
    tmp = (items[i].date).split(" ");
    out = tmp[1] + " " + tmp[2] + " " + tmp[3] 

    li.innerHTML = `
    ${out} &emsp; ${items[i].class}: ${items[i].name}

    <button type="submit" class='delete-button' name="delete_button" value="planItem">-</button>
    <a href="http://127.0.0.1:5000/edit&id=${items[i].id}" role="button" class='edit-button' name="edit_button" value="planItem"><i class="fas fa-edit"></i></a>`;
    
    todoItemsList.append(li);
  }
}


// toggle the value to completed and not completed
function toggle1(id) {
  //alert('test')
  for(let i = 0; i<items.length; i++){
    if(items[i].id == id){
      items[i].completed = !items[i].completed;
    }
  }
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

//Function 'deletes' item from the list (still in the database/archive)
async function deleteTodo(id) {
  const url = 'http://127.0.0.1:5000/delete'
  data = {value: id, type: "planItem"};

  const xhr = new XMLHttpRequest();
  sender = JSON.stringify(data)
  xhr.open('POST', url);
  xhr.send(sender);
  
  await sleep(300);

  window.location.reload()
  
  }

// Swaps items in the items array
function swapItems(first, second){
  let [tmp] = items.splice(first,1); 
  items.splice(second, 0, tmp);
  return items; 
}
  
//Event listener for 'done' and 'delete' buttons
todoItemsList.addEventListener('click', function(event) {
  // check if the event is on checkbox
  if (event.target && event.target.nodeName === 'LI'){
    toggle1(event.target.id);  // Check if the element is a LI
  }

  // check if that is a delete-button
  if (event.target.classList.contains('delete-button')) {
    // get id from data-key attribute's value of parent <li> where the delete-button is present
    deleteTodo(event.target.parentElement.getAttribute('data-key'));
  }
});

let dragged;
let id;
let index;
let indexDrop;
let list;

//Event listeners for drag and drop function
todoItemsList.addEventListener("dragstart", ({target}) => {
    dragged = target;
    id = target.id;
    list = target.parentNode.children;
    for(let i = 0; i < list.length; i += 1) {
      if(list[i] === dragged){
        index = i;
      }
    }
});

todoItemsList.addEventListener("dragover", (event) => {
  event.preventDefault();
});

todoItemsList.addEventListener("drop", ({target}) => {
  if((target.className == "item Exam" || target.className == "item Homework" || target.className == "item Project") && target.id !== id) {
    let test = [...list];
    let second = test.indexOf(target)
    dragged.remove( dragged );
    for(let i = 0; i < list.length; i++) {
      if(list[i] === target){
        indexDrop = i;
      }
    }
    if(index > indexDrop) {
      target.before( dragged );
    } else {
      target.after( dragged );
    }
    
    items = swapItems(index, second);
  
  }
});

//Event listener for sort button
clear.addEventListener('click', function(event){
  if(event.target.classList.contains('sort-button-span')){
    window.location.reload();
  }
  if(event.target.classList.contains('clear-button-span')){
    items = [];
  }
});

//Event listener for checked toggle
todoItemsList.addEventListener('click', function(event){
  if(event.target.tagName === 'LI'){
    event.target.classList.toggle('checked');
  }
}, false);

//Retrieve items from flask backend
getCurrentEntries();