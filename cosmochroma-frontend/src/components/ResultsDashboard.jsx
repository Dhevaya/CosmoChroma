import React from 'react';

export const ResultsDashboard = ({ results, onNewAnalysis, onDownload }) => {
  return (
    <div className="w-full spacing-generous">
      {/* Header with Actions */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6 card">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Your Analysis Results</h2>
          <p className="text-gray-600 mt-2 font-regular">
            Generated: {new Date(results.analysis_timestamp).toLocaleString()}
          </p>
        </div>
        
        <div className="flex gap-3 flex-wrap w-full sm:w-auto">
          <button
            onClick={onNewAnalysis}
            className="btn-primary flex-1 sm:flex-none"
          >
            📸 New Analysis
          </button>
          <button
            onClick={onDownload}
            className="btn-secondary flex-1 sm:flex-none"
          >
            📥 Download Results
          </button>
        </div>
      </div>

      {/* Results Content */}
      <div id="results-content" className="spacing-medium">
        {/* Skin Tone Section */}
        <section className="scroll-mt-20" id="skin-tone">
          {/* SkinToneResults component will be inserted here by parent */}
        </section>

        {/* Product Recommendations Section */}
        <section className="scroll-mt-20" id="products">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">
            💄 Makeup Recommendations
          </h2>
          {/* ProductRecommendations component will be inserted here by parent */}
        </section>

        {/* Skincare Routine Section */}
        <section className="scroll-mt-20" id="routine">
          {/* SkincareRoutines component will be inserted here by parent */}
        </section>
      </div>
    </div>
  );
};

export default ResultsDashboard;
