const OpenAI = require('openai');
const express = require('express');
const cors = require('cors');
const multer = require('multer');
require('dotenv').config();
// const { Configuration, OpenAIApi } = require('openai');
const fs = require('fs');
const path = require('path');
const apiKey = process.env.OPENAI_API_KEY;

// if (!process.env.OPENAI_API_KEY) {
//   console.error('Error: OPENAI_API_KEY is not set.');
//   process.exit(1); // Exit the application if the API key is missing
// }

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const app = express();

require('dotenv').config();



app.use(express.json());
app.use(cors());

const upload = multer({ dest: 'uploads/' });

// Endpoint to process transcript
app.post('/transcript/process', upload.single('transcript'), async (req, res) => {
  try {
    const { transcript } = req.body; // Extract the transcript text from the request body

    if (!transcript) {
      return res.status(400).json({ error: 'Transcript text is required.' });
    }
    // Call OpenAI API to simplify the transcript
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
          { role: "system", content: "You are a helpful assistant." },
          {
              role: "user",
              content: "Simplify the following meeting transcript into plain language:\n\n${fileContent}",
          },
      ],
    });

    // Log the response from OpenAI
    console.log('Response from OpenAI:', completion.choices[0].message);

    // Delete the file after processing
    fs.unlinkSync(filePath);

    const plainText = response.data.choices[0].text.trim();
    res.status(200).json({ plainText });
  } catch (error) {
    console.error('Error processing transcript:', error);
    res.status(500).json({ error: 'Failed to process transcript.' });
  }
});

// Error handling
app.use((req, res) => {
  res.status(404).send({ error: 'Endpoint not found' });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

