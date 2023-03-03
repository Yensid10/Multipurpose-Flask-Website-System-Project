// button.js

// Get the button element
const ringUsBtn = document.querySelector('.ringus');

// Set the maximum number of clicks
const maxClicks = 2;

// Set a variable to keep track of the number of clicks
let clickCount = 0;

// Add a click event listener to the button
ringUsBtn.addEventListener('click', () => {
  // Increment the click count
  clickCount++;

  // If the click count is greater than or equal to the max clicks
  if (clickCount >= maxClicks) {
    // Disable the button
    ringUsBtn.disabled = true;
    // Display a message to the user
    alert('A waiter will be on the way. Thank you!');
  }
});
