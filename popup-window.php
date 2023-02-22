<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $tableNumber = $_POST['table-number'];
    $allergens = isset($_POST['allergen']) ? $_POST['allergen'] : array();
    $religiousRestrictions = isset($_POST['religious-restriction']) ? $_POST['religious-restriction'] : array();

    echo "Table Number: " . $tableNumber . "<br>";
    echo "Allergens: " . implode(", ", $allergens) . "<br>";
    echo "Religious Restrictions: " . implode(", ", $religiousRestrictions) . "<br>";
}
?>

<body>
  <form action="" method="post">
    <div class="popup">
        <button id="close">&times;</button>
        <label for="table-number-select">Table Number:</label>
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
        <form>
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
        </form>
        <h4>Religious Restrictions:</h4>
        <form>
            <input type="checkbox" id="Kosher" name="religious-restriction[]" value="Kosher">
            <label for="Kosher">Kosher</label><br>
            <input type="checkbox" id="Halal" name="religious-restriction[]" value="Halal">
            <label for="Halal">Halal</label><br>
        </form>
        <input type="submit" value="Submit">
    </div>
  </form>
</body
