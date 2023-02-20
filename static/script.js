$(document).ready(function() {
    // Load the order queue table
    loadOrderQueueTable();

    // Load the accepted orders table
    loadAcceptedOrdersTable();

    // Listen for accept button clicks
    $(document).on('click', '.accept-button', function() {
        // Get the table row for the clicked button
        var row = $(this).closest('tr');

        // Get the order ID from the row data
        var orderID = row.data('order-id');

        // Send a request to mark the order as accepted
        $.ajax({
            url: '/accept_order',
            type: 'POST',
            data: JSON.stringify({ 'order_id': orderID }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function() {
                // Remove the row from the order queue table
                row.remove();

                // Reload the accepted orders table
                loadAcceptedOrdersTable();
            },
            error: function() {
                alert('Error accepting order. Please try again.');
            }
        });
    });

    // Listen for complete button clicks
    $(document).on('click', '.complete-button', function() {
        // Get the table row for the clicked button
        var row = $(this).closest('tr');

        // Get the order ID from the button data attribute
        var orderID = $(this).data('order-id');

        // Send a request to mark the order as complete
        $.ajax({
            url: '/complete_order',
            type: 'POST',
            data: JSON.stringify({ 'order_id': orderID }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function() {
                // Remove the row from the accepted orders table
                row.remove();
            },
            error: function() {
                alert('Error completing order. Please try again.');
            }
        });
    });

    // Periodically refresh the order queue and accepted orders tables
    setInterval(function() {

