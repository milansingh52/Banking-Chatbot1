
# Importing libraries and module
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# User Account DB
account_database = {
    "11111234": {"name": "Milan Singh", "balance": 1000},
    "11112345": {"name": "Durga Achary", "balance": 500},
    "11113456": {"name": "Prashan Thakur", "balance": 1500},
    "11114567": {"name": "Neeru Dhungana", "balance": 200},
    "11115678": {"name": "Jayanti Ghishing", "balance": 750},
    "11116789": {"name": "Ganesh Bhandari", "balance": 3000},
    "11117890": {"name": "Indira Guragain", "balance": 120},
    "32456789": {"name": "Rekha Rai", "balance": 600},
    "87654321": {"name": "Sudha Sharma", "balance": 900},
    "98765432": {"name": "Diwas Bhandari", "balance": 1800},
}

# Transaction History DB
transaction_history_db = {
    "11111234": [
        {"date": "2023-01-01", "description": "Purchase at Store A", "amount": -500},
        {"date": "2023-01-05", "description": "Purchase at Store B", "amount": -50},
        {"date": "2023-01-06", "description": "Deposit from Employer", "amount": 1000},
    ],
    "11112345": [
        {"date": "2023-01-02", "description": "Purchase at Store B", "amount": -300},
        {"date": "2023-01-04", "description": "Deposit from Employer", "amount": 500},
    ],
    "32456789": [
        {"date": "2023-01-04", "description": "Deposit from Friend", "amount": 600},
    ],
    "87654321": [
        {"date": "2023-01-02", "description": "Purchase at Store D", "amount": -300},
        {"date": "2023-01-04", "description": "Deposit from Manager", "amount": 900},
    ],
    "98765432": [
        {"date": "2023-01-02", "description": "Purchase at Store C", "amount": -300},
        {"date": "2023-01-04", "description": "Deposit from Employer", "amount": 1800},
    ],
}

# For Inquire Balance


class ActionInquireBalance(Action):

    def name(self) -> Text:
        return "action_inquire_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # user details
        account_number = tracker.get_slot("account_number")
        user_name = tracker.get_slot("user_name")
        phone_number = tracker.get_slot("phone_number")

        # verify and show the user balance
        if account_number in account_database:
            balance = account_database[account_number]["balance"]
            name = account_database[account_number]["name"]
            dispatcher.utter_message(
                f"Dear {name}, Your account ({account_number}) has a balance of Rs. {balance}")
        else:
            dispatcher.utter_message("Sorry ! Your Account not found.")

        # show user details
        print("AC Number: ", account_number)
        print("Phone: ", phone_number)
        print("Name: ", user_name)

        return []

# For Transaction History


class ActionTransactionHistory(Action):

    def name(self) -> Text:
        return "action_transaction_history"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # fetch account number name
        account_number = tracker.get_slot("account_number")
        name = account_database[account_number]["name"]

        # verify account number and show to history
        if account_number in transaction_history_db:
            dispatcher.utter_message(
                text=f"{name}, Here are your last transaction")

            history = transaction_history_db[account_number]
            print(history)

            for idx, transaction in enumerate(history, start=1):
                date = transaction.get("date", "N/A")
                description = transaction.get("description", "N/A")
                amount = transaction.get("amount", 0)

                message = (
                    f"{idx}. Date: {date}, Description: {description}, Amount: {amount}")
                dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(
                text="Sorry, I couldn't find transaction history for your account.")

        return []


class DefaultFallback(Action):

    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        # Send the configured default fallback message
        dispatcher.utter_message(domain.templates["utter_default"])

        # Revert to the previous user action
        tracker.undo()

        # Ask the user to rephrase their request
        dispatcher.utter_message(
            "Sorry, I didn't quite understand what you meant. Could you rephrase your request?")

        # Return the current turn
        return []
