import { useState, useCallback } from 'react';
import { analysisService } from '../services/api';

export const useImageAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const analyze = useCallback(async (file) => {
    setLoading(true);
    setError(null);

    try {
      const data = await analysisService.uploadAndAnalyze(file);
      setResult(data);
      return data;
    } catch (err) {
      console.error('Analysis hook error:', err);
      const errorMessage = typeof err === 'string' 
        ? err 
        : (err?.message || err?.detail || 'Analysis failed. Please try again.');
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, error, result, analyze };
};
