import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductGallery = () => {
  const [products, setProducts] = useState({
    foundation: [],
    concealer: [],
    blush: [],
    eyeshadow: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('foundation');

  useEffect(() => {
    fetchAllProducts();
  }, []);

  const fetchAllProducts = async () => {
    try {
      setLoading(true);
      
      // Load products data from mock data
      const allProducts = {
        foundation: [
          {
            id: 1,
            name: "Maybelline Fit Me Liquid Foundation",
            brand: "Maybelline",
            price_inr: 599,
            rating: 4.2,
            reviews_count: 2150,
            image_url: "https://images.nykaa.com/maybelline-foundation.jpg",
            shades: [
              { name: "128 Warm Nude", hex: "#F8C8B4" },
              { name: "130 Buff Beige", hex: "#E6BEAA" },
              { name: "220 Natural Beige", hex: "#D2AA96" },
              { name: "330 Toffee", hex: "#B48C6E" },
              { name: "380 Espresso", hex: "#8C6450" }
            ]
          },
          {
            id: 10,
            name: "Bobbi Brown Foundation Stick",
            brand: "Bobbi Brown",
            price_inr: 3500,
            rating: 4.6,
            reviews_count: 1950,
            image_url: "https://images.nykaa.com/bobbi-foundation.jpg",
            shades: [
              { name: "Porcelain", hex: "#FADCC8" },
              { name: "Warm Natural", hex: "#E6C8B4" },
              { name: "Beige", hex: "#D2B4A0" },
              { name: "Golden", hex: "#B49682" },
              { name: "Deep Golden", hex: "#8C6E5A" }
            ]
          }
        ],
        concealer: [
          {
            id: 7,
            name: "Lakme Absolute Blur Perfect Concealer",
            brand: "Lakme",
            price_inr: 549,
            rating: 4.3,
            reviews_count: 1680,
            image_url: "https://images.nykaa.com/lakme-concealer.jpg",
            shades: [
              { name: "Fair", hex: "#F0D2BE" },
              { name: "Light Medium", hex: "#DCBEAA" },
              { name: "Medium", hex: "#C8AA96" },
              { name: "Deep", hex: "#A0826E" },
              { name: "Dark Deep", hex: "#826450" }
            ]
          }
        ],
        blush: [
          {
            id: 5,
            name: "Mars Face Palette Blush & Contour",
            brand: "Mars",
            price_inr: 399,
            rating: 4.1,
            reviews_count: 1200,
            image_url: "https://images.nykaa.com/mars-blush.jpg",
            shades: [
              { name: "Warm Peach", hex: "#F89678" },
              { name: "Rose Gold", hex: "#E68282" },
              { name: "Coral", hex: "#FA8C64" },
              { name: "Bronze", hex: "#B47850" },
              { name: "Berry", hex: "#B46478" }
            ]
          }
        ],
        eyeshadow: [
          {
            id: 8,
            name: "Wet n Wild MegaEyes Eyeshadow Palette",
            brand: "Wet n Wild",
            price_inr: 799,
            rating: 4.4,
            reviews_count: 2100,
            image_url: "https://images.nykaa.com/wetnwild-eyeshadow.jpg",
            shades: [
              { name: "Rose Gold", hex: "#F0B4A0" },
              { name: "Bronze", hex: "#C88C64" },
              { name: "Plum", hex: "#966482" },
              { name: "Brown", hex: "#8C6446" },
              { name: "Gold", hex: "#DCB464" }
            ]
          }
        ]
      };

      setProducts(allProducts);
      setError(null);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const categoryLabels = {
    foundation: 'Foundation',
    concealer: 'Concealer',
    blush: 'Blush',
    eyeshadow: 'Eyeshadow'
  };

  const currentProducts = products[selectedCategory] || [];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Product Gallery</h1>
          <p className="text-lg text-gray-600">Explore our curated collection of makeup products</p>
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap gap-4 mb-8 justify-center">
          {Object.entries(categoryLabels).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setSelectedCategory(key)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedCategory === key
                  ? 'bg-gray-900 text-white shadow-lg'
                  : 'bg-white text-gray-900 border-2 border-gray-200 hover:border-gray-900'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-4 rounded-lg mb-8">
            {error}
          </div>
        )}

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {currentProducts.map((product) => (
            <div
              key={product.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow"
            >
              {/* Product Image */}
              <div className="w-full h-64 bg-gray-100 flex items-center justify-center overflow-hidden">
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"%3E%3Crect fill="%23e5e7eb" width="400" height="300"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="24"%3EProduct Image%3C/text%3E%3C/svg%3E';
                  }}
                />
              </div>

              {/* Product Info */}
              <div className="p-6">
                <p className="text-sm font-semibold text-gray-500 mb-1">{product.brand}</p>
                <h3 className="text-lg font-bold text-gray-900 mb-4">{product.name}</h3>

                {/* Rating */}
                <div className="flex items-center gap-2 mb-4">
                  <div className="flex items-center">
                    <span className="text-yellow-400">★</span>
                    <span className="font-semibold text-gray-900 ml-1">{product.rating}</span>
                  </div>
                  <span className="text-gray-500 text-sm">({product.reviews_count})</span>
                </div>

                {/* Price */}
                <p className="text-2xl font-bold text-gray-900 mb-4">₹{product.price_inr}</p>

                {/* Shades */}
                <div className="mb-6">
                  <p className="text-sm font-semibold text-gray-700 mb-3">Available Shades:</p>
                  <div className="flex flex-wrap gap-2">
                    {product.shades.map((shade, idx) => (
                      <div
                        key={idx}
                        className="flex items-center gap-2"
                        title={shade.name}
                      >
                        <div
                          className="w-8 h-8 rounded-full border-2 border-gray-300"
                          style={{ backgroundColor: shade.hex }}
                        />
                        <span className="text-xs text-gray-600 hidden sm:inline">
                          {shade.name}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* View Product Button */}
                <button className="w-full bg-gray-900 text-white font-bold py-3 px-4 rounded-lg hover:bg-gray-800 transition-colors">
                  View Product
                </button>
              </div>
            </div>
          ))}
        </div>

        {currentProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No products available in this category.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductGallery;
