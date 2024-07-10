import streamlit as st
import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from PIL import Image
import requests
from io import BytesIO
from PIL import Image

#Load the preprocessor, KNN models, processed subsets, and DataFrame
preprocessor = joblib.load('Streamlit/data/preprocessor.pkl')
knn_models = joblib.load('Streamlit/data/knn_models.pkl')
processed_subsets = joblib.load('Streamlit/data/processed_subsets.pkl')
best = pd.read_pickle('Streamlit/data/best_df.pkl')


# Function to recommend books
def recommend_books(book_title, df, knn_models, processed_subsets, preprocessor):
    # Find matching books
    matching_books = df[df['title'].str.contains(book_title, case=False, na=False)]
    
    if matching_books.empty:
        return [], []  # Return empty lists if no matching titles or books found

    # Confirm book with user
    matching_titles = matching_books['title'].tolist()
    return matching_titles, matching_books

def show_recommender():
    st.title("Welcome to Best Books Ever!:books:")

    # Display image
    try:
        image = Image.open("Streamlit/images/banner.png")
        st.image(image, caption='Welcome to the club', use_column_width=False, width=600)
    except FileNotFoundError:
        st.error("The image file was not found. Please check the file path.")

    st.header("Try it yourself!")

    # User input for the book recommender
    user_input = st.text_input("Enter the first letters of the title of the book you like:")

    if user_input:
        matching_titles, matching_books = recommend_books(user_input, best, knn_models, processed_subsets, preprocessor)
        
        if not matching_titles:
            st.write("Sorry, we don't have this book. Try another.")
        else:
            # Display matching titles for user to confirm
            selected_title = st.selectbox("Is this your book?", matching_titles)
            
            if selected_title:
                # Find the selected book from matching_books based on selected_title
                selected_book = None
                for book in matching_books.iterrows():
                    if book[1]['title'] == selected_title:
                        selected_book = book[1]
                        break
                
                if selected_book is None:
                    st.error("Selected book not found in matching books.")
                    return

                genre = selected_book['genre']
                
                if genre not in knn_models or genre not in processed_subsets:
                    st.write(f"Could not process genre: {genre}.")
                else:
                    processed_features, subset = processed_subsets[genre]
                    book_features = preprocessor.transform(pd.DataFrame([selected_book]))
                    
                    knn_model = knn_models[genre]
                    distances, indices = knn_model.kneighbors(book_features, n_neighbors=5)
                    
                    recommended_books = subset.iloc[indices[0]][['title', 'coverimg']].to_dict('records')
                    
                    # Display the chosen book with a specific message
                    st.write("This is the book you chose:")
                    st.write(f"{selected_book['title']} - {selected_book['author']}")  # Customize as per your DataFrame structure
                    try:
                        response = requests.get(selected_book['coverimg'])
                        img = Image.open(BytesIO(response.content))
                        st.image(img, width=300)
                    except Exception as e:
                        st.write("Image not found")

                    # Display recommended books excluding the chosen book
                    st.write("Recommended:")
                    for recommended_book in recommended_books:
                        if recommended_book['title'] != selected_title:  # Exclude the chosen book
                            st.write(f"I recommend {recommended_book['title']}")
                            try:
                                response = requests.get(recommended_book['coverimg'])
                                img = Image.open(BytesIO(response.content))
                                st.image(img, width=300)
                            except Exception as e:
                                st.write(f"Image not found for {recommended_book['title']}")