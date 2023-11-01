import streamlit as st

# Define a function to show "Page 1" content
def page_one():
    st.subheader("Page 1 Content")
    # Add content for Page 1 here
    st.write("Welcome to Page 1")

# Define a function to show "Page 2" content
def page_two():
    st.subheader("Page 2 Content")
    # Add content for Page 2 here
    st.write("Welcome to Page 2")

# Create a sidebar with navigation buttons
selected_page = st.radio("Select Page", ("Page 1", "Page 2"))

# Display the selected page
if selected_page == "Page 1":
    page_one()
elif selected_page == "Page 2":
    page_two()
