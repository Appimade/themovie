from flask import Flask, render_template, request
from imdb import IMDb
import requests
import os

app = Flask(__name__)

def fetch_movie_poster(title):
    ia = IMDb()
    movies = ia.search_movie(title)
    
    if not movies:
        return None
    
    movie = movies[0]
    ia.update(movie)
    
    if 'cover url' in movie:
        return movie['cover url']
    else:
        return None

def save_image(url, title):
    # Create the images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    response = requests.get(url)
    image_path = os.path.join('images', f"{title.replace(' ', '_')}.jpg")

    with open(image_path, 'wb') as file:
        file.write(response.content)

    return image_path

@app.route('/', methods=['GET', 'POST'])
def home():
    poster_url = None
    image_path = None
    if request.method == 'POST':
        movie_title = request.form['title']
        poster_url = fetch_movie_poster(movie_title)
        if poster_url:
            image_path = save_image(poster_url, movie_title)
    
    return render_template('index.html', poster_url=poster_url, image_path=image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)


