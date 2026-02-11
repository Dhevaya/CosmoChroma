import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div className="bg-white rounded-xl overflow-hidden border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      {/* Product Image */}
      <div className="w-full h-48 bg-gray-100 overflow-hidden">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover hover:scale-105 transition-transform"
          onError={(e) => {
            e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"%3E%3Crect fill="%23f3f4f6" width="200" height="200"/%3E%3Ctext x="50%25" y="50%25" font-family="Inter" font-size="14" text-anchor="middle" dominant-baseline="middle" fill="%239ca3af"%3EImage%3C/text%3E%3C/svg%3E';
          }}
        />
      </div>

      {/* Product Info */}
      <div className="p-4">
        <h4 className="font-bold text-gray-900 text-sm mb-1">{product.name}</h4>
        <p className="text-xs text-gray-600 mb-3 font-regular">{product.brand}</p>
        
        {/* Shade */}
        <p className="text-xs text-gray-700 mb-3 font-regular">
          <span className="font-bold">Shade:</span> {product.shade}
        </p>

        {/* Rating and Price */}
        <div className="flex justify-between items-center mb-3">
          <div className="flex items-center gap-1">
            <span className="text-yellow-400">★</span>
            <span className="text-sm font-bold text-gray-900">{product.rating}</span>
            <span className="text-xs text-gray-600 font-regular">({product.reviews_count})</span>
          </div>
          <span className="text-lg font-bold text-gray-900">₹{product.price_inr}</span>
        </div>

        {/* Color Match Distance */}
        {product.delta_e_distance !== undefined && (
          <div className="mb-3 p-2 bg-blue-50 rounded-lg border border-blue-100">
            <p className="text-xs text-gray-700 font-regular">
              Color Match: <span className="font-bold text-blue-600">{product.delta_e_distance.toFixed(1)}</span>
            </p>
          </div>
        )}

        {/* Buy Button */}
        <a
          href={product.buy_link}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full block text-center bg-gray-900 text-white py-2 rounded-lg font-bold text-sm hover:bg-gray-800 transition-colors"
        >
          View Product
        </a>
      </div>
    </div>
  );
};

export const ProductRecommendations = ({ recommendations }) => {
  const categories = {
    foundation_recommendations: { title: '💄 Foundation', icon: '🎨' },
    blush_recommendations: { title: '🌸 Blush', icon: '✨' },
    lipstick_recommendations: { title: '💋 Lipstick', icon: '❤️' },
    concealer_recommendations: { title: '🖌️ Concealer', icon: '🎯' },
    eyeshadow_recommendations: { title: '👁️ Eyeshadow', icon: '✨' },
  };

  return (
    <div className="spacing-generous">
      {Object.entries(categories).map(([key, { title }]) => (
        <div key={key}>
          <h3 className="text-2xl font-bold text-gray-900 mb-6">{title}</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {recommendations[key].map((product, idx) => (
              <ProductCard key={idx} product={product} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductRecommendations;
