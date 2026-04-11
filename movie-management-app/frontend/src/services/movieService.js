// frontend/src/services/movieService.js
import axios from 'axios';

// The base URL of our backend API
const API_URL = 'http://localhost:5000/api/movies/';

// Get all movies
const getMovies = async () => {
    const response = await axios.get(API_URL);
    return response.data;
};

// Add a new movie
const addMovie = async (movieData) => {
    const response = await axios.post(API_URL, movieData);
    return response.data;
};

// Update a movie by its movieID
const updateMovie = async (movieID, movieData) => {
    const response = await axios.put(API_URL + movieID, movieData);
    return response.data;
};

// Delete a movie by its movieID
const deleteMovie = async (movieID) => {
    const response = await axios.delete(API_URL + movieID);
    return response.data;
};

const movieService = {
    getMovies,
    addMovie,
    updateMovie,
    deleteMovie,
};

export default movieService;
