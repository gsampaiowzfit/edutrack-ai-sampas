import requests
import streamlit as st

INSTANCE_URL = "https://x8ki-letl-twmt.n7.xano.io"

API_GROUPS = {
    "auth": f"{INSTANCE_URL}/api:B0UmRltb",
    "members": f"{INSTANCE_URL}/api:IZNk6f4y",
    "subjects": f"{INSTANCE_URL}/api:oxEv2xgd"
}

def get_headers():
    headers = {"Content-Type": "application/json"}
    if "auth_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state['auth_token']}"
    return headers

def xano_get(group_name, endpoint):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def xano_post(group_name, endpoint, data):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.post(url, json=data, headers=get_headers())
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception:
        return None

def xano_patch(group_name, endpoint, data):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.patch(url, json=data, headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def xano_delete(group_name, endpoint):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.delete(url, headers=get_headers())
        if response.status_code == 200:
            return True
        return False
    except Exception:
        return False
