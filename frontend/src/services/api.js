import axios from 'axios'

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const scanEmail = async (rawEmail) => {
  try {
    const response = await api.post('/api/scan', { raw_email: rawEmail })
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Failed to scan email' }
  }
}

export const scanEmailFile = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/scan/file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Failed to scan file' }
  }
}

export const getHistory = async (domain = null, verdict = null, limit = 100, offset = 0) => {
  try {
    const params = new URLSearchParams()
    if (domain) params.append('domain', domain)
    if (verdict) params.append('verdict', verdict)
    params.append('limit', limit)
    params.append('offset', offset)

    const response = await api.get(`/api/history?${params}`)
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch history' }
  }
}

export const getStats = async () => {
  try {
    const response = await api.get('/api/history/stats')
    return response.data
  } catch (error) {
    throw error.response?.data || { error: 'Failed to fetch stats' }
  }
}

export default api