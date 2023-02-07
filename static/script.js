document.addEventListener("DOMContentLoaded", function () {
    function enableAcceptButton() {
        console.log("Running enableAcceptButton...");
        document.querySelectorAll('.accept-button').forEach(button => {
            const orderID = button.id.split('-')[2];
            const status = document.querySelector("#order-" + orderID + "-status").innerHTML;
            console.log('Order ID: ${orderID}, Status: ${status}');
            if (status === "pending") {
                button.setAttribute("disabled", true);
            } else {
                button.removeAttribute("disabled");
            }
        });
    }

    document.querySelectorAll('.accept-button').forEach(button => {
        button.addEventListener('click', function () {
            const orderID = this.id.split('-')[2];
            console.log("Accepting order with ID:", orderID);
            window.location.href = '/accept_order/' + orderID;
        });
    });

    document.querySelectorAll('.complete-button').forEach(button => {
        button.addEventListener('click', function () {
            const orderID = this.id.split('-')[2];
            console.log("Completing order with ID:", orderID);
            window.location.href = '/complete_order/' + orderID;
        });
    });

    document.querySelectorAll('.order-history-button').forEach(button => {
        button.addEventListener('click', function () {
            const orderID = this.id.split('-')[2];
            console.log("Redirecting to order history:", orderID);
            window.location.href = '/order_history';
        });
    });

    setInterval(function () {
        $.ajax({
            url: "/get_updated_orders",
            method: "GET",
            success: function (data) {
                $("#order-queue-table tbody").empty();
                $("#accepted-orders-table tbody").empty();
                $("#order-queue-table tbody").html(data.order_queue_table);
                $("#accepted-orders-table tbody").html(data.accepted_orders_table);
                enableAcceptButton();
            }
        });
    }, 5000);
});
