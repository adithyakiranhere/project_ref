// backend/models/Movie.js
const mongoose = require('mongoose');

const movieSchema = mongoose.Schema(
    {
        movieID: {
            type: String,
            required: [true, 'Please add a movie ID'],
            unique: true,
        },
        title: {
            type: String,
            required: [true, 'Please add a title'],
        },
        director: {
            type: String,
            required: [true, 'Please add a director'],
        },
        releaseYear: {
            type: Number,
            required: [true, 'Please add a release year'],
        },
        genre: {
            type: String,
            required: [true, 'Please add a genre'],
        },
        rating: {
            type: Number,
            min: 1,
            max: 10,
            required: [true, 'Please add a rating (1-10)'],
        },
    },
    {
        timestamps: true, // Adds createdAt and updatedAt fields automatically
    }
);

module.exports = mongoose.model('Movie', movieSchema);
