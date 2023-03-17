
/**
 * Javascript function for Pop-Up used in menu home screen
 * 
 *
 * @author - Ethan Chandler
 */

var tableNumber = null;

/**
*
* This function submits the form with the selected table number and allergens via an AJAX request to the server to hide items containing dairy.
*
* It then hides the selected items on the page and hides the popup.
*/
function submitPopup() {
	var selectElement = document.getElementById('table-number-select');
	tableNumber = selectElement.options[selectElement.selectedIndex].value;

    var allergenInputs = document.getElementsByName('allergen');
	var allergens = [];
	for (var i = 0; i < allergenInputs.length; i++) {
		if (allergenInputs[i].checked) {
			allergens.push(allergenInputs[i].value);
		}
	}
	console.log(tableNumber);
	console.log('tableNumber:', tableNumber + ' allergens:', allergens);

	if (tableNumber !== null && tableNumber !== '') {
		if (!isNaN(tableNumber) && tableNumber >= 0) {
			$.ajax({
				type: "POST",
				url: "/hideDairy",
				data: JSON.stringify({
					"tableNumber": tableNumber,
					"allergens": allergens
				}),
				contentType: "application/json",
				dataType: 'json'
			}).done(function (response) {
				console.log('this is my response:', response);
				var data = response.data;
				console.log(tableNumber);
				hide(data);
				document.querySelector(".popup").style.display = "none";
				document.querySelector("body").style.overflow = "auto";
			});
		}
	}
}

/**
*
* This function hides the selected items on the page by setting their display style to "none".
* @param {Array} data - An array of item IDs to be hidden.
*/

function hide(data) {
	if (data != null) {
		for (var i = 0; i < data.length; i++) {
			console.log(data[i]);
			var x1 = document.getElementById(data[i]);
			console.log('x is now changed to:', data[i]);
			if (x1 != null) {
				if (x1.style.display === "none") {
					x1.style.display = "block";
				} else {
					x1.style.display = "none";
				}
			}
		}
	}

}
