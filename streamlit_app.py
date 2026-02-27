import streamlit as st

# Define categories and their options
categories = {
    "Pronouns": ["he", "she", "they", "it", "I", "you", "we"],
    "Verbs": ["runs", "jumps", "eats", "sleeps", "talks"],
    "Nouns": ["dog", "cat", "house", "tree", "person"]
}

selected_words = []

st.subheader("Select your words:")

for category, options in categories.items():
    selection = st.selectbox(f"Choose a {category.lower()}:", options, key=category)
    if selection:
        selected_words.append(selection)

st.subheader("Your selected sentence:")
st.text_area("", " ".join(selected_words), height=100)
