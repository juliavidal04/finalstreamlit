import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time
import gspread
from google.oauth2.service_account import Credentials

# ============================== #
# Fetch Data from Google Sheets
# ============================== #
@st.cache_data
def fetch_google_sheets_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time
import gspread
from google.oauth2.service_account import Credentials

# ============================== #
# Fetch Data from Google Sheets
# ============================== #
@st.cache_data
def fetch_google_sheets_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # ✅ Load credentials from Streamlit secrets (instead of "hola2.json")
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

    client = gspread.authorize(creds)
    sheet = client.open("hola2").sheet1  # Ensure this is the correct sheet name
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = fetch_google_sheets_data()

# ============================== #
#  Streamlit UI
# ============================== #
st.title("Dow Jones Data Visualization")
st.subheader("Which trend do you observe in the Dow Jones Industrial Average?")

# ============================== #
#  A/B Testing Functionality
# ============================== #
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None

if "chart_displayed" not in st.session_state:
    st.session_state["chart_displayed"] = None

# Function to create Chart A
def plot_chart_a():
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="Date", y="Price", marker="o", color="blue", ax=ax)
    ax.set_title("Dow Jones Industrial Average Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Dow Jones Price")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Function to create Chart B
def plot_chart_b():
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Date", y="Price", color="green", ax=ax)
    ax.set_title("Dow Jones Price by Month")
    ax.set_xlabel("Date")
    ax.set_ylabel("Dow Jones Price")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ============================== #
#  Show Charts Based on Random Choice
# ============================== #
if st.button("Show a chart", key="show_chart"):
    st.session_state["chart_displayed"] = random.choice(["A", "B"])
    st.session_state["start_time"] = time.time()  # Start measuring time

    if st.session_state["chart_displayed"] == "A":
        plot_chart_a()
    else:
        plot_chart_b()

# ============================== #
#  Measure User Response Time
# ============================== #
# Ensure the key exists in session state before fetching data
if "google_sheets_data" not in st.session_state:
    client = gspread.authorize(creds)
    sheet = client.open("hola2").sheet1  # Make sure your Google Sheet is named "hola2"
    data = sheet.get_all_records()
    st.session_state["google_sheets_data"] = pd.DataFrame(data)  # Store data in session state

df = st.session_state["google_sheets_data"]  # Use cached data


# ============================== #
#  Streamlit UI
# ============================== #
st.title("Dow Jones Data Visualization")
st.subheader("Which trend do you observe in the Dow Jones Industrial Average?")

# ============================== #
#  A/B Testing Functionality
# ============================== #
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None

if "chart_displayed" not in st.session_state:
    st.session_state["chart_displayed"] = None

# Function to create Chart A
def plot_chart_a():
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="Date", y="Price", marker="o", color="blue", ax=ax)
    ax.set_title("Dow Jones Industrial Average Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Dow Jones Price")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Function to create Chart B
def plot_chart_b():
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Date", y="Price", color="green", ax=ax)
    ax.set_title("Dow Jones Price by Month")
    ax.set_xlabel("Date")
    ax.set_ylabel("Dow Jones Price")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ============================== #
#  Show Charts Based on Random Choice
# ============================== #
if st.button("Show a chart", key="show_chart"):
    st.session_state["chart_displayed"] = random.choice(["A", "B"])
    st.session_state["start_time"] = time.time()  # Start measuring time

    if st.session_state["chart_displayed"] == "A":
        plot_chart_a()
    else:
        plot_chart_b()

    

# ============================== #
#  Measure User Response Time
# ============================== #
if st.session_state["chart_displayed"] and st.button("Submit Response", key="submit_response"):
    end_time = time.time()
    response_time = round(end_time - st.session_state["start_time"], 2)
    st.write(f"⏳ You took **{response_time} seconds** to answer!")
