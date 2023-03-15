document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    form.addEventListener('submit', function(e) {
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
  