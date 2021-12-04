//window.localStorage.clear();
const todoForm = document.querySelector('.form');
// select the input box
const todoInput = document.querySelector('.plan-inp');
const todoDate = document.querySelector('.due-date');
// select the <ul> with class="todo-items"
const todoItemsList = document.querySelector('.items');
const priority = document.querySelector('.priority') 
const clear = document.querySelector('.button-div')

let items = [];

clear.addEventListener('click', function(event){
  if(event.target.classList.contains('sort-button-span')){
    items.sort(function(a,b){
      return new Date(a.date) - new Date(b.date);
    });
    addToLocalStorage(items);
  }
  if(event.target.classList.contains('clear-button-span')){
    items = [];
    addToLocalStorage(items);
  }
});


todoItemsList.addEventListener('click', function(event){
  if(event.target.tagName === 'LI'){
    event.target.classList.toggle('checked');
  }
}, false);

// todoForm.addEventListener('submit', function(event){
//   addItem(todoInput.value, todoDate.value);
// });

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

function addItem(item, dueDate){
  let colorValue; 
  if(priority.value === 'Exam'){
    colorValue = 'Exam';
  }
  else if(priority.value === 'Project'){
    colorValue = 'Project';
  }
  else{
    colorValue = 'HW'
  }
  if(item !== ''){
    var entry = {     //code has this as const
      id: Date.now(),
      date: dueDate,
      name: item, 
      completed: false, 
      color: colorValue
    };
  }
  items.push(entry);
  addToLocalStorage(items);

  todoInput.value = '';
  todoDate.value = '';
  priority.value = 'Homework'
}

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
    // items[i].date = new Date(items[i].date);
    // console.log((items[i].date).split(" "))
    
    //add span to separate date and name 
    // li.innerHTML = `
    // ${items[i].date} &emsp; ${items[i].class}: ${items[i].name}
    // <button class='delete-button' onclick='window.location.reload()'>-</button>`;   
    li.innerHTML = `
    ${out} &emsp; ${items[i].class}: ${items[i].name}

    <button type="submit" class='delete-button' name="delete_button" value="planItem">-</button>
    <a href="http://127.0.0.1:5000/edit&id=${items[i].id}" role="button" class='edit-button' name="edit_button" value="planItem"><i class="fas fa-edit"></i></a>`;
    
    todoItemsList.append(li);
  }
}

// function to add todos to local storage
function addToLocalStorage(items) {
  // conver the array to string then store it.
  localStorage.setItem('items', JSON.stringify(items));
  // render them to screen
  renderItems(items);
}

// function helps to get everything from local storage
function getFromLocalStorage() {
  var reference = localStorage.getItem('items');
  // if reference exists
  if (reference) {
    // converts back to array and store it in items array
    items = JSON.parse(reference);
    renderItems(items);
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
  addToLocalStorage(items);
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function deleteTodo(id) {
  // filters out the <li> with the id and updates the todos array
  // items = items.filter(function(item) {
  //   // use != not !==, because here types are different. One is number and other is string
  //   return item.id != id;
  // });
  const url = 'http://127.0.0.1:5000/delete'
  data = {value: id, type: "planItem"};

  const xhr = new XMLHttpRequest();
  sender = JSON.stringify(data)
  xhr.open('POST', url);
  xhr.send(sender);
  
  await sleep(300);

  window.location.reload()
  
  }

// getFromLocalStorage(); 

// function editItem(id){
//   const url = 'http://127.0.0.1:5000/edit'
//   data = {value: id, type: "edit"};

//   const xhr = new XMLHttpRequest();
//   sender = JSON.stringify(data)
//   xhr.open('POST', url);
//   xhr.send(sender);
// }


todoItemsList.addEventListener('click', function(event) {
  // check if the event is on checkbox

  if (event.target && event.target.nodeName === 'LI'){
    toggle1(event.target.id);  // Check if the element is a LI
  }

  // check if that is a delete-button
  if (event.target.classList.contains('delete-button')) {
    // get id from data-key attribute's value of parent <li> where the delete-button is present
    deleteTodo(event.target.parentElement.getAttribute('data-key'));
    // window.localStorage.removeItem(event.target.parentElement);
    //document.location.reload(true);
  }

  // if(event.target.classList.contains("edit-button")){
  //   window.location.reload(true);
  //   editItem(event.target.parentElement.getAttribute('data-key'));
  // }

});

let dragged;
let id;
let index;
let indexDrop;
let list;

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
    addToLocalStorage(items);
  }
});

function swapItems(first, second){
  let [tmp] = items.splice(first,1); 
  items.splice(second, 0, tmp);
  return items; 
}

getCurrentEntries();