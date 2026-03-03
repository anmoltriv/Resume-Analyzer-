import { useState } from 'react'

export default function ReviewBox() {
  const [feedback, setFeedback] = useState('')
  const [sent, setSent] = useState(false)

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!feedback.trim()) {
      return
    }

    console.log('Resume Analyzer Feedback:', feedback.trim())
    setFeedback('')
    setSent(true)
  }

  return (
    <section className="review-box">
      <h2>How did this analysis feel?</h2>
      <form onSubmit={handleSubmit} className="review-form">
        <textarea
          placeholder="Share feedback about accuracy or suggestions..."
          value={feedback}
          onChange={(event) => {
            setFeedback(event.target.value)
            if (sent) {
              setSent(false)
            }
          }}
          rows={4}
        />
        <button type="submit" className="secondary-btn">
          Send Feedback
        </button>
      </form>
      {sent && <p className="success-text">Thanks for the feedback.</p>}
    </section>
  )
}
