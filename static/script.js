
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