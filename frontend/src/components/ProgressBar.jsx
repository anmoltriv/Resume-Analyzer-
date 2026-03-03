export default function ProgressBar({ label, value, max }) {
  const safeValue = Number.isFinite(value) ? Math.max(0, Math.min(value, max)) : 0
  const percentage = (safeValue / max) * 100

  return (
    <div className="progress-item">
      <div className="progress-header">
        <span>{label}</span>
        <strong>
          {safeValue.toFixed(1)} / {max}
        </strong>
      </div>
      <div className="progress-track" role="progressbar" aria-valuenow={safeValue} aria-valuemin={0} aria-valuemax={max}>
        <div className="progress-fill" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  )
}
