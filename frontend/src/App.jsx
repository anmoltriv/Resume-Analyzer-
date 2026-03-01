import { useState } from 'react'

const API_URL = 'http://localhost:8000/evaluate'

export default function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jdFile, setJdFile] = useState(null)
  const [score, setScore] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setScore(null)

    if (!resumeFile || !jdFile) {
      setError('Please upload both PDFs before submitting.')
      return
    }

    const formData = new FormData()
    formData.append('resume_pdf', resumeFile)
    formData.append('jd_pdf', jdFile)

    try {
      setLoading(true)
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to evaluate documents.')
      }

      setScore(data.score)
    } catch (submitError) {
      setError(submitError.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <section className="card">
        <h1>Resume Analyzer</h1>
        <p className="subtitle">Upload your Resume and Job Description PDFs to get a fit score.</p>

        <form onSubmit={handleSubmit} className="form">
          <label>
            Resume PDF
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => setResumeFile(event.target.files?.[0] || null)}
            />
          </label>

          <label>
            Job Description PDF
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => setJdFile(event.target.files?.[0] || null)}
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Evaluating...' : 'Get Score'}
          </button>
        </form>

        {loading && (
          <div className="spinner-wrap">
            <div className="spinner" aria-label="loading" />
          </div>
        )}

        {error && <p className="error">{error}</p>}

        {score !== null && !loading && (
          <div className="score-card">
            <p className="score-label">Match Score</p>
            <p className="score-value">{score}/10</p>
          </div>
        )}
      </section>
    </main>
  )
}
