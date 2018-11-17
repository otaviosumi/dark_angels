function newLocation(checkbox){
    if(checkbox.checked == true){
        document.getElementById("selectBox").style.display = "none";
		  document.getElementById("div_new_location").style.display = "block";
    } else {
        document.getElementById("selectBox").style.display = "block";
        document.getElementById("div_new_location").style.display = "none";
    }
}
