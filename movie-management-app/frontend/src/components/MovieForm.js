// frontend/src/components/MovieForm.js
import React, { useState, useEffect } from 'react';

function MovieForm({ onSave, currentMovie, onCancel }) {
    const [formData, setFormData] = useState({
        movieID: '',
        title: '',
        director: '',
        releaseYear: '',
        genre: '',
        rating: '',
    });

    const isEditing = currentMovie !== null;

    useEffect(() => {
        // If we are editing, populate the form with the movie's data
        if (isEditing) {
            setFormData(currentMovie);
        }
    }, [currentMovie, isEditing]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(formData);
        // Reset form after saving
        setFormData({
            movieID: '',
            title: '',
            director: '',
            releaseYear: '',
            genre: '',
            rating: '',
        });
    };

    return (
        <form onSubmit={handleSubmit} className="movie-form">
            <h2>{isEditing ? 'Edit Movie' : 'Add a New Movie'}</h2>
            <input
                type="text"
                name="movieID"
                value={formData.movieID}
                onChange={handleChange}
                placeholder="Movie ID (e.g., tt0111161)"
                required
                disabled={isEditing} // Disable editing the ID
            />
            <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Title"
                required
            />
            <input
                type="text"
                name="director"
                value={formData.director}
                onChange={handleChange}
                placeholder="Director"
                required
            />
            <input
                type="number"
                name="releaseYear"
                value={formData.releaseYear}
                onChange={handleChange}
                placeholder="Release Year"
                required
            />
            <input
                type="text"
                name="genre"
                value={formData.genre}
                onChange={handleChange}
                placeholder="Genre"
                required
            />
            <input
                type="number"
                name="rating"
                value={formData.rating}
                onChange={handleChange}
                placeholder="Rating (1-10)"
                min="1"
                max="10"
                required
            />
            <div className="form-buttons">
                <button type="submit">{isEditing ? 'Update Movie' : 'Add Movie'}</button>
                {isEditing && <button type="button" onClick={onCancel}>Cancel</button>}
            </div>
        </form>
    );
}

export default MovieForm;
