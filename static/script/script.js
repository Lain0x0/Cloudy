const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors'); // Import the CORS module

const app = express();
const port = 3000;

// Use CORS middleware to allow cross-origin requests
app.use(cors());

// Set up Multer storage to save files to 'uploads/data/'
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Ensure the 'uploads/data' directory exists
    const uploadDir = path.join(__dirname, 'uploads/data');
    fs.mkdirSync(uploadDir, { recursive: true });
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage });

// Serve static files from the 'uploads/data' directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads/data')));

// Handle file uploads
app.post('/uploads', upload.array('files[]', 10), (req, res) => {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ error: 'No files uploaded' });
    }

    const filePaths = req.files.map((file) => file.path);
    res.json({ filePaths });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
