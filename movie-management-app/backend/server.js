// backend/server.js
const express = require('express');
const dotenv = require('dotenv').config(); // Load environment variables first
const connectDB = require('./config/db'); // Import DB connection
const cors = require('cors'); // Import CORS

// Connect to database
connectDB();

const app = express();
const port = process.env.PORT || 5000;

// Middleware to parse JSON bodies
app.use(express.json());
// Middleware to allow CORS requests from the frontend
app.use(cors());

// Movie routes
app.use('/api/movies', require('./routes/movieRoutes'));

// Simple route for testing
app.get('/', (req, res) => {
    res.send('Movie Management API is running!');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
