import os
import msal
import json
from pathlib import Path
from dotenv import load_dotenv

CACHE_PATH = os.path.join(os.path.dirname(__file__), ".msal_cache.json")
CLIENT_ID = "3e747674-29a3-46ec-be9e-faa584989c87"
TENANT_ID = "30520885-0a26-49e9-a66d-b53f7e1f958b"
SCOPES = ["Files.ReadWrite"]

def get_graph_token():
    """
    Acquire and cache a Microsoft Graph token using device code flow. Returns the access token.
    """
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            cache.deserialize(f.read())
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache
    )
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception(f"Failed to create device flow: {flow}")
    print(f"To sign in, use a web browser to open {flow['verification_uri']} and enter the code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        with open(CACHE_PATH, "wb") as f:
            f.write(cache.serialize().encode("utf-8"))
        return result["access_token"]
    else:
        raise Exception(f"Could not acquire token: {result}")

# --- Boilerplate utilities from test_utils_boilerplate.py ---
def load_env():
    """Load environment variables from .env file."""
    load_dotenv()

def inject_id_token(module_name: str, cache_relative_path='test/.msal_cache.json'):
    """Inject idToken from msal cache into the given module's globals."""
    import importlib
    msal_cache_path = Path(__file__).parents[1] / cache_relative_path
    if msal_cache_path.exists():
        with open(msal_cache_path, 'r') as f:
            msal_data = json.load(f)
            id_tokens = msal_data.get('IdToken', {})
            if id_tokens:
                first_token = next(iter(id_tokens.values()))
                id_token = first_token.get('secret')
                module = importlib.import_module(module_name)
                module.__dict__['idToken'] = id_token
                return id_token
    return None

def load_test_cases_json(json_path):
    """Loads test cases from the given JSON file path."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def parametrize_cases(data, pytest):
    """Wrap each case in pytest.param, using 'id' for test identification."""
    return [pytest.param(case, id=case.get("id", f"test_case_{i}")) for i, case in enumerate(data)]
