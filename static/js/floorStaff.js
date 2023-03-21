
// CLIENT CLASSES \\
/**
 * @class orderNotes
 * @classdesc This class is used to store the order notes and price of an order.
 * @param {string} Note1 - The first note of the order
 * @param {string} Note2 - The second note of the order
 * @param {number} price - The price of the order
 * @returns {Note1} - The first note of the order
 * @returns {Note2} - The second note of the order
 * @returns {price} - The price of the order
 */
class orderNotes {
    constructor(Note1, Note2, price) {
        this.Note1 = Note1;
        this.Note2 = Note2;
        this.price = price;
    }

    // Getters
    getNote1() {
        return this.Note1;
    }

    getNote2() {
        return this.Note2;
    }

    getPrice() {
        return this.price;
    }
}
/**
 * @class orderQueue
 * @classdesc This is a class used to manage order notes and price in the order queue.
 */
class orderQueue {
    /**
     * @constructor - Creates a new order queue.
     */
    constructor() {
        this.queue = [];
    }
    /**
       * Adds a new orderNotes object to the queue array.
       * @param {string} Note1 - The first note for the order
       * @param {string} Note2 - The second note for the order
       * @param {number} price - The price for the order
       */
    addObject(Note1, Note2, price) {
        // Add a new orderNotes object to the queue array
        this.queue.push(new orderNotes(Note1, Note2, price));
    }
    /**
       * Removes an object from the queue array at the specified index.
       * @param {number} index - The index of the object to remove
       */
    removeObject(index) {
        // Remove an object from the queue array at the specified index
        this.queue.splice(index, 1);
    }
    /**
       * Gets the object at the specified index of the queue array.
       * @param {number} index - The index of the object to get
       * @returns {orderNotes} - The orderNotes object at the specified index
       */
    getObject(index) {
        // Get the object at the specified index of the queue array
        return this.queue[index];
    }
    /**
       * Gets the length of the queue array.
       * @returns {number} - The length of the queue array
       */
    getLength() {
        // Get the length of the queue array
        return this.queue.length;
    }
}

// QUEUE FUNCTIONS \\
function acceptQueuePing() {
    // If the info-container div contains "Complete!" or "htmlCheck", change info-container to be the top popped ping from the python ping queue
    if (($("#info-container").html().includes("Complete!")) || ($("#info-container").html().includes("htmlCheck"))) {
        $.ajax({
            type: "POST",
            url: "/acceptQueuePing",
            success: function (data) {
                $("#info-container").html(data.acceptedPing);
            }
        })
        updateQueue();
    }
}

function completeCurrentJob() {
    // If the info-container div doesn't contain "htmlCheck" or "Complete!", add "Complete!" and a flash animation to the div
    if ((!$("#info-container").html().includes("htmlCheck"))
        && (!$("#info-container").html().includes("Complete!"))) {
        $("#info-container").html("<span id='fade-out-text' class='fade-out-text'>Complete!</span>");
        setTimeout(function () { $("#fade-out-text").css("opacity", "0"); }, 50);
    }
}

function updateQueue() {
    // Send a GET request to the server to get the ping queue data and update the page accordingly
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/updateQueue", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Parse the response from the server
            var data = JSON.parse(xhr.responseText);
            // Update the queue count on the page
            document.querySelector("h2").innerHTML = "QUEUE: " + data.queueLength;
            // Clear the existing queue
            var menu = document.querySelector(".scroll-menu");
            menu.innerHTML = "";

            // Adding the first new queue objects to the page with button
            var item = document.createElement("div");
            item.classList.add("menu-item");
            item.innerHTML = '<button type="button" class="button" onclick="acceptQueuePing()">Accept</button>'
                + data.queueItems[0].note + " " + data.queueItems[0].tableNo;
            menu.appendChild(item);

            // Adding the rest of the new queue objects to the page
            for (var i = 1; i < data.queueItems.length; i++) {
                item = document.createElement("div");
                item.classList.add("menu-item");
                item.innerHTML = data.queueItems[i].note + " " + data.queueItems[i].tableNo;
                menu.appendChild(item);
            }
        }
    };
    xhr.send();
}


