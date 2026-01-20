import React, { useState } from 'react'
import { scanEmailFile } from '../services/api'

const FileUploader = ({ onScanComplete }) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    setLoading(true)
    setError(null)

    try {
      const result = await scanEmailFile(file)
      onScanComplete(result)
    } catch (err) {
      setError(err.error || 'Failed to scan file')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="file-uploader">
      <h3>Upload Email File</h3>
      <input
        type="file"
        accept=".eml,.msg"
        onChange={handleFileUpload}
        disabled={loading}
      />
      {loading && <p>Scanning...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
    </div>
  )
}

export default FileUploader