const handleSubmit = require('./js/contact-form.js');

describe('handleSubmit', () => {
  test('it should submit the form and display a success message', () => {
    // Set up the DOM elements
    document.body.innerHTML = `
      <header></header>
      <form id="contact-form">
        <input type="text" placeholder="Your Name" value="John Doe">
        <input type="text" placeholder="Your Email" value="johndoe@example.com">
        <input type="text" placeholder="Subject" value="Test Subject">
        <textarea placeholder="Message">This is a test message.</textarea>
        <button type="submit">Send</button>
      </form>
    `;

    // Simulate form submission
    const form = document.getElementById('contact-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.click();

    // Check that email was sent
    const emailLink = `mailto:Oaxaca@yahoo.com?subject=Test Subject&body=Name%3A%20John%20Doe%0AEmail%3A%20johndoe%40example.com%0AMessage%3A%20This%20is%20a%20test%20message.`;
    expect(window.location.href).toEqual(emailLink);

    // Check that success message was displayed
    const successMsg = document.querySelector('.alert-success');
    expect(successMsg).not.toBeNull();
    expect(successMsg.textContent).toEqual('Message sent!');

    // Reset the form
    expect(form.querySelector('input[type="text"][placeholder="Your Name"]').value).toEqual('');
    expect(form.querySelector('input[type="text"][placeholder="Your Email"]').value).toEqual('');
    expect(form.querySelector('input[type="text"][placeholder="Subject"]').value).toEqual('');
    expect(form.querySelector('textarea[placeholder="Message"]').value).toEqual('');
  });
});

