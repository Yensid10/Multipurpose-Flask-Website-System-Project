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

var oqprevData;


document.addEventListener("DOMContentLoaded", function () {
    function getOrderQueueData() {
    $.getJSON("/order_queue_data", function (oqdata) {
        if (oqprevData == null) {
            oqprevData = oqdata;
        }

        else if (JSON.stringify(oqdata) !== JSON.stringify(oqprevData)) {
            console.log("Order queue data changed, reloading page...");
            oqprevData = oqdata;
            location.reload();
        }
    });
}
setInterval(getOrderQueueData, 5000);
});



var aoprevData;

document.addEventListener("DOMContentLoaded", function () {
    function getAcceptedOrdersData() {
    $.getJSON("/accepted_orders_data", function (aodata) {
        if (aoprevData == null) {
            aoprevData = aodata;
        }

        else if (JSON.stringify(aodata) !== JSON.stringify(aoprevData)) {
            console.log("Accepted orders data changed, reloading page...");
            aoprevData = aodata;
            location.reload();
        }
    });
}
setInterval(getAcceptedOrdersData, 5000);
});


