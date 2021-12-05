const todoItemsList = document.querySelector('.grade_items');

getUngraded();

function getUngraded() {
    const url = 'http://127.0.0.1:5000/getUngraded'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        json.sort(function(a,b){
            return new Date(a.date) - new Date(b.date);
        });
        console.log(json);
        displayUngraded(json);
    })
    
}

//Function to display archived items 
function displayUngraded(ungraded){  
    todoItemsList.innerHTML = '';
    // console.log(items)
    for(let i = 0; i<ungraded.length; i++){
      const li = document.createElement('li');
      
      
      li.setAttribute('class', 'item' + " " + ungraded[i].color);
      li.setAttribute('id', ungraded[i].id);
      li.setAttribute('data-key', ungraded[i].id);
      li.setAttribute('draggable', true);
      if(ungraded[i].completed === true){
        li.classList.add('checked');
      }
      
      tmp = (ungraded[i].completed).split(" ");
      out = tmp[1] + " " + tmp[2] + " " + tmp[3] 
  
      li.innerHTML = `
      ${out} &emsp; ${ungraded[i].class}: ${ungraded[i].name}
      
      <button type="submit" class='delete-archive' >-</button>
      <a href="http://127.0.0.1:5000/arch&id=${ungraded[i].id}" role="button" class='recover-archive' name="restore_button" value="planItem"><i class='fas fa-redo-alt fa-spin fa-3x'></a>`;
      todoItemsList.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }
