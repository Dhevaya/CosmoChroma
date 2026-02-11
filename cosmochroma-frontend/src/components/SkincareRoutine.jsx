import React, { useState } from 'react';

export const SkincareRoutine = ({ routine, routineType }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const routineIcons = {
    morning: '🌅',
    evening: '🌙',
    weekly: '📅'
  };

  const routineLabels = {
    morning: 'Morning Routine',
    evening: 'Evening Routine',
    weekly: 'Weekly Routine'
  };

  return (
    <div className="card">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between hover:bg-gray-50 p-4 -m-4 rounded-lg transition-colors"
      >
        <div className="flex items-center gap-4">
          <span className="text-3xl">{routineIcons[routineType]}</span>
          <div>
            <h3 className="text-xl font-bold text-gray-900 text-left">
              {routineLabels[routineType]}
            </h3>
            <p className="text-sm text-gray-600 text-left font-regular">
              {routine.total_duration_minutes} minutes
            </p>
          </div>
        </div>
        <div className={`text-2xl transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
          ▼
        </div>
      </button>

      {isExpanded && (
        <div className="mt-6 pt-6 border-t border-gray-200 spacing-medium">
          {routine.steps.map((step) => (
            <div key={step.order} className="flex gap-4">
              {/* Step Number */}
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-sm">
                  {step.order}
                </div>
              </div>

              {/* Step Content */}
              <div className="flex-1">
                <h4 className="font-bold text-gray-900 text-lg">{step.step_name}</h4>
                <p className="text-gray-600 text-sm mt-2 font-regular">{step.description}</p>
                
                {/* Duration */}
                <p className="text-xs text-gray-500 mt-3 font-regular">
                  ⏱️ {step.duration_minutes} minute{step.duration_minutes > 1 ? 's' : ''}
                </p>

                {/* Product Recommendations */}
                {step.product_recommendations && step.product_recommendations.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {step.product_recommendations.map((product, idx) => (
                      <span
                        key={idx}
                        className="inline-block bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs font-bold border border-blue-200"
                      >
                        💡 {product}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export const SkincareRoutines = ({ morningRoutine, eveningRoutine, weeklyRoutine }) => {
  return (
    <div className="spacing-generous">
      <SkincareRoutine routine={morningRoutine} routineType="morning" />
      <SkincareRoutine routine={eveningRoutine} routineType="evening" />
      <SkincareRoutine routine={weeklyRoutine} routineType="weekly" />
    </div>
  );
};

export default SkincareRoutines;
