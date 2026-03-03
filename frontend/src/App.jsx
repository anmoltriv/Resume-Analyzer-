import { useState } from 'react'
import UploadForm from './components/UploadForm'
import ResultsPanel from './components/ResultsPanel'
import ReviewBox from './components/ReviewBox'

const API_URL = 'http://localhost:8000/analyze'

export default function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async ({ resumeFile, jdType, jdFile, jdUrl }) => {
    setError('')
    setLoading(true)
    setResults(null)

    const formData = new FormData()
    formData.append('resume_pdf', resumeFile)
    formData.append('jd_type', jdType)

    if (jdType === 'url') {
      formData.append('jd_url', jdUrl)
    } else {
      formData.append('jd_pdf', jdFile)
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to analyze resume right now.')
      }

      setResults(data)
    } catch (submitError) {
      setError(submitError.message || 'Unexpected error while analyzing the documents.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>Resume Analyzer — Hybrid ML Matching Engine</h1>
        <p>Deterministic IR + ML scoring with explainable insights</p>
      </header>

      <UploadForm onSubmit={handleAnalyze} loading={loading} />

      {error && <div className="error-banner">{error}</div>}

      {results && <ResultsPanel data={results} />}

      <ReviewBox />
    </main>
  )
}
