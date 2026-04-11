// frontend/src/components/MovieCard.js
import React from 'react';
// Import the icons we need
import { FaPencilAlt, FaTrash } from 'react-icons/fa';

function MovieCard({ movie, onEdit, onDelete }) {
    return (
        <div className="movie-card glass-effect">
            <div className="movie-card-header">
                <h3>{movie.title}</h3>
                <div className="movie-rating">{movie.rating} / 10 ★</div>
            </div>
            <div className="movie-card-details">
                <p><strong>Director:</strong> {movie.director}</p>
                <p><strong>Release Year:</strong> {movie.releaseYear}</p>
                <p><strong>Genre:</strong> {movie.genre}</p>
            </div>
            <div className="movie-card-footer">
                <p className="movie-id">ID: {movie.movieID}</p>
                <div className="movie-card-actions">
                    <button className="icon-btn" onClick={() => onEdit(movie)}>
                        <FaPencilAlt />
                    </button>
                    <button className="icon-btn btn-delete" onClick={() => onDelete(movie.movieID)}>
                        <FaTrash />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default MovieCard;
