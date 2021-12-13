const todoListItems = document.querySelector('.gpa_items');

getGPA();

function getGPA() {
    const url = 'http://127.0.0.1:5000/getGPA'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        console.log(json)
        showClasses(json);
    })
}

//Function to display archived items 
function showClasses(graded){    
    todoListItems.innerHTML = '';
    // console.log(items)
    for(let i = 0; i<graded.length; i++){
      const li = document.createElement('li');
      
    //   console.log(graded[i])
      let letterGrade;
      numGrade = graded[i].grade;
      if (numGrade >= 90) {
        letterGrade = 'A';
      }
      else if (numGrade >= 80) {
        letterGrade = 'B';
      }
      else if (numGrade >= 70) {
        letterGrade = 'C';
      }
      else if (numGrade >= 60) {
        letterGrade = 'D';
      }
      else {
        letterGrade = 'F';
      }

      li.innerHTML = `Class: ${graded[i].class} &emsp; &emsp; &emsp; <span id="left_align">Grade: ${graded[i].grade.toFixed(2)} <i class="fas fa-long-arrow-alt-right"></i> ${letterGrade} </span>`;
      todoListItems.append(li);
      // <button type="submit" class='recover-archive'><i class='fas fa-redo-alt fa-spin fa-3x'></i>
    }
  }