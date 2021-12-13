const todoItemsList = document.querySelector('.grade_items');
const gradedItems = document.querySelector('.graded_items');

getUngraded();

function getUngraded() {
    const url = 'http://127.0.0.1:5000/gradedItems'
    const url2 = 'http://127.0.0.1:5000/getGrades'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        console.log(json)
        json.sort(function(a,b){
            return new Date(a.date) - new Date(b.date);
        });
        displayGraded(json);
    })
    fetch(url2)
    .then(response => response.json())
    .then(json => {
        console.log(json)
        json.sort(function(a,b){
            return new Date(a.date) - new Date(b.date);
        });
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
      
      tmp = (ungraded[i].completed).split(" ");
      out = tmp[1] + " " + tmp[2] + " " + tmp[3] 
  
      li.innerHTML = `
      ${out} &emsp; ${ungraded[i].class}: ${ungraded[i].name}
      <form id="GFG" method="POST" action="http://127.0.0.1:5000/insert_grade&id=${ungraded[i].id}">
        <input id="box1" type="number" step="0.01" class="weight" name="weight" placeholder="Weight" size="20" required  min="0" max="1">
        <input id="box2" type="number" step="1" class="grade" name="grade" placeholder="Grade" size="20" required  min="0" max="200">
        <a onclick="submission()" class='edit-grade'>
           <i class="fas fa-marker"></i> 
        </a>
      </form>`;
      todoItemsList.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }

//Function to display archived items 
function displayGraded(graded){  
    gradedItems.innerHTML = '';
    // console.log(items)
    for(let i = 0; i<graded.length; i++){
      const li = document.createElement('li');
      
      li.setAttribute('class', 'item' + " " + graded[i].color);
      li.setAttribute('id', graded[i].id);
      
      tmp = (graded[i].completed).split(" ");
      out = tmp[1] + " " + tmp[2] + " " + tmp[3] 
      
    //   console.log(graded[i])
      li.innerHTML = `<span id="gradeDisplay"> Grade: ${graded[i].grade}  Weight: ${graded[i].weight} </span> <br><br>
      ${out} &emsp; ${graded[i].class}: ${graded[i].name} 
        <a href="http://127.0.0.1:5000/editGrade&id=${graded[i].id}" class='edit-grade'>
            <i class="fas fa-edit"></i>
        </a>`;
      gradedItems.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }

function submission(){
    if(document.getElementById("box1").value !== null && document.getElementById("box2").value !== null){
        document.getElementById("GFG").submit();
    }
}