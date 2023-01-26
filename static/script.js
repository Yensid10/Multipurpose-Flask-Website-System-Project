function acceptOrder(orderId) {
    // Remove the order from the order queue table
    var orderRow = document.querySelector(`#order-queue-table tbody tr[data-order-id='${orderId}']`);
    orderRow.remove();

    // Get the order data from the order queue
    var acceptedOrder = order_queue.find(order => order.id === orderId);

    // Add the order data to the accepted orders table
    var acceptedOrdersTable = document.querySelector("#accepted-orders-table tbody");
    var newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${acceptedOrder.id}</td>
        <td>${acceptedOrder.customer_name}</td>
        <td>${acceptedOrder.items}</td>
        <td>
            <a href="${acceptedOrder.recipe_url}" class="recipe-link">View Recipe</a>
        </td>
    `;
    acceptedOrdersTable.appendChild(newRow);
}
