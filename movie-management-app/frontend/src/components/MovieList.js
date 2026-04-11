// frontend/src/components/MovieList.js
import React from 'react';
import MovieCard from './MovieCard'; // Import the new component

function MovieList({ movies, onEdit, onDelete }) {
    if (movies.length === 0) {
        return <p className="no-movies-message">No movies added yet. Use the form to add your first movie!</p>;
    }

    return (
        <div className="movie-list">
            {movies.map((movie) => (
                <MovieCard 
                    key={movie.movieID} 
                    movie={movie} 
                    onEdit={onEdit} 
                    onDelete={onDelete} 
                />
            ))}
        </div>
    );
}

export default MovieList;
