import axios from 'axios'

/**
 * Single source of truth for API base URL
 */
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  'https://pes-backend.onrender.com'

/**
 * Axios instance
 */
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 15000
})

/**
 * Normalize API errors
 */
const handleError = (error, fallback) => {
  throw error.response?.data || fallback
}

/* ============================
   Scan APIs
   ============================ */

/**
 * Scan raw email text
 * @param {string} rawEmail
 */
export const scanEmail = async (rawEmail) => {
  try {
    const res = await api.post('/api/scan', {
      raw_email: rawEmail
    })
    return res.data
  } catch (err) {
    handleError(err, { error: 'Failed to scan email' })
  }
}

/**
 * Legacy compatibility (old /scan contract)
 * @deprecated
 */
export const scanEmailLegacy = async (payload) => {
  try {
    const res = await api.post('/scan', payload)
    return res.data
  } catch (err) {
    handleError(err, { error: 'Failed to scan email (legacy)' })
  }
}

/**
 * Scan uploaded email file
 */
export const scanEmailFile = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const res = await api.post('/api/scan/file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return res.data
  } catch (err) {
    handleError(err, { error: 'Failed to scan file' })
  }
}

/* ============================
   History & Analytics
   ============================ */

/**
 * Fetch scan history
 */
export const getHistory = async ({
  domain = null,
  verdict = null,
  limit = 100,
  offset = 0
} = {}) => {
  try {
    const params = new URLSearchParams()
    if (domain) params.append('domain', domain)
    if (verdict) params.append('verdict', verdict)
    params.append('limit', limit)
    params.append('offset', offset)

    const res = await api.get(`/api/history?${params.toString()}`)
    return res.data
  } catch (err) {
    handleError(err, { error: 'Failed to fetch history' })
  }
}

/**
 * Fetch aggregate stats
 */
export const getStats = async () => {
  try {
    const res = await api.get('/api/history/stats')
    return res.data
  } catch (err) {
    handleError(err, { error: 'Failed to fetch stats' })
  }
}

export default api
