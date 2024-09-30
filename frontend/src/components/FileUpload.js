import React, { useState, useRef, useEffect } from 'react';
import { Button, TextField, Box, Alert, Typography, InputAdornment, IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';

function FileUpload({setLoading, setShowInputField, setCalendarData }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [csvUrl, setCsvUrl] = useState(null);
  const [isFetching, setIsFetching] = useState(false);
  const [courseNumber, setCourseNumber] = useState('');
  const [fileName, setFileName] = useState('');
  const [fileError, setFileError] = useState('');
  const fileInputRef = useRef(null);

  const fetchCSV = async () => {
    if (selectedFile) {
      setIsFetching(true);
      try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await axios.post('http://localhost:8000/extract_and_convert_events_to_csv', formData, {
          withCredentials: true,
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          responseType: 'blob'
        });
        const url = URL.createObjectURL(response.data);
        console.log(url);
        setCsvUrl(url);
        console.log(csvUrl);
      } catch (error) {
        console.error('Error uploading the file and downloading the CSV:', error);
      } finally {
        setLoading(false);
        setIsFetching(false);
      }
    }
  };

  const handleFileRemove = () => {
    setFileName('');
    setFileError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setFileName(file.name);
      setFileError('');
      setSelectedFile(file);
    } else {
      setFileName('');
    }
  };

  const handleSubmit = async (event) => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
      // switch to loading screen
      setLoading(true);
      // send initial request to extract events from pdf
      const response = await axios.post('http://localhost:8000/extract_events_to_google', formData, {
        withCredentials: true,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      const data = response.data;
      console.log('data:', data);
      setLoading(false);
      if (data.success == false && data.code == 100) {
        setShowInputField(true);
        const calendarData = data['data'];
        console.log("calendar data:", calendarData);
        setCalendarData(calendarData);
      } else if (data.success == true && data.code == 200) {
        // handle successful extraction
      }
    } else {
      console.error('No file selected');
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
        padding: 3,
        borderRadius: 2,
        boxShadow: 3,
        backgroundColor: '#2C2C2C',
        width: '50%',
        margin: '0 auto'
      }}
    >
      <Typography variant="h6" gutterBottom>
        Upload Your File
      </Typography>

      <TextField
        value={fileName}
        placeholder="No file chosen"
        InputProps={{
          readOnly: true,
          endAdornment: fileName && (
            <InputAdornment position="end">
              <IconButton onClick={handleFileRemove}>
                <CloseIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
        fullWidth
        variant="outlined"
      />

      <Button
        variant="contained"
        component="label"
        startIcon={<CloudUploadIcon />}
        color="secondary"
        fullWidth
        sx={{ textTransform: 'none' }}
      >
        Choose File
        <input
          type="file"
          hidden
          onChange={handleFileChange}
        />
      </Button>

      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        disabled={!fileName}
        fullWidth
        sx={{ textTransform: 'none' }}
      >
        Upload to Calendar
      </Button>
      <Button
        variant="contained"
        color="primary"
        disabled={!fileName}
        fullWidth
        sx={{ textTransform: 'none' }}
        onClick={fetchCSV}>
        {isFetching ? 'Processing...' : 'Upload and Download CSV'}
      </Button>
      {csvUrl && !isFetching && (
        <a href={csvUrl} download="calendar_data.csv">
          <Button>Download CSV</Button>
        </a>
      )}
      {fileError && <Alert severity="error">{fileError}</Alert>}
    </Box>
  );
}

export default FileUpload;