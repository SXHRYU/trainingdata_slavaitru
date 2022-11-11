import requests
import pandas as pd


USERNAME = "" # here were credentials, removed for github
PASSWORD = ""

HOSTNAME = "" # here was a hostname, removed for github
USERS_LIST_URL = 'http://' + HOSTNAME + "users"

def get_session() -> requests.Session:
    """Returns session instance with authorized credentials."""
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    
    return session

def get_page_size(session: requests.Session,
                  users_list_url: str) -> int:
    """Returns the number of all users.
    
    Desired param in `get_users` API query.
    """
    response = session.get(users_list_url)
    page_size = response.json()["count"]

    return page_size

def get_token(session: requests.Session, 
              hostname: str,
              username: str,
              password: str) -> str:
    """Returns authorization token of current user."""

    url = "https://" + hostname + "/auth/login"
    response = session.post(
        url,
        json={
            "username": username,
            "password": password,
        }
    )
    token = response.json()['key']
    
    return token

def get_users(session: requests.Session,
              page_size: int,
              users_list_url: str,
              token: str) -> list[dict]:
    """Returns a list of users from the JSON response from
    corresponding API call.
    """
    response = session.get(
        users_list_url,
        params={
            "page_size": page_size,
        },
        headers={
            "Authorization": f"Token {token}",
        }
    )
    return response.json()["results"]

def create_excel(user_list: list[dict]) -> None:
    """Creates excel file will all the users."""
    columns = user_list[0].keys()
    df = pd.DataFrame(user_list, columns=columns)
    df.head()

    df.to_excel('cvat_users.xlsx', index=False, freeze_panes=(1, 0))

def excel_creation_main():     
    """Driver function to initiate the whole process.
    Should be used in Telegram bot to dynamically create .xlsx files.
    """
    session = get_session()
    page_size = get_page_size(session, USERS_LIST_URL)
    token = get_token(session, HOSTNAME, USERNAME, PASSWORD)
    users = get_users(session, page_size, USERS_LIST_URL, token)
    create_excel(users)
