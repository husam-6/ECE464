function swapItems(first, second){
  let [tmp] = test.splice(first,1); 
  test.splice(second,0, tmp);
  return test; 
}

let test = ['one', 'two', 'three', 'four'];
//console.log(swapItems(1,0));

let bruh = new Date();
let te = new Date();
//console.log(bruh);
// console.log(String(bruh.getDate()));

tmp = `[{"class": "Kiss me", "date": "Mon, 06 Dec 2021 00:00:00 GMT", "desc": "Right now buddy", "id": 53183642}, {"class": "OS", "date": "Thu, 16 Dec 2021 00:00:00 GMT", "desc": "word or what lol", "id": 997107744}, {"class": "Comm Theory", "date": "Tue, 14 Dec 2021 00:00:00 GMT", "desc": "            Test", "id": 1451509278}, {"class": "Comm Theory", "date": "Thu, 16 Dec 2021 00:00:00 GMT", "desc": "Test                   ", "id": 2633587872}, {"class": "OS", "date": "Thu, 16 Dec 2021 00:00:00 GMT", "desc": "word or what lol", "id": 4142372340}]`;

console.log(JSON.parse(tmp));
