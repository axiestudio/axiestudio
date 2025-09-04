# 🚀 Vercel Deployment Guide - Axie Studio Swedish

## 📋 Pre-Deployment Checklist

### ✅ **Translation Status - COMPLETE!**
- [x] All user-facing strings translated to Swedish
- [x] Global Variable Modal translated
- [x] Playground Modal translated  
- [x] Settings pages translated
- [x] Error messages translated
- [x] Success messages translated
- [x] Form fields and placeholders translated
- [x] Navigation items translated
- [x] Modal titles and content translated

### ✅ **Technical Preparation**
- [x] HTML lang attribute set to "sv"
- [x] Swedish meta descriptions
- [x] Manifest files updated
- [x] Favicon configuration complete
- [x] Environment variables configured

## 🌐 **Deployment Options**

### **Option 1: Vercel Web Interface (Recommended)**

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/Login** with your GitHub account
3. **Import Project**:
   - Click "New Project"
   - Import from Git Repository
   - Connect your GitHub account if needed
   - Select this repository

4. **Configure Project**:
   ```
   Framework Preset: Vite
   Root Directory: ./
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

5. **Environment Variables**:
   ```
   VITE_PROXY_TARGET=https://flow.axiestudio.se
   ```

6. **Deploy**: Click "Deploy" button

### **Option 2: Vercel CLI (Alternative)**

If you have Node.js properly configured in PATH:

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

### **Option 3: GitHub Integration (Automated)**

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Swedish translation complete - ready for deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to vercel.com
   - Import from GitHub
   - Select auto-deploy on push

## ⚙️ **Vercel Configuration**

Create `vercel.json` in project root:

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev",
  "env": {
    "VITE_PROXY_TARGET": "https://flow.axiestudio.se"
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://flow.axiestudio.se/api/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

## 🔧 **Build Configuration**

Update `package.json` scripts if needed:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "deploy": "vercel --prod"
  }
}
```

## 🌍 **Domain Configuration**

### **Custom Domain Setup**:
1. Go to Vercel Dashboard
2. Select your project
3. Go to "Settings" → "Domains"
4. Add your custom domain
5. Configure DNS records as instructed

### **Suggested Domains**:
- `axiestudio-sv.vercel.app` (free Vercel subdomain)
- `axiestudio.se` (if you own the domain)
- `sv.axiestudio.com` (subdomain)

## 📊 **Performance Optimization**

### **Vite Build Optimizations**:
```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

## 🔒 **Security Headers**

Vercel automatically adds security headers, but you can customize:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000; includeSubDomains"
        },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
        }
      ]
    }
  ]
}
```

## 📈 **Analytics & Monitoring**

### **Vercel Analytics**:
1. Go to project settings
2. Enable "Analytics"
3. Add to your app:
   ```bash
   npm install @vercel/analytics
   ```

### **Performance Monitoring**:
- Vercel provides built-in performance metrics
- Core Web Vitals tracking
- Real User Monitoring (RUM)

## 🚀 **Deployment Commands**

### **Quick Deploy**:
```bash
# One-time deployment
vercel

# Production deployment
vercel --prod

# Deploy with custom name
vercel --name axiestudio-swedish
```

### **Environment-specific Deployments**:
```bash
# Preview deployment
vercel

# Production deployment
vercel --prod

# Deploy specific branch
vercel --prod --target production
```

## 🔍 **Post-Deployment Testing**

### **Checklist**:
- [ ] Swedish interface loads correctly
- [ ] All pages accessible
- [ ] API calls work (proxy to backend)
- [ ] Forms submit properly
- [ ] Error messages in Swedish
- [ ] Mobile responsiveness
- [ ] Performance metrics acceptable

### **Test URLs**:
- `/` - Main dashboard
- `/login` - Login page
- `/settings` - Settings page
- `/flows` - Flow builder
- `/admin` - Admin panel

## 🎯 **Success Metrics**

Your deployment is successful when:
- ✅ All pages load in Swedish
- ✅ No console errors
- ✅ API integration working
- ✅ Performance score > 90
- ✅ Mobile-friendly
- ✅ SEO optimized for Swedish

## 📞 **Support**

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test locally first with `npm run build && npm run preview`
4. Check browser console for errors

---

**🎉 Your Swedish Axie Studio is ready for the world!** 🇸🇪
