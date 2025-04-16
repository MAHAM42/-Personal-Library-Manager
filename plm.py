import streamlit as st

# 💅 Custom CSS Styling
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")

st.markdown("""
<style>
/* 🔶 Main headings color (orange) */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #ff6f00 !important;
}

/* 💗 Sidebar menu (radio) - active/pink on hover and click */
div[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover,
div[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:focus-within,
div[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-selected="true"] {
    background-color: #f8bbd0 !important; /* Light Pink */
    border-radius: 8px;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# 📦 Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = []

st.title("📚 Personal Library Manager")
st.markdown("Manage your books easily with a sleek Streamlit app.")

# 📋 Sidebar Navigation
menu = st.sidebar.radio("📋 Menu", ["Add Book", "View Books", "Search Book", "Delete Book"])

# 🧠 Smart Description Generator
def generate_description(title, author, year):
    title_lower = title.lower()
    
    if "love" in title_lower:
        return f"'{title}' is a heartwarming tale that explores the depths of human emotion and connection. Written by {author} in {year}, it delves into the complexities of love and relationships."
    elif "war" in title_lower or "battle" in title_lower:
        return f"In '{title}', {author} brings the chaos and courage of war to life. Published in {year}, it's a gripping narrative of survival and honor."
    elif "mystery" in title_lower or "secret" in title_lower:
        return f"'{title}' is a thrilling mystery penned by {author} in {year}. It's filled with unexpected twists that keep readers on the edge of their seats."
    elif "future" in title_lower or "robot" in title_lower:
        return f"Set in a futuristic world, '{title}' by {author} (published in {year}) dives into the realm of artificial intelligence and humanity’s destiny."
    elif "history" in title_lower or "empire" in title_lower:
        return f"'{title}' is a deep dive into the historical events that shaped civilizations. {author}'s work from {year} combines research with storytelling brilliance."
    elif "dark" in title_lower or "night" in title_lower:
        return f"'{title}' by {author} (written in {year}) explores themes of darkness—both literal and metaphorical—in a captivating and poetic manner."
    else:
        return f"'{title}' is a fascinating book written by {author} in {year}. It offers unique insights, storytelling depth, and a memorable reading experience."

# 🖼️ Placeholder Image Generator
def generate_image_url(title):
    return f"https://via.placeholder.com/300x400.png?text={'+'.join(title.split())}"

# ➕ Add Book
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    with st.form("book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Year of Publication")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            description = generate_description(title, author, year)
            image_url = generate_image_url(title)
            st.session_state.library.append({
                "Title": title,
                "Author": author,
                "Year": year,
                "Description": description,
                "Image": image_url
            })
            st.success(f"✅ '{title}' added successfully!")

# 📖 View Books
elif menu == "View Books":
    st.subheader("📖 All Books in Your Library")
    if st.session_state.library:
        for idx, book in enumerate(st.session_state.library):
            st.markdown(f"### {idx + 1}. {book['Title']}")
            st.image(book['Image'], width=200)
            st.markdown(f"**Author:** {book['Author']}")
            st.markdown(f"**Year:** {book['Year']}")
            st.markdown(f"**Description:** {book['Description']}")
            st.markdown("---")
    else:
        st.warning("No books added yet!")

# 🔍 Search Book
elif menu == "Search Book":
    st.subheader("🔍 Search Books")
    keyword = st.text_input("Enter keyword (title or author):")
    if keyword:
        results = [book for book in st.session_state.library if keyword.lower() in book['Title'].lower() or keyword.lower() in book['Author'].lower()]
        if results:
            st.success(f"Found {len(results)} result(s):")
            for book in results:
                st.markdown(f"### {book['Title']}")
                st.image(book['Image'], width=200)
                st.markdown(f"**Author:** {book['Author']}")
                st.markdown(f"**Year:** {book['Year']}")
                st.markdown(f"**Description:** {book['Description']}")
                st.markdown("---")
        else:
            st.error("No matching books found.")

# 🗑️ Delete Book
elif menu == "Delete Book":
    st.subheader("🗑️ Delete a Book")
    if st.session_state.library:
        book_titles = [f"{b['Title']} by {b['Author']}" for b in st.session_state.library]
        to_delete = st.selectbox("Select a book to delete:", book_titles)
        if st.button("Delete"):
            index = book_titles.index(to_delete)
            removed = st.session_state.library.pop(index)
            st.success(f"✅ '{removed['Title']}' deleted successfully!")
    else:
        st.warning("Library is empty. Nothing to delete.")
