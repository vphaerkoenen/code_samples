function patchIt(){
  axios({
  method: 'patch',
  url: '/students',
  data:{
        "student_number": document.getElementById("studentNumber").value,
        "name":document.getElementById("studentName").value,
        "credits":document.getElementById("credits").value,
        "degree" : document.getElementById("degreeProgramme").value

      }
    }); 
    document.getElementById("studentNumber").value ="";
    document.getElementById("studentName").value = "";
    document.getElementById("credits").value = "";
    document.getElementById("degreeProgramme").value = "";
    alert("Student added");
  }
addButton.addEventListener("click", patchIt);

