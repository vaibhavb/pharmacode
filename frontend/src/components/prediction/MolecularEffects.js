import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const MolecularEffects = ({ prediction }) => {
  const effectsData = [
    { 
      name: 'Gene Expression', 
      value: Math.abs(prediction.molecular_effects.gene_expression_change) 
    },
    { 
      name: 'Chromatin Access', 
      value: Math.abs(prediction.molecular_effects.chromatin_accessibility_change) 
    }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white border rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-2">{prediction.variant_name}</h2>
        
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">Predicted Molecular Effects</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={effectsData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis label={{ value: '% Change', angle: -90, position: 'insideLeft' }} />
                  <Tooltip formatter={(value) => [`${value}%`, 'Change']} />
                  <Bar dataKey="value" fill="#EF4444" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div>
              <div className="space-y-2 text-sm">
                <div><strong>Gene Expression:</strong> {prediction.molecular_effects.gene_expression_change}%</div>
                <div><strong>Splicing Impact:</strong> {prediction.molecular_effects.splicing_impact}</div>
                <div><strong>Binding Sites Lost:</strong> {prediction.molecular_effects.binding_sites_lost}</div>
                <div><strong>Confidence:</strong> {prediction.prediction_confidence.expression}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MolecularEffects;
