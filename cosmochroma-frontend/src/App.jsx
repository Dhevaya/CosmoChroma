import React, { useState, useEffect } from 'react';
import { useImageAnalysis } from './hooks/useImageAnalysis';
import { useAnalysisStore } from './store/analysisStore';
import UploadForm from './components/UploadForm';
import SkinToneResults from './components/SkinToneResults';
import ProductRecommendations from './components/ProductRecommendations';
import SkincareRoutines from './components/SkincareRoutine';
import ResultsDashboard from './components/ResultsDashboard';
import ProductGallery from './components/ProductGallery';
import { analysisService } from './services/api';
import './styles/globals.css';

function App() {
  const { loading, error, result, analyze } = useImageAnalysis();
  const { analysisResult, setAnalysisResult, setLoading, setError } = useAnalysisStore();
  const [currentPage, setCurrentPage] = useState('upload');

  // Check API health on mount (silently)
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await analysisService.getHealth();
      } catch (err) {
        // Silent - health check is optional, API will be available when needed
        console.log('Health check pending...');
      }
    };
    
    // Add delay to ensure server is ready
    const timer = setTimeout(checkAPI, 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleFileUpload = async (file) => {
    setLoading(true);
    try {
      const results = await analyze(file);
      setAnalysisResult(results);
      setCurrentPage('results');
      setError(null);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setCurrentPage('upload');
    setAnalysisResult(null);
    setError(null);
  };

  const handleDownloadResults = () => {
    if (!analysisResult) return;

    const resultsText = `
CosmoChroma Analysis Results
============================

Skin Tone Analysis:
- Hex Color: ${analysisResult.skin_analysis.skin_tone_hex}
- RGB: RGB(${analysisResult.skin_analysis.skin_tone_rgb.r}, ${analysisResult.skin_analysis.skin_tone_rgb.g}, ${analysisResult.skin_analysis.skin_tone_rgb.b})
- Undertone: ${analysisResult.skin_analysis.undertone}
- Season: ${analysisResult.skin_analysis.season}
- Skin Type: ${analysisResult.skin_analysis.skin_type}

Generated: ${new Date(analysisResult.analysis_timestamp).toLocaleString()}
    `;

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(resultsText));
    element.setAttribute('download', 'cosmochroma-results.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="container-main">
          <div className="py-6 flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 flex items-center gap-3">
                ✨ CosmoChroma
              </h1>
              <p className="text-gray-600 mt-2 font-regular">
                AI-Powered Skin Analysis & Beauty Recommendations
              </p>
            </div>
            <button
              onClick={() => setCurrentPage(currentPage === 'gallery' ? 'upload' : 'gallery')}
              className="px-6 py-2 bg-gray-900 text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors"
            >
              {currentPage === 'gallery' ? '← Back to Analyzer' : 'Browse Products →'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg container-main">
            ❌ {error}
          </div>
        )}

        {/* Product Gallery Page */}
        {currentPage === 'gallery' && (
          <ProductGallery />
        )}

        {/* Upload & Results Pages */}
        {currentPage !== 'gallery' && (
          <div className="container-main">

        {/* Upload Page */}
        {currentPage === 'upload' && (
          <div className="py-16">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Upload Your Selfie
              </h2>
              <p className="text-gray-600 text-lg max-w-2xl mx-auto">
                Get instant analysis of your skin tone, undertone, and personalized recommendations
              </p>
            </div>
            <UploadForm onUpload={handleFileUpload} isLoading={loading} />
          </div>
        )}

        {/* Results Page */}
        {currentPage === 'results' && analysisResult && (
          <div className="py-12 spacing-generous">
            <ResultsDashboard
              results={analysisResult}
              onNewAnalysis={handleNewAnalysis}
              onDownload={handleDownloadResults}
            />

            {/* Skin Tone Results */}
            <section className="spacing-medium">
              <h2 className="text-3xl font-bold text-gray-900">🎨 Skin Tone Analysis</h2>
              <SkinToneResults skinAnalysis={analysisResult.skin_analysis} />
            </section>

            {/* Product Recommendations */}
            <section className="spacing-medium">
              <h2 className="text-3xl font-bold text-gray-900">💄 Makeup Recommendations</h2>
              <ProductRecommendations recommendations={analysisResult} />
            </section>

            {/* Skincare Routine */}
            <section className="spacing-medium">
              <h2 className="text-3xl font-bold text-gray-900">🧴 Personalized Skincare Routine</h2>
              <SkincareRoutines
                morningRoutine={analysisResult.morning_routine}
                eveningRoutine={analysisResult.evening_routine}
                weeklyRoutine={analysisResult.weekly_routine}
              />
            </section>
          </div>
        )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container-main py-8 text-center text-gray-600">
          <p>© 2024 CosmoChroma. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
