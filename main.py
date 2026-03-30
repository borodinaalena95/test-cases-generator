from jira_client import get_ticket
from llm import generate_test_cases

if __name__ == "__main__":
    ticket_id = input("Enter Jira ticket ID: ")
    ticket = get_ticket(ticket_id)
    test_cases = generate_test_cases(ticket)
    print(test_cases)





