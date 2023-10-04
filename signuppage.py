import streamlit as st
import pandas as pd
import base64

# Streamlit app
st.title("Sign-up Page")

# User input fields
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Sign Up"):
    # Check if passwords match
    if password == confirm_password:
        # Load existing data from the Excel file (if it exists)
        try:
            # Load the Excel file from GitHub
            df = pd.read_excel("https://github.com/yourusername/your-repo/raw/main/user_data.xlsx")
        except Exception as e:
            # If the file doesn't exist, create an empty DataFrame
            df = pd.DataFrame(columns=["Username", "Email", "Password"])

        # Append the new user data
        new_user = {"Username": username, "Email": email, "Password": password}
        df = pd.concat([df, pd.DataFrame(new_user, index=[0])], ignore_index=True)

        # Create a new Excel file
        df.to_excel("user_data.xlsx", index=False)

        st.success("You have successfully signed up!")
    else:
        st.error("Passwords do not match.")

# Display the current user data
try:
    current_data = pd.read_excel("https://github.com/yourusername/your-repo/raw/main/user_data.xlsx")
    st.subheader("Current User Data")
    st.write(current_data)
except Exception as e:
    st.info("No user data available yet.")
