import React, {useState} from 'react';
import { TextField, Button, Box } from '@mui/material';

function DownloadCSVButton() {
    const [csvUrl, setCsvUrl] = useState(null);

    const fetchCSV = async () => {
      try {
        const response = await fetch("http://localhost:8000/extract_and_convert_events_to_csv", {
          method: 'GET',
        });
  
        if (!response.ok) {
          throw new Error('CSV download failed.');
        }
  
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob); 
        setCsvUrl(url);
      } catch (error) {
        console.error('Error downloading the CSV file:', error);
      }
    };
  
    return (
      <div>
        <Button onClick={fetchCSV}>Fetch CSV</Button>
        {csvUrl && (
          <a href={csvUrl} download="data.csv">
            <Button>Download CSV</Button>
          </a>
        )}
      </div>
    );
}


export default DownloadCSVButton;
