/**
 *  This file contains the JavaScript code for the kitchen page.
 *  It handles the AJAX requests to the server to accept, cancel, and complete orders.
 *  It also handles the AJAX requests to the server to send and remove pings to the queue.
 */

/**
 * This function is called when the accept button is clicked.
 * It reads the order data including the order ID, order index, items, and note from the table row.
 * It then sends a POST request to the server to accept the order.
 * It then removes the order from the order queue table.
 * @name acceptOrderButton
 */
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

/**
 * This function is called when the cancel button is clicked.
 * It reads the order ID and order index from the table row.
 * It then sends a POST request to the server to cancel the order.
 * It then removes the order from the accepted orders table.
 * @name cancelOrderButton
 */
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
                    $(this).closest('tr').remove();
                }
            });

            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');

        });

/**
 * This function refreshes the order queue and accepted orders tables every 5 seconds.
 * This is done to ensure that the tables are up to date with the server.
 * This is done by reloading the tables from the server.
 * @name refreshTables
 */
setInterval(function () {
            $('#order-queue-table-content').load(location.href + ' #order-queue-table');
            $('#accepted-orders-table-content').load(location.href + ' #accepted-orders-table');
        }, 5000);


/**
 * This function is called when the complete button is clicked.
 * It reads the order ID from the table row.
 * It then sends a POST request to the server to complete the order.
 * It then removes the order from the accepted orders table.
 * @name completeOrderButton
 */
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

/**
 * This function is called when the cancel button is clicked.
 * It reads the order index from the table row.
 * It then splits the order index to get the table number and index number.
 * It then sends a POST request to the server to send a ping to the queue.
 * It then removes the order from the order queue table.
 * @param orderIndex The order index of the order to send a ping for
 */
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

/**
 * This function is called when the complete button is clicked.
 * It splits the order index to get the table number.
 * It then sends a POST request to the server to complete the order.
 * @param orderIndex The order index of the order to send a ping for
 */
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