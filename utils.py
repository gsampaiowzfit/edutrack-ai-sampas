import requests
# pyrefly: ignore [missing-import]
import streamlit as st
import json
import os

INSTANCE_URL = "https://x8ki-letl-twmt.n7.xano.io"

API_GROUPS = {
    "auth": f"{INSTANCE_URL}/api:B0UmRltb",
    "members": f"{INSTANCE_URL}/api:IZNk6f4y",
    "subjects": f"{INSTANCE_URL}/api:C3FBb9tZ",
    "academic_tasks": f"{INSTANCE_URL}/api:TasksGroup"
}

def get_headers():
    headers = {
        "Content-Type": "application/json",
        "X-Xano-Branch": "v1"
    }
    if "auth_token" in st.session_state:
        headers["Authorization"] =  f"Bearer {st.session_state['auth_token']}"
    return headers

def check_auth_error(response):
    if response.status_code in [401, 403]:
        st.session_state["auth_token"] = None
        st.session_state["user_name"] = None
        st.rerun()

def xano_get(group_name, endpoint):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            return response.json()
        check_auth_error(response)
        return None
    except Exception:
        return None

def xano_post(group_name, endpoint, data):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.post(url, json=data, headers=get_headers())
        if response.status_code in [200, 201]:
            return response.json()
        check_auth_error(response)
        st.warning(f"[DEBUG] {endpoint} → {response.status_code}: {response.text}")
        return None
    except Exception as e:
        st.warning(f"[DEBUG] Exceção em {endpoint}: {e}")
        return None

def xano_patch(group_name, endpoint, data):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.patch(url, json=data, headers=get_headers())
        if response.status_code == 200:
            return response.json()
        check_auth_error(response)
        return None
    except Exception:
        return None

def xano_delete(group_name, endpoint):
    try:
        url = f"{API_GROUPS[group_name]}/{endpoint}"
        response = requests.delete(url, headers=get_headers())
        if response.status_code == 200:
            return True
        check_auth_error(response)
        return False
    except Exception:
        return False

SESSION_FILE = ".xano_session.json"

def save_session(auth_token, user_name):
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"auth_token": auth_token, "user_name": user_name}, f)
    except Exception:
        pass

def load_session():
    if "auth_token" not in st.session_state:
        st.session_state["auth_token"] = None
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = None
        
    if st.session_state["auth_token"] is None:
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    st.session_state["auth_token"] = data.get("auth_token")
                    st.session_state["user_name"] = data.get("user_name")
            except Exception:
                pass

def clear_session():
    if "auth_token" in st.session_state:
        st.session_state["auth_token"] = None
    if "user_name" in st.session_state:
        st.session_state["user_name"] = None
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception:
            pass
