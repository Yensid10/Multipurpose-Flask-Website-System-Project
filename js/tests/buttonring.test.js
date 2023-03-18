// Import the code to test
import '../js/buttonring';

// Create a test suite
describe('Ring Us Button', () => {
  // Test that the button is disabled when clicked
  test('should disable button on click', () => {
    // Create a mock button
    const button = document.createElement('button');
    button.classList.add('ringus');
    document.body.appendChild(button);

    // Simulate a click on the button
    button.click();

    // Check that the button is disabled
    expect(button.disabled).toBe(true);
  });

  // Test that the button is enabled after the timer ends
  test('should enable button after timer ends', () => {
    // Create a mock button
    const button = document.createElement('button');
    button.classList.add('ringus');
    document.body.appendChild(button);

    // Simulate a click on the button
    button.click();

    // Wait for the timer to end (2 minutes)
    jest.advanceTimersByTime(2 * 60 * 1000);

    // Check that the button is enabled
    expect(button.disabled).toBe(false);
  });
});
