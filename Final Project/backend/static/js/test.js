//Function to display archived items 
export function dispNotif(notifs){  
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

export function displaySnooze(snooze){  
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