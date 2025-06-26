import React from 'react';

const VariantSelector = ({ variants, onVariantSelect, loading }) => {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-3">Select a Pharmacogenomic Variant</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {variants.map((variant) => (
          <button
            key={variant}
            onClick={() => onVariantSelect(variant)}
            disabled={loading}
            className="p-3 text-left border rounded-lg transition-colors border-gray-200 hover:border-gray-300 disabled:opacity-50"
          >
            <div className="font-medium text-sm">{variant}</div>
          </button>
        ))}
      </div>
      {loading && (
        <div className="mt-4 text-center">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="ml-2">Getting predictions...</span>
        </div>
      )}
    </div>
  );
};

export default VariantSelector;
