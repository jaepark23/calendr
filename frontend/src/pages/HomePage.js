import React, {useState} from "react";
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import FileUpload from "../components/FileUpload"
import TopBar from "../components/TopBar"
import LoadingPage from "./LoadingPage";
import axios from 'axios';
import { TextField, Button, Box } from '@mui/material';

function HomePage() {
  const [loading, setLoading] = useState(false); 
  const [showInputField, setShowInputField] = useState(false); 
  const [courseNumber, setCourseNumber] = useState(''); 
  const [calendarData, setCalendarData] = useState(null); 


  const handleAdditionalInfoSubmit = async () => {
    try {
      setLoading(true);
      setShowInputField(false);
      console.log("data:", calendarData);
      calendarData['course_number'] = courseNumber;
      const response = await axios.post('http://localhost:8000/submit_course_name', calendarData, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      const data = response.data;
      console.log("data:", data);
      setLoading(false);
      if(data.success == true && data.code == 200) {
        console.log("success resubmitting");
      } else {
        console.log("error resubmitting information");
      }
    } catch (error) {
      console.error('Error submitting additional information:', error);
    }
  };

  return (
    <div>
      <CssBaseline />
      <TopBar/>
      {loading ? (
      <LoadingPage/> 
      ) : showInputField ? (
        <Container
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
        <Box 
        display="flex" 
        alignItems="center" 
        justifyContent="center" 
        sx={{ mt: 2 }}
      >
        <TextField
          variant="outlined"
          label="Course Number"
          placeholder="Enter course number"
          value={courseNumber}
          onChange={(e) => setCourseNumber(e.target.value)}
          sx={{ mr: 2 }}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleAdditionalInfoSubmit}
        >
          Submit Info
        </Button>
      </Box> </Container>) : (<Container
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
          <FileUpload setLoading={setLoading} setShowInputField={setShowInputField} setCalendarData={setCalendarData} />
          
      </Container>)}

      </div>
  );
}

export default HomePage;
