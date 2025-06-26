import { useState, useEffect } from 'react';

export const useAlphaGenome = () => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableVariants, setAvailableVariants] = useState([]);

  useEffect(() => {
    fetchAvailableVariants();
  }, []);

  const fetchAvailableVariants = async () => {
    try {
      const response = await fetch('http:///localhost:8000/api/v1/variants/');
      if (!response.ok) throw new Error('Failed to fetch variants');
      const data = await response.json();
      setAvailableVariants(data.variants);
    } catch (err) {
      setError(err.message);
    }
  };

  const predictVariant = async (variantName) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http:///localhost:8000/api/v1/variants/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ variant_name: variantName })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }
      
      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    prediction,
    loading,
    error,
    availableVariants,
    predictVariant,
    clearError: () => setError(null)
  };
};
