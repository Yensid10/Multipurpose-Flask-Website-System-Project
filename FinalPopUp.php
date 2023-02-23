<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Popup</title>
	<style>
		body {
			background-color: #e7eff6;
		}
		.popup {
			background-color: #ffffff;
			border: 1px solid #c6d8e9;
			box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
			padding: 20px;
			position: absolute;
			left: 50%;
			top: 50%;
			transform: translate(-50%, -50%);
			z-index: 999;
			max-width: 400px;
			width: 100%;
			border-radius: 4px;
			box-sizing: border-box;
		}

		button#close {
			background-color: transparent;
			border: 0;
			color: #666;
			float: right;
			font-size: 30px;
			font-weight: bold;
			line-height: 1;
			margin-top: -10px;
			margin-right: -10px;
			padding: 0;
			cursor: pointer;
			transition: color 0.2s;
		}

		button#close:hover {
			color: #333;
		}

		h3, h4 {
			margin: 10px 0;
			color: #333;
			font-weight: normal;
			font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
			text-transform: uppercase;
			letter-spacing: 1px;
		}

		input[type="checkbox"] {
			margin-right: 5px;
		}

		input[type="submit"] {
			margin-top: 20px;
			background-color: #007bff;
			color: #fff;
			border: none;
			padding: 10px 20px;
			font-size: 16px;
			font-weight: bold;
			border-radius: 4px;
			cursor: pointer;
			transition: background-color 0.2s;
		}

		input[type="submit"]:hover {
			background-color: #0069d9;
		}
	</style>
</head>
<body>
	<script>
		window.onload = function() {
			document.querySelector('.popup').style.display = 'block';
			document.querySelector('#close').onclick = function() {
				document.querySelector('.popup').style.display = 'none';
			}
		};
	</script>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$tableNumber = $_POST['table-number'];
	$allergens = isset($_POST['allergen']) ? $_POST['allergen'] : array();
	$religiousRestrictions = isset($_POST['religious-restriction']) ? $_POST['religious-restriction'] : array();

	echo "<div class='popup'>";
	echo "<h3>Your Order Details:</h3>";
	echo "Table Number: " . $tableNumber . "<br>";
	echo "Allergens: " . implode(", ", $allergens) . "<br>";
	echo "Religious Restrictions: " . implode(", ", $religiousRestrictions) . "<br>";
	echo "<button id='close'>&times;</button>";
	echo "</div>";
}
?>

<form action="" method="post">
	<div class="popup" style="display: none;">
        <h4> Table Number </h4>
		<label for="table-number-select">Select your table number:</label>
		<select id="table-number-select" name="table-number">
			<option value="">Select a Table</option>
			<?php
			for ($i = 1; $i <= 20; $i++) {
				echo "<option value=\"" . $i . "\">" . $i . "</option>";
			}
			?>
		</select>
		<h3>Please Select any Dietary Restrictions:</h3>
		<h4>Allergens:</h4>
			    <input type="checkbox" id="allergen1" name="allergen[]" value="Milk">
			    <label for="allergen1">Milk</label><br>
			    <input type="checkbox" id="allergen2" name="allergen[]" value="Eggs">
                <label for="allergen2">Eggs</label><br>
            	<input type="checkbox" id="allergen3" name="allergen[]" value="Peanuts">
            	<label for="allergen3">Peanuts</label><br>
            	<input type="checkbox" id="allergen4" name="allergen[]" value="Tree Nuts">
            	<label for="allergen4">Tree Nuts</label><br>
            	<input type="checkbox" id="allergen5" name="allergen[]" value="Wheat">
            	<label for="allergen5">Wheat</label><br>
            	<input type="checkbox" id="allergen6" name="allergen[]" value="Soy">
            	<label for="allergen6">Soy</label><br>
            	<input type="checkbox" id="allergen7" name="allergen[]" value="Fish">
            	<label for="allergen7">Fish</label><br>
            	<input type="checkbox" id="allergen8" name="allergen[]" value="Shellfish">
            	<label for="allergen8">Shellfish</label><br>
		<h4>Religious Restrictions:</h4>
			<input type="checkbox" id="religious1" name="religious-restriction[]" value="Halal">
            <label for="religious1">Halal</label><br>
            <input type="checkbox" id="religious2" name="religious-restriction[]" value="Kosher">
            <label for="religious2">Kosher</label><br>
			<input type="submit" name="submit-btn" value="Submit">
		</div>
	</form>


	<script>
		document.addEventListener("DOMContentLoaded", function() {
			document.querySelector(".popup").classList.add("active");
		});
		document.querySelector("#close").addEventListener("click", function() {
			document.querySelector(".popup").classList.remove("active");
		});
	</script>
</body>
</html>

