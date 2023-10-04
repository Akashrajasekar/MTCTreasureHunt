import streamlit as st
import pandas as pd
import base64
import io

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
            # Load the Excel file from GitHub using its raw URL
            excel_url = "https://github.com/yourusername/your-repo/raw/main/user_data.xlsx"
            df = pd.read_excel(excel_url)
        except Exception as e:
            # If the file doesn't exist, create an empty DataFrame
            df = pd.DataFrame(columns=["Username", "Email", "Password"])

        # Append the new user data
        new_user = {"Username": username, "Email": email, "Password": password}
        df = df.append(new_user, ignore_index=True)

        # Convert the updated DataFrame to Excel binary data
        excel_data = df.to_excel(index=False)
        excel_binary = io.BytesIO()
        excel_binary.write(excel_data)
        excel_binary.seek(0)

        # Update the Excel file on GitHub using the GitHub API
        import requests

        file_url = "https://api.github.com/repos/yourusername/your-repo/contents/user_data.xlsx"
        headers = {
            "Authorization": "token YOUR_GITHUB_TOKEN",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {
            "message": "Updated user_data.xlsx",
            "content": base64.b64encode(excel_binary.read()).decode("utf-8"),
            "branch": "main",
            "sha": "your_sha",  # Replace with the SHA of the existing file
        }
        response = requests.put(file_url, headers=headers, json=data)

        if response.status_code == 200:
            st.success("You have successfully signed up!")
        else:
            st.error("Failed to update user_data.xlsx on GitHub.")
    else:
        st.error("Passwords do not match.")

# Display the current user data
try:
    current_data = pd.read_excel("https://github.com/yourusername/your-repo/raw/main/user_data.xlsx")
    st.subheader("Current User Data")
    st.write(current_data)
except Exception as e:
    st.info("No user data available yet.")
