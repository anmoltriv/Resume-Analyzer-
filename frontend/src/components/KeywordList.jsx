export default function KeywordList({ topKeywords = [], missingKeywords = [] }) {
  return (
    <section className="results-card keyword-grid">
      <div>
        <h3>Top Matching Keywords</h3>
        <div className="tag-wrap">
          {topKeywords.length > 0 ? (
            topKeywords.map((keyword) => (
              <span className="tag tag-positive" key={keyword}>
                {keyword}
              </span>
            ))
          ) : (
            <p className="muted-text">No matching keywords available.</p>
          )}
        </div>
      </div>

      <div>
        <h3>Missing Critical Keywords</h3>
        <div className="tag-wrap">
          {missingKeywords.length > 0 ? (
            missingKeywords.map((keyword) => (
              <span className="tag tag-negative" key={keyword}>
                {keyword}
              </span>
            ))
          ) : (
            <p className="muted-text">No missing keywords identified.</p>
          )}
        </div>
      </div>
    </section>
  )
}
