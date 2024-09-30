import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useAuth } from '../auth/AuthContext';

function CalendarEvents() {
    const [events, setEvents] = useState([]);
    const { login, isAuthenticated } = useAuth();

    useEffect(() => {
        const fetchEvents = async () => {
            const token = Cookies.get('access_token');
            if (token) {
                try {
                    const response = await fetch('http://localhost:8000/calendar_events', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json',
                        },
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    setEvents(data.events);
                } catch (error) {
                    console.error('Error fetching events:', error);
                }
            }
        };

        fetchEvents();
    }, []);

    return (
        <div>
            <h1>Calendar Events</h1>
            <ul>
                {events.map(event => (
                    <li key={event.id}>
                        {event.summary} - {event.start.dateTime || event.start.date}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default CalendarEvents;
