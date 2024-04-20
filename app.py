import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from datetime import datetime

# Initialize session state variables for bills
if 'bills' not in st.session_state:
    st.session_state.bills = []

# Function to add or update a bill
def add_update_bill(bill_id, name, cost, date, type, is_paid):
    event_color = "#28a745" if is_paid else "#dc3545"  # Green if paid, red otherwise
    return {
        "id": bill_id,
        "title": f"{name} - ${cost} ({type})",
        "start": date.strftime('%Y-%m-%dT00:00:00'),
        "end": date.strftime('%Y-%m-%dT23:59:59'),
        "color": event_color,
        "extendedProps": {
            "is_paid": is_paid
        }
    }

# Bill input form
with st.form("bill_form"):
    st.write("### Add or Update a Bill")
    bill_name = st.text_input("Bill Name")
    bill_cost = st.number_input("Bill Cost", min_value=0.0, format="%.2f")
    bill_date = st.date_input("Bill Date", datetime.today())
    bill_type = st.selectbox("Bill Type", ['Utility', 'Credit Card', 'Rent', 'Mortgage', 'Other'])
    is_paid = st.checkbox("Paid?")
    submitted = st.form_submit_button("Submit")

    if submitted:
        bill_id = len(st.session_state.bills) + 1  # Simple unique ID for example
        new_bill = add_update_bill(bill_id, bill_name, bill_cost, bill_date, bill_type, is_paid)
        st.session_state.bills.append(new_bill)  # Add or update the bill

# Display calendar with bills
calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    }
}

custom_css = """
    .fc-event {
        font-size: 0.8rem;
        border: none;  /* Remove borders */
    }
    .fc-event-title {
        font-weight: bold;  /* Bold event titles */
    }
"""

if st.session_state.bills:
    cal = calendar(events=st.session_state.bills, options=calendar_options, custom_css=custom_css)
    st.write(cal)
else:
    st.write("No bills added yet.")
