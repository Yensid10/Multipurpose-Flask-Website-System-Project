from flask import Flask, render_template

app = Flask(__name__)

# Dummy order queue and accepted orders data
order_queue = [
    {
        "id": 1,
        "customer_name": "Customer 1",
        "items": "Spaghetti Bolognese Chicken Parmesan Lasagna",
        "status": "pending"
    },
    {
        "id": 2,
        "customer_name": "Customer 2",
        "items": "Lasagna Chicken Parmesan Pizza",
        "status": "pending"
    },
    {
        "id": 3,
        "customer_name": "Customer 3",
        "items": "Lasagna Spaghetti Bolognese Fish and Chips",
        "status": "pending"
    },
    {
        "id": 4,
        "customer_name": "Customer 4",
        "items": "Spaghetti Bolognese Pizza Fish and Chips",
        "status": "pending"
    },
    {
        "id": 5,
        "customer_name": "Customer 5",
        "items": "Pizza Fish and Chips Chicken Parmesan",
        "status": "pending"
    },
    {
        "id": 6,
        "customer_name": "Customer 6",
        "items": "Lasagna Fish and Chips Spaghetti Bolognese",
        "status": "pending"
    },
    {
        "id": 7,
        "customer_name": "Customer 7",
        "items": "Fish and Chips Chicken Parmesan Pizza",
        "status": "pending"
    },
    {
        "id": 8,
        "customer_name": "Customer 8",
        "items": "Spaghetti Bolognese Lasagna Pizza",
        "status": "pending"
    },
    {
        "id": 9,
        "customer_name": "Customer 9",
        "items": "Fish and Chips Pizza Chicken Parmesan",
        "status": "pending"
    },
    {
        "id": 10,
        "customer_name": "Customer 10",
        "items": "Lasagna Spaghetti Bolognese Chicken Parmesan",
        "status": "pending"
    }
]

accepted_orders = [
    {
        "id": 1,
        "customer_name": "Customer 1",
        "items": "Beef Stroganoff Vegetable Stir Fry",
        "recipe_url": "https://www.example.com/recipe/1"
    },
    {
        "id": 2,
        "customer_name": "Customer 2",
        "items": "Sushi Taco Salad",
        "recipe_url": "https://www.example.com/recipe/2"
    },
    {
        "id": 3,
        "customer_name": "Customer 3",
        "items": "Clam Chowder Beef Stroganoff",
        "recipe_url": "https://www.example.com/recipe/3"
    },
    {
        "id": 4,
        "customer_name": "Customer 4",
        "items": "Vegetable Stir Fry Sushi",
        "recipe_url": "https://www.example.com/recipe/4"
    },
    {
        "id": 5,
        "customer_name": "Customer 5",
        "items": "Taco Salad Clam Chowder",
        "recipe_url": "https://www.example.com/recipe/5"
    }
]


@app.route("/kitchen")
def kitchen():
    return render_template("kitchen.html", order_queue=order_queue, accepted_orders=accepted_orders)


if __name__ == "__main__":
    app.run(debug=True)
