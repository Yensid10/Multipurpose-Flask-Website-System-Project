document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.accept-button').forEach(button => {
        button.addEventListener('click', function () {
            const orderID = this.id.split('-')[2];
            console.log("Accepting order with ID:", orderID);
            window.location.href = '/accept_order/' + orderID;
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.complete-button').forEach(button => {
        button.addEventListener('click', function () {
            const orderID = this.id.split('-')[2];
            console.log("Completing order with ID:", orderID);
            window.location.href = '/complete_order/' + orderID;
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.order-history-button').forEach(button => {
        button.addEventListener('click', function () {
            const orderID = this.id.split('-')[2];
            console.log("Redirecting to order history:", orderID);
            window.location.href = '/order_history';
        });
    });
});