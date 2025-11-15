const InsightsDisplay = ({ document }) => {
  if (!document || !document.insights) {
    return <div>No insights available</div>;
  }

  const { insights } = document;

  return (
    <div className="insights-display">
      <h2>Document Insights</h2>

      {/* Summary */}
      {insights.summary && (
        <div className="insight-section">
          <h3>📝 Summary</h3>
          <p className="insight-content">{insights.summary}</p>
        </div>
      )}

      {/* Key Points */}
      {insights.key_points && insights.key_points.length > 0 && (
        <div className="insight-section">
          <h3>🔑 Key Points</h3>
          <ul className="key-points-list">
            {insights.key_points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Tables */}
      {insights.tables && insights.tables.length > 0 && (
        <div className="insight-section">
          <h3>📊 Extracted Tables</h3>
          {insights.tables.map((table, index) => (
            <div key={index} className="table-container">
              <table className="extracted-table">
                <thead>
                  <tr>
                    {table.headers?.map((header, hIndex) => (
                      <th key={hIndex}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {table.rows?.map((row, rIndex) => (
                    <tr key={rIndex}>
                      {row.map((cell, cIndex) => (
                        <td key={cIndex}>{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      )}

      {/* Sentiment/Classification */}
      {(insights.sentiment || insights.category) && (
        <div className="insight-section">
          <h3>🏷️ Classification</h3>
          {insights.sentiment && (
            <p>
              <strong>Sentiment:</strong>{' '}
              <span className={`sentiment-badge sentiment-${insights.sentiment.toLowerCase()}`}>
                {insights.sentiment}
              </span>
            </p>
          )}
          {insights.category && (
            <p>
              <strong>Category:</strong> {insights.category}
            </p>
          )}
        </div>
      )}

      {/* Keywords */}
      {insights.keywords && insights.keywords.length > 0 && (
        <div className="insight-section">
          <h3>🏷️ Keywords</h3>
          <div className="keywords-container">
            {insights.keywords.map((keyword, index) => (
              <span key={index} className="keyword-tag">
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default InsightsDisplay;

