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