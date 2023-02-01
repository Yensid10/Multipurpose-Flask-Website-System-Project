document.addEventListener("DOMContentLoaded", function() {
document.querySelectorAll('.accept-button').forEach(button => {
button.addEventListener('click', function () {
const orderID = this.id.split('-')[2];
console.log("Accepting order with ID:", orderID);
window.location.href = '/accept_order/' + orderID;
});
});
});