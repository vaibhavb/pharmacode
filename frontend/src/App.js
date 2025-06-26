import React from 'react';
import VariantSelector from './components/variant/VariantSelector';
import MolecularEffects from './components/prediction/MolecularEffects';
import { useAlphaGenome } from './hooks/useAlphaGenome';
import './styles/globals.css';

function App() {
  const { prediction, loading, error, availableVariants, predictVariant } = useAlphaGenome();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">PharmaCode</h1>
          <p className="text-gray-600">AI-powered pharmacogenomics learning</p>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-6 px-4">
        <VariantSelector 
          variants={availableVariants}
          onVariantSelect={predictVariant}
          loading={loading}
        />
        
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded">
            <p className="text-red-700">{error}</p>
          </div>
        )}
        
        {prediction && <MolecularEffects prediction={prediction} />}
      </main>
    </div>
  );
}

export default App;
