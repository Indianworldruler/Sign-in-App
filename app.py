import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with the credentials stored in st.secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])  # This assumes the secrets contain the JSON data as a string
    firebase_admin.initialize_app(cred)

# Firestore Client
db = firestore.client()

# Function to add or retrieve user data
def handle_user_data(user_name, user_text):
    # Reference to the users collection
    users_ref = db.collection('users')

    # Check if the user already exists in Firestore
    user_doc = users_ref.document(user_name).get()

    if user_doc.exists:
        # If user exists, retrieve their text
        stored_text = user_doc.to_dict().get('text', '')
        return f"Welcome back {user_name}! Your stored text is: {stored_text}"
    else:
        # If user doesn't exist, add them to the Firestore
        users_ref.document(user_name).set({
            'name': user_name,
            'text': user_text
        })
        return f"Hello {user_name}! Your text has been saved."

# Streamlit UI
st.title("User Sign-In and Text Retrieval")

# Inputs for name and text
user_name = st.text_input("Enter your name:")
user_text = st.text_input("Enter some random text:")

# Button to submit user data
if st.button("Sign In"):
    if user_name and user_text:
        # Handle user data based on input
        response = handle_user_data(user_name, user_text)
        st.write(response)
    else:
        st.write("Please enter both your name and text.")

# Optional: Button to retrieve text without entering new text (for logging in)
if st.button("Log In"):
    if user_name:
        response = handle_user_data(user_name, '')
        st.write(response)
    else:
        st.write("Please enter your name to log in.")
