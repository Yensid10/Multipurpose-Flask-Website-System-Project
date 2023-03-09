// Get the button element
const ringUsBtn = document.querySelector('.ringus');

// Set a variable to keep track of the timer
let timer;

// Add a click event listener to the button
ringUsBtn.addEventListener('click', () => {
  if (tableNumber != null) {
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
    const storedTime = localStorage.getItem('ringUsTime');
    const storedDuration = localStorage.getItem('ringUsDuration');
    let timeLeft;
    if (storedTime && storedDuration) {
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
    const minutes = Math.floor(timeLeft / 60000);
    let seconds = Math.floor((timeLeft % 60000) / 1000);
    background.innerText = `Please wait ${minutes}:${seconds < 10 ? '0' : ''}${seconds} minutes. The waiter will be with you shortly.`;
    timer = setInterval(() => {
      timeLeft -= 1000;
      if (timeLeft > 0) {
        const minutes = Math.floor(timeLeft / 60000);
        seconds = Math.floor((timeLeft % 60000) / 1000);
        background.innerText = `Please wait ${minutes}:${seconds < 10 ? '0' : ''}${seconds} minutes. The waiter will be with you shortly.`;
        localStorage.setItem('ringUsTime', clickTime);
        localStorage.setItem('ringUsDuration', timeLeft);
      } else {
        // Enable the button
        ringUsBtn.disabled = false;
        // Remove the background
        document.body.removeChild(background);
        // Stop the timer
        clearInterval(timer);
        localStorage.removeItem('ringUsTime');
        localStorage.removeItem('ringUsDuration');
      }
    }, 1000); // 1 second interval
    localStorage.setItem('ringUsTime', clickTime);
    localStorage.setItem('ringUsDuration', timeLeft);
  }
});

if (tableNumber != null) {
  const storedTime = localStorage.getItem('ringUsTime');
  const storedDuration = localStorage.getItem('ringUsDuration');
  let timeLeft;
  if (storedTime && storedDuration) {
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
