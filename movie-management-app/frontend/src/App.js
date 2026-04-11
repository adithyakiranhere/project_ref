// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import MovieList from './components/MovieList';
import MovieForm from './components/MovieForm';
import movieService from './services/movieService';
import './App.css'; // This will import our beautiful new styles

function App() {
    const [movies, setMovies] = useState([]);
    const [currentMovie, setCurrentMovie] = useState(null); // To hold movie being edited

    // Fetch movies from the backend when the component loads
    useEffect(() => {
        fetchMovies();
    }, []);

    const fetchMovies = async () => {
        try {
            const data = await movieService.getMovies();
            setMovies(data);
        } catch (error) {
            console.error("Failed to fetch movies:", error);
        }
    };

    // Handler for saving a movie (both add and update)
    const handleSave = async (movieData) => {
        try {
            if (currentMovie) {
                // We are updating an existing movie
                await movieService.updateMovie(currentMovie.movieID, movieData);
            } else {
                // We are adding a new movie
                await movieService.addMovie(movieData);
            }
            fetchMovies(); // Refresh the list
            setCurrentMovie(null); // Reset the form
        } catch (error) {
            console.error("Failed to save movie:", error);
        }
    };

    // Handler to set the current movie for editing
    const handleEdit = (movie) => {
        setCurrentMovie(movie);
    };

    // Handler to cancel editing
    const handleCancel = () => {
        setCurrentMovie(null);
    };

    // Handler for deleting a movie
    const handleDelete = async (movieID) => {
        if (window.confirm('Are you sure you want to delete this movie?')) {
            try {
                await movieService.deleteMovie(movieID);
                fetchMovies(); // Refresh the list
            } catch (error) {
                console.error("Failed to delete movie:", error);
            }
        }
    };

    return (
        <div className="app-container">
            <header>
                <h1>Movie Management System</h1>
            </header>
            <main>
                <MovieForm
                    onSave={handleSave}
                    currentMovie={currentMovie}
                    onCancel={handleCancel}
                    className="glass-effect"
                />
                <div className="list-container">
                    <h2>My Movie List</h2>
                    <MovieList movies={movies} onEdit={handleEdit} onDelete={handleDelete} />
                </div>
            </main>
        </div>
    );
}

export default App;
