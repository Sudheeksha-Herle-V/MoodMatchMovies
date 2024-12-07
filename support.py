import random as r
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['MovieDB']  # Replace with your database name
movies_collection = db['movies']  # Replace with your collection name

# Define genre pools
positive_genres = ['Action', 'Comedy', 'Drama']
negative_genres = ['Horror', 'Thriller', 'Documentary']

# Map for emotion to sentiment
emotion_dict = {0: 'Angry', 1: 'Disgusted', 2: 'Fearful', 4: 'Happy', 5: 'Sad', 6: 'Surprised'}
face_map = {'Angry': 0, 'Disgusted': 0, 'Fearful': 0, 'Happy': 1, 'Sad': 0, 'Surprised': 1}
color_map = {'Black': 0, 'White': 1, 'Red': 0, 'Yellow': 1, 'Blue': 1}

# Function to get positive and negative sentiment from selected colors
def get_pos_neg(sentiments):
    pos, neg = 0, 0
    for sentiment in sentiments:
        if color_map.get(sentiment, 0) == 1:
            pos += 1
        else:
            neg += 1
    return pos, neg

# Function to determine the final sentiment based on color sentiment and face sentiment
def get_final_sentiment(color_sentiment, face_id=None):
    if face_id is not None and face_id in face_map:
        face_val = face_map[emotion_dict.get(face_id, 'Unknown')]
        pos, neg = color_sentiment
        if face_val == 1:
            return 'pos' if pos + 1 > neg else 'neg'
        elif face_val == 0:
            return 'neg' if neg + 1 > pos else 'pos'
    return 'neutral'  # Return 'neutral' if no strong sentiment is detected

# Function to fetch movies from the database based on genre
def get_movie_from_db(genre):
    try:
        movies = movies_collection.find({"genre": genre})  # Assuming you have a genre field
        movie_names = []
        movie_poster_links = []
        
        for movie in movies:
            movie_names.append(movie['title'])  # Assuming the movie's title is in the 'title' field
            movie_poster_links.append(movie['poster'])  # Assuming the poster URL is in the 'poster' field
        
        return movie_names, movie_poster_links
    except Exception as e:
        print(f"Error fetching from database: {e}")
        return [], []

# Function to get genres based on sentiment type
def get_genres_based_on_sentiment(sentiment_type):
    if sentiment_type == 'pos':  # Positive sentiment
        return list(set(positive_genres + negative_genres))
    elif sentiment_type == 'neg':  # Negative sentiment
        return positive_genres
    elif sentiment_type == 'neutral':  # Neutral sentiment
        return positive_genres + negative_genres  # Include all genres for neutral sentiment
    else:
        return []

# Function to suggest movies based on the final sentiment
def suggest_movie(final_emotion):
    genre_list = get_genres_based_on_sentiment(final_emotion)
    movie_names = []
    movie_poster_links = []
    movie_genres = []

    for genre in genre_list:
        movie_name, poster_link = get_movie_from_db(genre)
        movie_names.extend(movie_name)
        movie_poster_links.extend(poster_link)
        movie_genres.extend([genre] * len(movie_name))  # Assuming you want the genre for each movie
    
    return movie_names, movie_poster_links, movie_genres  # Return movie names, posters, and genres


# Function to get all recommendations based on selected colors and face sentiment
def get_all_recom(all_color, face_id):
    try:
        final_emotion = get_final_sentiment(get_pos_neg(all_color), face_id)
        movie_names, movie_poster_links, movie_genres = suggest_movie(final_emotion)
        
        return movie_names, movie_poster_links, movie_genres  # Return movie names, posters, and genres
    except Exception as e:
        print(f"Error in get_all_recom: {e}")
        return [], [], []  # Return empty lists in case of error
