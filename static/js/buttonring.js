/**
 * This file is used to handle the ring us button.
 * When the button is clicked, it will be disabled for 2 minutes.
 * The button will be enabled again after 2 minutes.
 * The button will also be disabled if the user refreshes the page.
 * The button will be enabled again if the user refreshes the page after 2 minutes.
 */
// Get the button element
const ringUsBtn = document.querySelector('.ringus');

// Set a variable to keep track of the timer
let timer;

// Set a variable to keep track of the time left
let timeLeft = 0;

// Add a click event listener to the button
ringUsBtn.addEventListener('click', () => {
  if (tableNumber != null && timeLeft === 0) {
    // Disable the button
    ringUsBtn.disabled = true;
    // Create a transparent background
    const background = document.createElement('div');
    background.style.position = 'absolute';
    background.style.top = '0';
    background.style.left = '0';
    background.style.width = '100%';
    background.style.height = '100%';
    background.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    background.style.color = '#fff';
    background.style.display = 'flex';
    background.style.justifyContent = 'center';
    background.style.alignItems = 'center';
    document.body.appendChild(background);
    // Start the timer
    const clickTime = Date.now();
    if (timeLeft === 0) {
      timeLeft = 120000; // 2 minutes in milliseconds
      $.ajax({
        type: "POST",
        url: "/addPingToQueue",
        data: JSON.stringify({ "pingType": "Table", "tableNo": "#" + tableNumber }),
        contentType: "application/json",
      });
    }
    const minutes = Math.floor(timeLeft / 60000);
    let seconds = Math.floor((timeLeft % 60000) / 1000);
    background.innerText = `Please wait ${minutes}:${seconds < 10 ? '0' : ''}${seconds} minutes. The waiter will be with you shortly.`;
    timer = setInterval(() => {
      timeLeft -= 1000;
      if (timeLeft > 0) {
        const minutes = Math.floor(timeLeft / 60000);
        seconds = Math.floor((timeLeft % 60000) / 1000);
        background.innerText = `Please wait ${minutes}:${seconds < 10 ? '0' : ''}${seconds} minutes. The waiter will be with you shortly.`;
      } else {
        // Enable the button
        ringUsBtn.disabled = false;
        // Remove the background
        document.body.removeChild(background);
        // Stop the timer
        clearInterval(timer);
        timeLeft = 0;
      }
    }, 1000); // 1 second interval
  }
});
/**
 * This function is used to disable the button when the user refreshes the page.
 * @param {number} timeLeft - The time left in milliseconds.
 * @param {number} clickTime - The time when the button was clicked.
 * @param {number} storedDuration - The duration of the timer in milliseconds.
 * @param {number} storedTime - The time when the timer was started.
 * @param {number} elapsedTime - The time elapsed since the timer was started.
 * @param {number} minutes - The minutes left.
 * @param {number} seconds - The seconds left.
 * @param {number} duration - The duration of the timer in milliseconds.
 * @param {number} time - The time when the timer was started. 

 */
if (tableNumber != null && timeLeft === 0) {
  const storedTime = localStorage.getItem('ringUsTime');
  const storedDuration = localStorage.getItem('ringUsDuration');
  if (storedTime && storedDuration) {
    const clickTime = Date.now();
    const elapsedTime = clickTime - storedTime;
    timeLeft = Math.max(0, storedDuration - elapsedTime);
  } else {
    timeLeft = 120000; // 2 minutes in milliseconds
    $.ajax({
      type: "POST",
      url: "/addPingToQueue",
      data: JSON.stringify({ "pingType": "Table", "tableNo": "#" + tableNumber }),
      contentType: "application/json",
    });
  }
}
