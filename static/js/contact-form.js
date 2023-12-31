/**
 * This script is used to send an email from the contact form.
 * @param {string} name - The name of the person sending the email.
 * @param {string} email - The email address of the person sending the email.
 * @param {string} subject - The subject of the email.
 * @param {string} message - The message of the email.
 * @param {string} to - The email address to send the email to.
 * @param {string} emailBody - The body of the email.
 * @param {string} emailLink - The link to send the email.
 * @param {string} messageDiv - The div to display the success message.
 * @param {string} header - The header of the page.
 * @param {string} form - The form to send the email.
 * @param {string} e - The event.
 */
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('contact-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault(); // prevent form from submitting normally

    const name = form.querySelector('input[type="text"][placeholder="Your Name"]').value;
    const email = form.querySelector('input[type="text"][placeholder="Your Email"]').value;
    const subject = form.querySelector('input[type="text"][placeholder="Subject"]').value;
    const message = form.querySelector('textarea[placeholder="Message"]').value;

    // send email
    const to = 'Oaxaca@yahoo.com'; // default email address
    const emailBody = `Name: ${name}\nEmail: ${email}\nMessage: ${message}`;
    const emailLink = `mailto:${to}?subject=${subject}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = emailLink;

    // show success message
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('alert', 'alert-success');
    messageDiv.textContent = 'Message sent!';
    const header = document.querySelector('header');
    header.insertBefore(messageDiv, header.firstChild);

    // reset form
    form.reset();
  });
});
