from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cinema_management']
movies_collection = db['movies']
bookings_collection = db['bookings']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        genre = request.form['genre']
        release_date = request.form['release_date']

        # Insert movie into MongoDB
        movie = {
            'name': movie_name,
            'genre': genre,
            'release_date': release_date
        }
        movies_collection.insert_one(movie)

        return redirect('/')
    return render_template('add_movie.html')

@app.route('/add_reservation', methods=['GET', 'POST'])
def add_reservation():
    movies = movies_collection.find()  # Fetch movies for dropdown
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        movie_name = request.form['movie_name']
        seats = int(request.form['seats'])

        # Insert reservation into MongoDB
        booking = {
            'customer_name': customer_name,
            'movie_name': movie_name,
            'seats': seats
        }
        bookings_collection.insert_one(booking)

        return redirect('/bookings')
    return render_template('add_reservation.html', movies=movies)

@app.route('/bookings')
def bookings():
    all_bookings = list(bookings_collection.find())
    return render_template('bookings.html', bookings=all_bookings)

if __name__ == '__main__':
    app.run(debug=True)
