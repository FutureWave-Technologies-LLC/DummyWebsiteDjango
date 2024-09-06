import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function clickMe() {
  alert("Database goes here!");
}

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <button onClick={clickMe}>Button</button>
      </div>
    </>
  )
}

export default App
