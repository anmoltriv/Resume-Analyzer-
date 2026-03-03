import ProgressBar from './ProgressBar'

export default function ScoreBreakdown({ structureScore, cosineScore, geminiScore }) {
  return (
    <section className="results-card">
      <h3>Score Breakdown</h3>
      <ProgressBar label="Structure Score" value={structureScore} max={2} />
      <ProgressBar label="Cosine Score" value={cosineScore} max={4} />
      <ProgressBar label="Gemini Score" value={geminiScore} max={4} />
    </section>
  )
}
