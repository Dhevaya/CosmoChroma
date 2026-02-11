import { create } from 'zustand';

export const useAnalysisStore = create((set) => ({
  analysisResult: null,
  loading: false,
  error: null,
  
  setAnalysisResult: (result) => set({ analysisResult: result, error: null }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearAnalysis: () => set({ analysisResult: null, error: null }),
  resetStore: () => set({ analysisResult: null, loading: false, error: null }),
}));
