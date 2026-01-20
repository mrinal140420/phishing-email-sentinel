import React, { useState, useEffect } from 'react'
import { getHistory, getStats } from '../services/api'

const History = () => {
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filterDomain, setFilterDomain] = useState('')
  const [filterVerdict, setFilterVerdict] = useState('')

  useEffect(() => {
    fetchHistory()
    fetchStats()
  }, [filterDomain, filterVerdict])

  const fetchHistory = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getHistory(filterDomain || null, filterVerdict || null)
      setHistory(data.results || [])
    } catch (err) {
      setError(err.error || 'Failed to fetch history')
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const data = await getStats()
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Scan History</h1>

      {stats && (
        <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f5f5f5' }}>
          <h3>Statistics</h3>
          <p>Total Scans: {stats.total_scans}</p>
          <p>Phishing Detected: {stats.phishing_detected}</p>
          <p>Benign: {stats.benign}</p>
        </div>
      )}

      <div style={{ marginBottom: '20px' }}>
        <label>
          Filter by Domain:
          <input
            type="text"
            value={filterDomain}
            onChange={(e) => setFilterDomain(e.target.value)}
            placeholder="domain.com"
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </label>
        <label style={{ marginLeft: '20px' }}>
          Filter by Verdict:
          <select
            value={filterVerdict}
            onChange={(e) => setFilterVerdict(e.target.value)}
            style={{ marginLeft: '10px', padding: '5px' }}
          >
            <option value="">All</option>
            <option value="PHISHING">Phishing</option>
            <option value="BENIGN">Benign</option>
          </select>
        </label>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {history.length > 0 ? (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f0f0f0' }}>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Scan ID</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Domain</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Verdict</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Confidence</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {history.map((scan) => (
              <tr key={scan.scan_id}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  <code>{scan.scan_id}</code>
                </td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{scan.sender_domain}</td>
                <td style={{
                  border: '1px solid #ddd',
                  padding: '8px',
                  color: scan.verdict === 'PHISHING' ? '#d32f2f' : '#388e3c'
                }}>
                  {scan.verdict}
                </td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  {(scan.confidence * 100).toFixed(1)}%
                </td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  {new Date(scan.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        !loading && <p>No scan history available</p>
      )}
    </div>
  )
}

export default History