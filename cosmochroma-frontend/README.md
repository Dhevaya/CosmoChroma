# CosmoChroma Frontend

AI-Powered Skin Analysis & Beauty Recommendation Platform

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Set Environment Variables
Create `.env` file:
```
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```

The app will be available at http://localhost:3000

### 4. Build for Production
```bash
npm run build
```

## Project Structure

```
cosmochroma-frontend/
├── src/
│   ├── components/
│   │   ├── UploadForm.jsx           # Image upload with drag-drop
│   │   ├── SkinToneResults.jsx      # Skin tone analysis display
│   │   ├── ProductRecommendations.jsx # Product cards
│   │   ├── SkincareRoutine.jsx      # Routine display
│   │   └── ResultsDashboard.jsx     # Results overview
│   ├── services/
│   │   └── api.js                   # API client with Axios
│   ├── store/
│   │   └── analysisStore.js         # Zustand state management
│   ├── hooks/
│   │   └── useImageAnalysis.js      # Analysis hook
│   ├── styles/
│   │   └── globals.css              # Global styles
│   ├── App.jsx                      # Main app component
│   └── main.jsx                     # React entry point
├── public/                          # Static assets
├── index.html                       # HTML template
├── vite.config.js                   # Vite configuration
├── tailwind.config.js               # Tailwind CSS config
├── postcss.config.js                # PostCSS config
└── package.json
```

## Features

### 🎨 Skin Tone Analysis
- Displays exact skin tone with RGB, HSV, and hex codes
- Shows undertone classification (Warm Golden, Cool, Olive, Neutral)
- Identifies seasonal color type (Spring, Summer, Autumn, Winter)
- Confidence scores for all classifications

### 💄 Product Recommendations
- **Foundation**: 5 color-matched options
- **Blush**: 5 shade recommendations
- **Lipstick**: 5 complementary shades
- **Concealer**: 5 matching options
- **Eyeshadow**: 5 coordinated options

Each product includes:
- Product image
- Brand name and shade
- Price in INR
- Rating and reviews
- Direct purchase link
- Color match distance

### 🧴 Personalized Skincare Routine
- **Morning Routine**: Energizing & protective steps
- **Evening Routine**: Cleansing & repair steps
- **Weekly Routine**: Deep care treatments

Customized for:
- Oily skin
- Dry skin
- Combination skin
- Sensitive skin
- Normal skin

### 📥 Download Results
Export analysis results as text file for future reference

## Technologies

- **React 18**: UI framework
- **Tailwind CSS**: Styling
- **Vite**: Build tool
- **Axios**: HTTP client
- **Zustand**: State management
- **React Dropzone**: File upload with drag-drop

## Components

### UploadForm
Drag-drop image upload interface with validation

### SkinToneResults
Displays:
- Skin tone swatch
- RGB/HSV/Hex values
- Undertone classification
- Season classification
- Confidence scores

### ProductRecommendations
Grid of product cards with:
- Product images
- Price and ratings
- Color match information
- Buy links

### SkincareRoutine
Collapsible routine sections with:
- Step-by-step instructions
- Duration timers
- Product recommendations
- Visual progress indicators

### ResultsDashboard
Main results page with navigation and download

## API Integration

### Environment Variables
```
VITE_API_URL=http://localhost:8000  # Backend API URL
```

### API Endpoints Used
- `POST /api/analyze` - Upload image and get analysis
- `GET /api/health` - Check API health

### Error Handling
- Displays user-friendly error messages
- Validates image formats before upload
- Shows loading states during analysis

## Styling

### Color Palette
- Primary: `#8B5CF6` (Purple)
- Secondary: `#EC4899` (Pink)
- Accent: `#F59E0B` (Amber)

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Grid layouts for product recommendations

## Development

### Code Quality
```bash
npm run lint
```

### Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Deployment

### Vercel
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Drag dist folder to Netlify
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## Performance Tips

- Images are lazy-loaded
- CSS is tree-shaken by Vite
- Components are optimized with React.memo where needed
- API calls are debounced
- Results are cached in Zustand store

## Accessibility

- Semantic HTML structure
- ARIA labels for interactive elements
- Keyboard navigation support
- Color contrast ratios meet WCAG standards

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## License

CosmoChroma © 2024
