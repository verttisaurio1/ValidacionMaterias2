var selectionCounter = 0;
var ValueCounter = 0;

function cloneSelect() {
	var select = document.getElementById("plan");
	var clone = select.cloneNode(true);
	var name = select.getAttribute("name") + selectionCounter++;
	clone.id = name;
	clone.setAttribute("name", name);
	document.getElementById("selects").appendChild(clone);
  document.getElementById("count").setAttribute("value",selectionCounter)
}

function delSelect() {
	if (selectionCounter > 0) {
		selectionCounter--;
		var child = document.getElementById("plan" + selectionCounter);
		var parent = document.getElementById("selects");
		// Delete child
		parent.removeChild(child);
    document.getElementById("count").setAttribute("value",selectionCounter)
	}
}

function addValue() {
	
	var text = document.getElementById("nuevo_plan").value;
  

	if (text == "") {
		alert("Please input a Value");
		return false;
	} else {
    populateSelect('plan', text);
		for (i =  0; i<selectionCounter; i++){

      populateSelect('plan' + i, text);
    }

		return true;
	}
}

function populateSelect(target, text){
  if (!target){
      return false;
  }
  else {
      select = document.getElementById(target);
      var opt = document.createElement('option');
      opt.value = text;
      opt.innerHTML = text;
      select.appendChild(opt);
  }
}