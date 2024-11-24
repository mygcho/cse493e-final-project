import { useState } from 'react';
import './TranscriptUploader.css'; // Update the styles for the new component.

const TranscriptUploader = () => {
  const [transcriptText, setTranscriptText] = useState('');
  const [processedTranscript, setProcessedTranscript] = useState('');

  const handleSubmit = async () => {
    if (!transcriptText.trim()) {
      alert('Please paste a transcript to process.');
      return;
    }

    try {
      const response = await fetch('http://localhost:3001/transcript/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ transcript: transcriptText }), // Send the pasted text as JSON
      });

      if (!response.ok) {
        throw new Error('Failed to process the transcript.');
      }

      const data = await response.json();
      setProcessedTranscript(data.plainText);
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while processing the transcript.');
    }
  };

  return (
    <div className='transcript-uploader-container'>
      <textarea
        placeholder="Paste your transcript here..."
        value={transcriptText}
        onChange={(e) => setTranscriptText(e.target.value)}
        rows="10"
        cols="50"
        className="transcript-input"
      ></textarea>
      <button onClick={handleSubmit}>Process Transcript</button>
      {processedTranscript && (
        <div className='transcript-output'>
          <h3>Processed Transcript:</h3>
          <pre>{processedTranscript}</pre>
        </div>
      )}
    </div>
  );
};

export default TranscriptUploader;