// ORDER FUNCTIONS \\
/**
 * Creates a flashing animation effect on an HTML element by adding/removing "flash" class.
 * The "flash" animation causes the element to briefly flash red and then fade away.
 * @param {HTMLElement} element - The HTML element on which to apply the "flash" effect
*/
function flashElement(element) {
    // Creates an animation effect called "flash" on an element which will flash red and then fade away
    if (element.classList.contains("flash")) {
        element.classList.remove("flash");
        void element.offsetWidth;
        element.classList.add("flash");
    } else {
        element.classList.add("flash");
    }
}
/**
 * Updates the order review list on the webpage and displays the total price of the order.
 * @description If the order is not empty, this function generates HTML markup for each order item with a remove button.
 * Calculates and displays the total price of the order. Otherwise, the order list is cleared.
*/
function updateOrder() {
    // Updates the order review list on the webpage and displays the total price of the order
    var orderHtml = "";
    priceTotal = 0;
    if (order.getLength() > 0) {
        for (var i = 0; i < order.getLength(); i++) {
            orderHtml += "<div><strong>" + order.getObject(i).getNote1() + "</strong><br>"
                + order.getObject(i).getNote2()
                + "<button class=\"remove-button\" onclick=\"removeOrderItem(" + i + ")\"><img src=\"/static/images/trashcan.png\" alt=\"Remove\"></button></div><br>";
            priceTotal += parseFloat(order.getObject(i).getPrice());
        }
        $("#order-item").html(orderHtml + "<strong style='text-decoration: underline; '>Total: £" + priceTotal + "</strong><br><br>");
    } else {
        $("#order-item").html("");
    }
}

/**
 * Adds an item to the order list and updates the display.
 * @param {string} orderItem - The name of the item to add to the order
 * @param {number} price - The price of the item to add to the order
*/
function addItemToOrder(orderItem, price) {
    // Adds an item to the order list and updates the display
    document.getElementById("review").classList.remove("flash");
    order.addObject(orderItem, document.getElementById(orderItem).value, price);
    document.getElementById(orderItem).value = "";
    updateOrder();
}
/**
 * Removes an item from the order list and updates the display..
 * @param {number} index - The index of the item to remove from the order
*/
function removeOrderItem(index) {
    // Removes an item from the order list and updates the display
    order.removeObject(index);
    updateOrder();
}
/**
 * Sends the order to the kitchen via an AJAX call and updates the display accordingly
 * Checks if the selected table has a "htmlCheck" value and flashes the element if it does.
 * Checks if the order is empty and flashes the review element if it is.
 * If the order is not empty and does not have a "htmlCheck" value, sends the order to the kitchen via AJAX.
 * Clears the order queue and updates the display after sending the order.
 * Displays a confirmation message to the user and fades it out after a delay.
 * @throws {Error} If there is an issue sending the order to the kitchen
*/
function sendToKitchen() {
    // Sends the order to the kitchen via an AJAX call and updates the display accordingly
    var selectElement = document.getElementById("orderSelect");
    if (selectElement.options[selectElement.selectedIndex].value.includes("htmlCheck")) {
        flashElement(selectElement)
    }
    if (order.getLength() == 0) {
        flashElement(document.getElementById("review"));
    }
    if (!selectElement.options[selectElement.selectedIndex].value.includes("htmlCheck") && order.getLength() != 0) {
        $.ajax({
            type: "POST",
            url: "/sendToKitchen",
            data: JSON.stringify({ "order": order, "tableNo": selectElement.options[selectElement.selectedIndex].value }),
            contentType: "application/json",
        });
        order = new orderQueue();
        updateOrder();
        $("#order-item").html("<span id='fade-out-text' style='text-align: center; font-size: 25px; font-weight: bold;"
            + "color: red; text-decoration: underline;' class='fade-out-text'>Sent to Kitchen!</span>");
        setTimeout(function () { $("#fade-out-text").css("opacity", "0"); }, 50);
        selectElement.selectedIndex = 0;
    }
}

// BILLS FUNCTIONS \  
/**
 * Retrieves the bill for a particular table and redirects the user to that specific table's bill page.
 * If the selected table has a "htmlCheck" value, flashes the element.
*/
function getBill() {
    // Retrieves the bill for a particular table and redirects the user to that specific tables bill page
    var selectElement = document.getElementById("billSelect");
    if (!selectElement.options[selectElement.selectedIndex].value.includes("htmlCheck")) {
        var form = document.createElement('form');
        form.action = '/getBill'; // Set the form action URL
        form.method = 'POST'; // Set the form submission method
        var input = document.createElement('input');
        input.name = 'tableNo';
        input.value = selectElement.options[selectElement.selectedIndex].value;
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    } else {
        flashElement(selectElement);
    }
}


// MAIN JAVASCRIPT CODE \\
order = new orderQueue();
updateQueue();
setInterval(updateQueue, 1000); 
