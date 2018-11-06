 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, options);
  });
  
function changeFunc() {
	var selectBox = document.getElementById("selectBox");
   var selectedValue = selectBox.options[selectBox.selectedIndex].value;
   if (selectedValue == "SEC") {
   	document.getElementById("man_group").style.display = "none";
   	document.getElementById("train").style.display = "block";
   } else if (selectedValue == "MAN"){
   	document.getElementById("train").style.display = "none";
   	document.getElementById("man_group").style.display = "block";
   } else {
   	document.getElementById("train").style.display = "none";
		document.getElementById("man_group").style.display = "none";
   }
}

function handleChangeEletric(checkbox) {
        document.getElementById("man_ele_nr").style.display = "block";
    if(checkbox.checked == true){
    }else{
        document.getElementById("man_ele_nr").style.display = "none";
   }
}

function handleChangeMecanic(checkbox) {
    if(checkbox.checked == true){
        document.getElementById("man_mec_nr").style.display = "block";
    }else{
        document.getElementById("man_mec_nr").style.display = "none";
   }
}

function handleChangeTI(checkbox) {
    if(checkbox.checked == true){
        document.getElementById("man_ti_nr").style.display = "block";
    }else{
        document.getElementById("man_ti_nr").style.display = "none";
   }
}