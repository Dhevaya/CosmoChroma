import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import './UploadForm.css';

export const UploadForm = ({ onUpload, isLoading }) => {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (file.type.startsWith('image/')) {
        onUpload(file);
      } else {
        alert('Please upload an image file');
      }
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    disabled: isLoading
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 bg-white hover:border-gray-400 hover:bg-gray-50'
        } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <div className="text-5xl">📸</div>
          
          {isDragActive ? (
            <div>
              <p className="text-xl font-bold text-blue-600">Drop your selfie here!</p>
            </div>
          ) : (
            <div>
              <p className="text-xl font-bold text-gray-900">
                Drag your selfie here or click to select
              </p>
              <p className="text-gray-600 mt-2 font-regular">
                Supported formats: JPG, PNG (max 10MB)
              </p>
            </div>
          )}
          
          {isLoading && (
            <div className="mt-4">
              <p className="text-blue-600 font-semibold">Analyzing your image...</p>
              <div className="mt-2 w-8 h-8 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin mx-auto"></div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadForm;
