# 🔗 Backend Integration Guide - Axie Studio Tauri App

This document explains how the Axie Studio Tauri desktop application connects to the backend at `https://flow.axiestudio.se`.

## 🎯 **Integration Overview**

### **Backend URL Configuration**
- **Production Backend:** `https://flow.axiestudio.se`
- **Development Backend:** `http://localhost:7860`
- **Health Check Endpoint:** `/health`
- **API Base:** `/api/v1/` and `/api/v2/`

## 🔧 **Technical Implementation**

### **1. Environment Configuration**
```bash
# .env file
VITE_PROXY_TARGET=https://flow.axiestudio.se
BACKEND_URL=https://flow.axiestudio.se
AXIESTUDIO_AUTO_LOGIN=false
```

### **2. Tauri Security Configuration**
```json
// tauri.conf.json
"security": {
  "csp": "default-src 'self' ... https://flow.axiestudio.se wss://flow.axiestudio.se; connect-src 'self' ... https://flow.axiestudio.se wss://flow.axiestudio.se;"
}
```

### **3. Frontend API Configuration**
- **Base URL Detection:** Automatically detects Tauri vs Web environment
- **Production Builds:** Always use `https://flow.axiestudio.se`
- **Development:** Use localhost or environment variable

### **4. Tauri Backend Commands**
```rust
// Available Tauri commands
get_backend_url() -> String
check_backend_health() -> HealthResponse
get_api_config() -> ApiConfig
```

## 🚀 **Usage in Frontend**

### **React Hook Integration**
```typescript
import { useTauriBackend } from '@/hooks/useTauriBackend';

function MyComponent() {
  const { 
    isInTauri, 
    backendUrl, 
    isBackendHealthy, 
    loading 
  } = useTauriBackend();

  if (loading) return <div>Connecting to backend...</div>;
  
  return (
    <div>
      <p>Environment: {isInTauri ? 'Tauri Desktop' : 'Web Browser'}</p>
      <p>Backend: {backendUrl}</p>
      <p>Status: {isBackendHealthy ? '✅ Healthy' : '❌ Offline'}</p>
    </div>
  );
}
```

### **API Calls**
All existing API calls automatically use the correct backend URL:
```typescript
// This works in both Tauri and Web environments
const response = await api.get('/api/v1/flows');
```

## 🔍 **Environment Detection**

### **Tauri Environment**
- Detected by presence of `window.__TAURI__`
- Uses Rust backend commands for health checks
- CSP allows connections to production backend
- Always uses `https://flow.axiestudio.se`

### **Web Environment**
- Standard browser environment
- Uses fetch for health checks
- Respects CORS policies
- Uses environment variables for backend URL

## 🛠️ **Development vs Production**

### **Development Mode**
```bash
# Frontend dev server
npm start
# Uses: http://localhost:7860 (if backend running locally)
# Or: https://flow.axiestudio.se (if no local backend)

# Tauri dev mode
cargo tauri dev
# Always uses: https://flow.axiestudio.se
```

### **Production Builds**
```bash
# Web build
npm run build
# Uses: https://flow.axiestudio.se

# Tauri build
cargo tauri build
# Uses: https://flow.axiestudio.se
```

## 🔐 **Security Considerations**

### **CORS Configuration**
The backend at `https://flow.axiestudio.se` must allow:
- Origin: `tauri://localhost` (for Tauri apps)
- Origin: `https://your-web-domain.com` (for web deployments)

### **CSP (Content Security Policy)**
Tauri CSP allows connections to:
- `https://flow.axiestudio.se` (HTTPS)
- `wss://flow.axiestudio.se` (WebSocket)
- All standard localhost development URLs

## 🧪 **Testing Backend Connection**

### **Health Check**
```bash
# Test backend availability
curl https://flow.axiestudio.se/health
# Expected: {"status":"ok"}
```

### **API Configuration**
```bash
# Test API config endpoint
curl https://flow.axiestudio.se/api/v1/config
# Expected: JSON with feature flags and settings
```

### **In Application**
1. **Tauri App:** Check console for "🚀 Tauri Backend Integration Initialized"
2. **Web App:** Check console for "🌐 Web Backend Integration Initialized"
3. **Health Status:** Monitor the health indicator in the UI

## 🐛 **Troubleshooting**

### **Common Issues**

1. **CSP Violations**
   - **Symptom:** Network requests blocked
   - **Solution:** Update CSP in `tauri.conf.json`

2. **CORS Errors**
   - **Symptom:** "Access-Control-Allow-Origin" errors
   - **Solution:** Configure backend CORS settings

3. **Health Check Failures**
   - **Symptom:** Backend shows as offline
   - **Solution:** Verify `https://flow.axiestudio.se/health` responds

4. **Environment Detection Issues**
   - **Symptom:** Wrong backend URL used
   - **Solution:** Check console logs for environment detection

### **Debug Commands**
```javascript
// In browser console or Tauri dev tools
console.log('Backend URL:', window.__TAURI__ ? 'Tauri Mode' : 'Web Mode');

// Check current API base URL
console.log('API Base:', axios.defaults.baseURL);

// Test health check
fetch('https://flow.axiestudio.se/health').then(r => r.json()).then(console.log);
```

## 📊 **Monitoring**

### **Health Monitoring**
- Automatic health checks every 30 seconds
- Visual indicators in the UI
- Console logging for debugging

### **Connection Status**
- Real-time connection status
- Automatic reconnection attempts
- Fallback handling for offline scenarios

---

**✅ Your Axie Studio Tauri app is now properly configured to connect to `https://flow.axiestudio.se`!**
