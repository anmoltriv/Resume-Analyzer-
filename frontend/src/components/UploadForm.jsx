import { useEffect, useState } from 'react'

const JD_OPTIONS = [
  { value: 'pdf', label: 'PDF' },
  { value: 'image_pdf', label: 'Image-based PDF (OCR)' },
  { value: 'url', label: 'URL' },
]

export default function UploadForm({ onSubmit, loading }) {
  const [resumeFile, setResumeFile] = useState(null)
  const [jdType, setJdType] = useState('pdf')
  const [jdFile, setJdFile] = useState(null)
  const [jdUrl, setJdUrl] = useState('')
  const [formError, setFormError] = useState('')

  useEffect(() => {
    setFormError('')
    setJdFile(null)
    setJdUrl('')
  }, [jdType])

  const handleSubmit = (event) => {
    event.preventDefault()
    setFormError('')

    if (!resumeFile) {
      setFormError('Please upload your resume PDF before continuing.')
      return
    }

    if (jdType === 'url' && !jdUrl.trim()) {
      setFormError('Please provide a job description URL.')
      return
    }

    if (jdType !== 'url' && !jdFile) {
      setFormError('Please upload a job description PDF for the selected type.')
      return
    }

    onSubmit({ resumeFile, jdType, jdFile, jdUrl: jdUrl.trim() })
  }

  return (
    <section className="card">
      <h2>Analyze a Resume Against a Job Description</h2>
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Upload Your Resume (PDF)
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(event) => setResumeFile(event.target.files?.[0] || null)}
          />
        </label>
        {resumeFile && <p className="file-name">Selected: {resumeFile.name}</p>}

        <label>
          Job Description Type
          <select value={jdType} onChange={(event) => setJdType(event.target.value)}>
            {JD_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        {jdType === 'url' ? (
          <label>
            Job Description URL
            <input
              type="url"
              placeholder="Paste Job Description URL"
              value={jdUrl}
              onChange={(event) => setJdUrl(event.target.value)}
            />
          </label>
        ) : (
          <label>
            Upload Job Description (PDF)
            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => setJdFile(event.target.files?.[0] || null)}
            />
          </label>
        )}

        {jdFile && jdType !== 'url' && <p className="file-name">Selected: {jdFile.name}</p>}

        {formError && <div className="inline-error">{formError}</div>}

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? (
            <span className="btn-loading">
              <span className="spinner" aria-hidden="true" />
              Analyzing...
            </span>
          ) : (
            'Analyze Match'
          )}
        </button>
      </form>
    </section>
  )
}
