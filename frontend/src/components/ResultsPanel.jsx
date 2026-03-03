import ScoreBreakdown from './ScoreBreakdown'
import KeywordList from './KeywordList'

const SECTION_LABELS = {
  skills: 'Skills',
  experience: 'Experience',
  education: 'Education',
}

export default function ResultsPanel({ data }) {
  const {
    overall_score: overallScore,
    best_matching_role: bestMatchingRole,
    structure_score: structureScore,
    cosine_score: cosineScore,
    gemini_score: geminiScore,
    top_keywords: topKeywords,
    missing_keywords: missingKeywords,
    section_scores: sectionScores,
  } = data

  const sectionItems = Object.entries(sectionScores || {})

  return (
    <section className="results-panel">
      <div className="results-header">
        <div className="score-badge">
          <span>{overallScore}</span>
          <small>/100</small>
        </div>
        <div>
          <p className="muted-label">Best Matching Role</p>
          <h2>{bestMatchingRole}</h2>
        </div>
      </div>

      <ScoreBreakdown
        structureScore={structureScore}
        cosineScore={cosineScore}
        geminiScore={geminiScore}
      />

      <section className="results-card">
        <h3>Section-wise Match</h3>
        <div className="section-grid">
          {sectionItems.map(([sectionName, sectionValue]) => (
            <article className="mini-card" key={sectionName}>
              <p>{SECTION_LABELS[sectionName] || sectionName}</p>
              <strong>{sectionValue}%</strong>
            </article>
          ))}
        </div>
      </section>

      <KeywordList topKeywords={topKeywords} missingKeywords={missingKeywords} />
    </section>
  )
}
