# SmartServe Eatery NLP Chatbot

SmartServe Eatery is a Dialogflow-based food ordering chatbot with a FastAPI webhook and MySQL backend. The bot can start an order, add or remove menu items, confirm the order, calculate the bill, and track an existing order by order id.

## Features

- Dialogflow intent flow for food ordering and order tracking
- Entity extraction for food items, quantities, and order ids
- FastAPI webhook for fulfillment logic
- MySQL database with menu, order, and tracking tables
- Stored procedure for inserting order items
- Static restaurant page with embedded chatbot
- Environment-based database configuration

## Project Structure

```text
NLP-project/
├── backend/
│   ├── main.py              # FastAPI webhook and intent routing
│   ├── db_helper.py         # MySQL access helpers
│   ├── generic_helper.py    # Shared text/session helpers
│   └── requirements.txt
├── db/
│   └── smartserve_eatery.sql
├── dialogflow_assets/
│   └── training_phrases.txt
├── frontend/
│   ├── home.html
│   ├── styles.css
│   ├── banner.jpg
│   ├── menu1.jpg
│   ├── menu2.jpg
│   └── menu3.jpg
├── .env.example
├── .gitignore
└── README.md
```

## NLP Flow

1. The user sends a natural-language message through Dialogflow.
2. Dialogflow detects the intent, such as `order.add` or `track.order`.
3. Dialogflow extracts entities like `food-item`, `number`, and `order_id`.
4. The FastAPI webhook receives the structured request.
5. The webhook updates the active order session or queries MySQL.
6. A conversational response is returned to Dialogflow.

## Main Intents

| Intent | Purpose | Example utterance |
| --- | --- | --- |
| `new.order` | Starts a new order context | "I want to order food" |
| `order.add` | Adds items and quantities | "Add two pizzas and one mango lassi" |
| `order.remove` | Removes selected items | "Remove samosa from my order" |
| `order.complete` | Saves the final order | "That will be all" |
| `track.order` | Starts order tracking | "Track my order" |
| `track.order - context: ongoing-tracking` | Reads an order id | "My order id is 41" |

## Setup

### 1. Create the database

Import the SQL dump in MySQL:

```bash
mysql -u root -p < db/smartserve_eatery.sql
```

### 2. Configure backend environment

Copy `.env.example` to `.env` and adjust values if your MySQL credentials are different.

```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=smartserve_eatery
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the webhook

```bash
uvicorn main:app --reload --port 8000
```

The webhook endpoint will be available at:

```text
http://localhost:8000/
```

For Dialogflow cloud testing, expose the local webhook using a tunneling service such as ngrok and paste the HTTPS URL into Dialogflow fulfillment settings.

## Suggested Dialogflow Entities

- `food-item`: Pav Bhaji, Chole Bhature, Pizza, Mango Lassi, Masala Dosa, Vegetable Biryani, Vada Pav, Rava Dosa, Samosa
- `number`: Dialogflow system number entity
- `order_id`: numeric order id

## Test Scenarios

| Scenario | Example | Expected result |
| --- | --- | --- |
| Add valid items | "I want two pizzas and one lassi" | Bot confirms items in active order |
| Missing quantity | "I want pizza" | Bot asks for quantity |
| Remove item | "Remove pizza" | Bot removes pizza if present |
| Complete order | "That is all" | Bot saves order and returns order id |
| Track valid id | "My id is 40" | Bot returns current order status |
| Track invalid id | "My id is 9999" | Bot says no order was found |

## Notes for Reviewers

This project focuses on applied NLP rather than training a custom model from scratch. Dialogflow handles the NLU layer, while the Python webhook manages conversational state, validation, database persistence, and response generation.
