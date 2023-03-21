$(document).on('click', '.accept-button', function () {
        // Get the order ID and data
        const orderID = $(this).data('order-id');
        const orderData = $(this).closest('tr').find('td').map(function () {
            return $(this).text();
        }).get();

        $('#order-queue-table-content').load(location.href + ' #order-queue-table');
        $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

        // Send the order data to the server to be accepted
        $.ajax({
            url: '/accept_order',
            type: 'POST',
            data: {
                'order_data': JSON.stringify({
                    'old_id': orderID,
                    'order_index': orderData[0],
                    'items': orderData[1],
                    'note': orderData[2]
                }),
                'time': Date.now()
            },
            success: function (data) {
                // If the order was accepted, remove it from the order queue table
                $(this).closest('tr').remove();
            }
        });

        $('#order-queue-table-content').load(location.href + ' #order-queue-table');
        $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');
    });

$(document).on('click', '.cancel-button', function () {
            // Get the order ID and order index from the table row
            const orderID = $(this).data('order-id');
            const orderIndex = $(this).closest('tr').find('td:first-child').text();

            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

            // Send a POST request to cancel the item
            $.ajax({
                url: '/cancel_order',
                type: 'POST',
                data: {'order_id': orderID, 'order_index': orderIndex},
                success: function (data) {
                    // If the item was cancelled, remove it from the bill table
                    $(this).closest('tr').remove();
                }
            });

            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

        });

setInterval(function () {
            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');
        }, 5000);

$(document).on('click', '.complete-button', function () {
            // Get the order ID
            const orderID = $(this).data('order-id');

            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

            // Send the order ID to the server to be completed
            $.ajax({
                url: '/complete_order',
                type: 'POST',
                data: {'order_id': orderID},
                success: function (data) {
                    // If the order was completed, remove it from the accepted orders table
                    $(this).closest('tr').remove();
                }
            });

            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

        });

function sendCancel(orderIndex) {
            // Split the orderIndex to get the table number
            const orderIndexParts = orderIndex.split('-');
            const tableNumber = orderIndexParts[0];
            const indexNumber = orderIndexParts[1];
            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

            $.ajax({
                type: "POST",
                url: "/sendCancel",
                data: JSON.stringify({"pingType": "Food", "tableNo": "#" + tableNumber, "indexNo": indexNumber}),
                contentType: "application/json",
            });
        }

function addPingToQueue(orderIndex) {

            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');
            const tableNumber = orderIndex.split('-')[0];

            $.ajax({
                type: "POST",
                url: "/addPingToQueue",
                data: JSON.stringify({"pingType": "Food", "tableNo": "#" + tableNumber}),
                contentType: "application/json",
            });
        }