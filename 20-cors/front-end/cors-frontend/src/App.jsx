import { useState, useEffect } from 'react'
// import heroImg from './assets/hero.png'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import './App.css'


function App() {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
    .then(response=>response.json())
    .then(json=> setData(json))
    .catch(err=>console.error("Error while fetching data : ", err))
  }, [])

  return (
    <div>
      <h1 style={{ color: "lime" }}>Hello Vite! </h1>
      <p> This is just a simple React app for testing CORS. </p>
      <p>CORS is working properly...</p>
      {
        data ? (
          <>
          
          <p>Message: {data.Backend} </p>
          <p>Message: {data.message} </p>
          </>
        ) : (
          <p>Loading data from backend ...</p>
        )
      }
    </div>
  )
}

export default App