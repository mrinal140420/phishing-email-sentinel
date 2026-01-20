import React, { useState } from 'react'
import Upload from './pages/Upload'
import History from './pages/History'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('upload')

  return (
    <div className="app">
      <nav style={{ backgroundColor: '#1976d2', padding: '10px', color: 'white' }}>
        <button
          onClick={() => setCurrentPage('upload')}
          style={{
            background: currentPage === 'upload' ? '#1565c0' : 'transparent',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            marginRight: '10px'
          }}
        >
          Upload & Scan
        </button>
        <button
          onClick={() => setCurrentPage('history')}
          style={{
            background: currentPage === 'history' ? '#1565c0' : 'transparent',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer'
          }}
        >
          History
        </button>
      </nav>

      <main>
        {currentPage === 'upload' && <Upload />}
        {currentPage === 'history' && <History />}
      </main>
    </div>
  )
}

export default App