import React, { useState } from 'react';
import Label from './components/Label';

const App = () => {
  const [url, setUrl] = useState('');
  const [location, setLocation] = useState('');
  const [labels, setLabels] = useState([]);
  const [error, setError] = useState('');

  const fetchLocation = async () => {
    setError('');
    try {
      const formData = new FormData();
      formData.append('url', url);

      const response = await fetch('/get-location', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.error) {
        setError(data.error);
        setLocation('');
      } else {
        setLocation(data.location);
      }
    } catch (err) {
      setError('Failed to fetch location');
    }
  };

  const addToQueue = () => {
    if (!url || !location) {
      setError('URL and location must be provided');
      return;
    }

    const label = { url, location };
    setLabels([...labels, label]);
    setUrl('');
    setLocation('');
    setError('');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="container">
      <h1>Electronics Label Maker</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          placeholder="Paste PartsBox URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button type="button" onClick={fetchLocation}>Fetch Location</button>
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <button type="button" onClick={addToQueue}>Add to Queue</button>
        <button type="button" onClick={handlePrint}>Print</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div id="print-area" className="label-list">
        {labels.map((part, idx) => (
          <Label key={idx} part={part} />
        ))}
      </div>
    </div>
  );
};

export default App;
