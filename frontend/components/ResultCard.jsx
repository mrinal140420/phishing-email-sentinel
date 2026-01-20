import React from 'react'

const ResultCard = ({ result }) => {
  if (!result) return null

  const verdictColor = result.verdict === 'PHISHING' ? '#d32f2f' : '#388e3c'
  const verdictBg = result.verdict === 'PHISHING' ? '#ffebee' : '#e8f5e9'

  return (
    <div className="result-card" style={{ backgroundColor: verdictBg, padding: '20px', borderRadius: '8px' }}>
      <h2>Scan Result</h2>

      <div style={{ marginBottom: '10px' }}>
        <strong>Verdict: </strong>
        <span style={{ color: verdictColor, fontSize: '18px', fontWeight: 'bold' }}>
          {result.verdict}
        </span>
      </div>

      <div style={{ marginBottom: '10px' }}>
        <strong>Confidence: </strong>
        {(result.confidence * 100).toFixed(1)}%
      </div>

      <div style={{ marginBottom: '10px' }}>
        <strong>Scan ID: </strong>
        <code>{result.scan_id}</code>
      </div>

      {result.signals && (
        <div>
          <strong>Signals:</strong>
          <ul>
            {result.signals.rules && result.signals.rules.length > 0 && (
              <li>Rules triggered: {result.signals.rules.join(', ')}</li>
            )}
            {result.signals.ml_probability !== undefined && (
              <li>ML Probability: {(result.signals.ml_probability * 100).toFixed(1)}%</li>
            )}
          </ul>
        </div>
      )}
    </div>
  )
}

export default ResultCard