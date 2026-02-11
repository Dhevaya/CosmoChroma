import React from 'react';

export const SkinToneResults = ({ skinAnalysis }) => {
  const { skin_tone_hex, skin_tone_rgb, undertone, season, skin_type, confidence_scores } = skinAnalysis;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Skin Tone Swatch */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Your Skin Tone</h3>
        
        <div className="flex items-end gap-6">
          <div
            className="w-32 h-32 rounded-xl shadow-sm border-2 border-gray-100"
            style={{ backgroundColor: skin_tone_hex }}
            title={skin_tone_hex}
          ></div>
          
          <div className="flex-1">
            <p className="text-sm text-gray-600 mb-2 font-regular">HEX Code</p>
            <p className="text-2xl font-bold text-gray-900 font-mono">{skin_tone_hex}</p>
            
            <p className="text-sm text-gray-600 mt-6 mb-2 font-regular">RGB Values</p>
            <p className="text-gray-700 font-regular">
              RGB({skin_tone_rgb.r}, {skin_tone_rgb.g}, {skin_tone_rgb.b})
            </p>
          </div>
        </div>
      </div>

      {/* Classification Results */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Analysis Results</h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center pb-4 border-b border-gray-200">
            <span className="text-gray-600 font-regular">Undertone</span>
            <span className="font-bold text-gray-900">{undertone.replace(/_/g, ' ').toUpperCase()}</span>
          </div>
          
          <div className="flex justify-between items-center pb-4 border-b border-gray-200">
            <span className="text-gray-600 font-regular">Season</span>
            <span className="font-bold text-gray-900">{season}</span>
          </div>
          
          <div className="flex justify-between items-center pb-4">
            <span className="text-gray-600 font-regular">Skin Type</span>
            <span className="font-bold text-gray-900">{skin_type.toUpperCase()}</span>
          </div>
        </div>

        {/* Confidence Scores */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-xs text-gray-600 font-bold mb-4">Confidence Scores</p>
          <div className="space-y-3">
            {Object.entries(confidence_scores).map(([key, value]) => (
              <div key={key}>
                <div className="flex justify-between mb-2">
                  <span className="text-xs text-gray-600 capitalize font-regular">{key}</span>
                  <span className="text-xs text-gray-700 font-bold">{value.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gray-900 rounded-full h-2 transition-all duration-500"
                    style={{ width: `${value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkinToneResults;
