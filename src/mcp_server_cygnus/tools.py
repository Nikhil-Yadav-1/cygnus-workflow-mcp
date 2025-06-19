import requests
import time
import traceback
import random

def generate_random_session_id():
    return ''.join(random.choices('123456789abcdefghijklmnopqrstuvwxyz', k=5))
    
def my_account_chat_tool(query: str = "how can you help me?") -> str:
    """
    Tool to interact with the Kindlife.in customer support chatbot.

    Args:
        query (str): The user's question or request about Kindlife.in services.
            Examples:
            - "Tell me about your clean beauty products"
            - "How do I track my order?"
            - "What are the current promotions?"
            - "Tell me about the Superkind Club"
            - "How can I join the Kind Champion Program?"

    Returns:
        str: The chatbot's response text, or an error message if the request fails.
        The response will provide helpful information about Kindlife.in's products,
        services, and support options.

    Description:
        This function sends a POST request to the Kindlife.in customer support chatbot
        API endpoint. It handles queries about:
        1. Product Information (clean beauty, healthy snacks, wellness essentials)
        2. Order Support (tracking, order details, issue resolution)
        3. Promotions and Discounts (sales, discounts, Kinders loyalty program)
        4. Membership Programs (Superkind Club, Kind Champion Program)
        5. Community and Resources (community engagement, clean beauty and wellness resources)
    """
    url = "https://portal.demo.cygnusalpha.one/api/v1/api-controller/invoke-service/my-account-chat/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer kl-my-acc-c398e977-a645-4429-8543-16290ce51d4a",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8evtbe"
    }
    body = {
        "mobile": "919816640889",
        "text": query,
        "session_id": generate_random_session_id(),
        "client_identifier": "919816640889",
        # "client_identifier": "Q1lHTlVTX0FJX0FQSV9VU0VSQGtpbmRsaWZlLmluOnczcXU4QjRKZVZlODgzdlNzNzA4dDk0VzA0czk4U2cw"
    }

    try:
        response = requests.post(url, headers=headers, data=body, timeout=15)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.text
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
        return str(e)

if __name__ == "__main__":
    print(generate_random_session_id())
