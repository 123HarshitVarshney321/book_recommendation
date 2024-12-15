from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-S'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    
    return render_template('recommend.html')

@app.route('/recommend_books', methods = ['post'])
def recommend():
    user_input = request.form.get('user_input')
    if not user_input.strip():
        return render_template('recommend.html', message="Please enter a book name to get recommendations.")
    
    # Convert user_input to lowercase and search for matching books
    user_input_lower = user_input.strip().lower()
    
    # Create a list of book titles in lowercase to handle case insensitivity
    matching_books = [book.lower() for book in pt.index]

    # Check if the user input matches any book
    if user_input_lower not in matching_books:
        return render_template('recommend.html', message="Sorry, we couldn't find any books matching that title.")
    
    # Find the index of the matched book title
    index = matching_books.index(user_input_lower)
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)

    print(data)    
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)