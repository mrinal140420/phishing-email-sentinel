import React, { useState } from 'react'
import FileUploader from '../components/FileUploader'
import ResultCard from '../components/ResultCard'
import { scanEmail } from '../services/api'

const Upload = () => {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [emailText, setEmailText] = useState('')

  const handleScanEmail = async () => {
    if (!emailText.trim()) {
      setError('Please enter email content')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const scanResult = await scanEmail(emailText)
      setResult(scanResult)
    } catch (err) {
      setError(err.error || 'Failed to scan email')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Phishing Email Sentinel</h1>

      <div style={{ marginBottom: '20px' }}>
        <h3>Paste Email Content</h3>
        <textarea
          value={emailText}
          onChange={(e) => setEmailText(e.target.value)}
          placeholder="Paste raw RFC 822 email content here..."
          rows="10"
          style={{ width: '100%', padding: '10px', fontFamily: 'monospace' }}
        />
        <button
          onClick={handleScanEmail}
          disabled={loading}
          style={{ marginTop: '10px', padding: '10px 20px' }}
        >
          {loading ? 'Scanning...' : 'Scan Email'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {result && <ResultCard result={result} />}

      <hr />

      <FileUploader onScanComplete={setResult} />
    </div>
  )
}

export default Upload