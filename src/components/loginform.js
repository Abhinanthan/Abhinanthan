// FormComponent.js
import './loginform.css';
import React, { useState } from 'react';
import { useEffect } from 'react';
//import dgram from 'dgram';  
const FormComponent = () => {
  const [cropInfo, setCropInfo] = useState(' ');
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    humidity: '',
    ph: '',
    rainfall: '',
    temperature: '',
  }); 

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    (async () => {
      // Convert formData to JSON
      const formDataJson = JSON.stringify(formData);
      
      // Display form data in console
      console.log(formDataJson);
      
      // Send formDataJson to API endpoint
      try {//http://127.0.0.1:5000
        const response = await fetch('http://127.0.0.1:12345/receive_data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: formDataJson,
        });

        if (response.ok) {
          const data = await response.json();
          setCropInfo(data.label); // Update cropInfo with the received label
        } else {
          console.error('Failed to send form data');
        }
      } catch (error) {
        console.error('Error sending form data:', error);
      }

      // Determine crop type based on form data
      const { Nitrogen, Phosphorus, Potassium } = formData;
      // Check conditions and set cropInfo accordingly
      if (Nitrogen === '120' && Phosphorus === '40' && Potassium === '40') {
        setCropInfo("Rice");
      } else if (Nitrogen === '80' && Phosphorus === '40' && Potassium === '20'){
        setCropInfo("Maize");
      }
      // Add more conditions for other crop types

      // You can perform further actions with the form data here
    })();
  };
  
  return (
    <div>
    <div className="container">
      <h1 className="form-title">Soil Macronutrients</h1>
      <form id="registrationForm" onSubmit={handleSubmit}>
        <div className="main-user-info">
          <div className="user-input-box">
            <label htmlFor="Nitrogen">Nitrogen</label>
            
            <input
              type="float"
              id="N"
              name="N"
              placeholder="Enter Nitrogen values"
              value={formData.N}
              onChange={handleChange}
            />
          </div>
          <div className="user-input-box">
            <label htmlFor="Nitrogen">Phosphorus</label>
            <input
              type="float"
              id="P"
              name="P"
              placeholder="Enter Phosphorus values"
              value={formData.P}
              onChange={handleChange}
            />
          </div>
          <div className="user-input-box">
            <label htmlFor="Nitrogen">Potassium</label>
            <input
              type="float"
              id="K"
              name="K"
              placeholder="Enter Potassium values"
              value={formData.K}
              onChange={handleChange}
            />
          </div>
          <div className="user-input-box">
            <label htmlFor="Nitrogen">Temperature</label>
            <input
              type="float"
              id="temperature"
              name="temperature"
              placeholder="Enter Temperature values"
              value={formData.temperature}
              onChange={handleChange}
            />
          </div>
          <div className="user-input-box">
            <label htmlFor="Nitrogen">Humidity</label>
            <input
              type="float"
              id="humidity"
              name="humidity"
              placeholder="Enter Humidity values"
              value={formData.humidity}
              onChange={handleChange}
            />
          </div>
          <div className="user-input-box">
            <label htmlFor="Nitrogen">PH_Values</label>
            <input
              type="float"
              id="ph"
              name="ph"
              placeholder="Enter PH_Values values"
              value={formData.ph}
              onChange={handleChange}
            />
          </div>
          <div className="user-input-box">
            <label htmlFor="Nitrogen">Rainfall</label>
            <input
              type="float"
              id="rainfall"
              name="rainfall"
              placeholder="Enter Rainfall values"
              value={formData.rainfall}
              onChange={handleChange}
            />
          </div>
          
          {/* Add other input fields similarly */}
        </div>
        <div className="form-submit-btn">
          <input type="submit" value="Submit" />
        </div>
      </form>
      
      </div>
      <div className="container1">
      <div className="suitable">
        <h1 className="form-title">Suitable crop type : {cropInfo}</h1>
       
      </div>
      </div>
    </div>
  );
};

export default FormComponent;
