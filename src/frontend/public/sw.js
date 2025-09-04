// Service Worker for Axie Studio PWA
// Version 1.0.0

const CACHE_NAME = 'axie-studio-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Resources to cache immediately
const STATIC_CACHE_URLS = [
  '/',
  '/offline.html',
  '/manifest.json',
  '/favicon.ico',
  '/favicon_io/android-chrome-192x192.png',
  '/favicon_io/android-chrome-512x512.png',
  '/favicon generator/1024 x 1024.png',
  // Add critical CSS and JS files here when available
];

// Resources to cache on first access
const RUNTIME_CACHE_URLS = [
  // API endpoints that should be cached
  '/api/v1/',
  '/api/v2/',
  // Static assets
  '/static/',
  '/assets/',
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
  console.log('[SW] Install event');
  
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      console.log('[SW] Caching static resources');
      
      // Cache static resources, but don't fail if some are missing
      const cachePromises = STATIC_CACHE_URLS.map(async (url) => {
        try {
          await cache.add(url);
          console.log(`[SW] Cached: ${url}`);
        } catch (error) {
          console.warn(`[SW] Failed to cache: ${url}`, error);
        }
      });
      
      await Promise.allSettled(cachePromises);
      
      // Force activation of new service worker
      self.skipWaiting();
    })()
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activate event');
  
  event.waitUntil(
    (async () => {
      // Clean up old caches
      const cacheNames = await caches.keys();
      const deletePromises = cacheNames
        .filter(name => name !== CACHE_NAME)
        .map(name => {
          console.log(`[SW] Deleting old cache: ${name}`);
          return caches.delete(name);
        });
      
      await Promise.all(deletePromises);
      
      // Take control of all clients
      await self.clients.claim();
      console.log('[SW] Service worker activated and claimed clients');
    })()
  );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension and other non-http requests
  if (!event.request.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    (async () => {
      try {
        // Try network first for API calls
        if (event.request.url.includes('/api/')) {
          return await handleApiRequest(event.request);
        }
        
        // For navigation requests (HTML pages)
        if (event.request.mode === 'navigate') {
          return await handleNavigationRequest(event.request);
        }
        
        // For static assets
        return await handleStaticRequest(event.request);
        
      } catch (error) {
        console.error('[SW] Fetch error:', error);
        
        // Return offline page for navigation requests
        if (event.request.mode === 'navigate') {
          const cache = await caches.open(CACHE_NAME);
          return await cache.match(OFFLINE_URL) || new Response('Offline');
        }
        
        return new Response('Network error', { status: 408 });
      }
    })()
  );
});

// Handle API requests - network first, then cache
async function handleApiRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    // Cache successful responses
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Fall back to cache
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      console.log(`[SW] Serving API from cache: ${request.url}`);
      return cachedResponse;
    }
    
    throw error;
  }
}

// Handle navigation requests - cache first, then network
async function handleNavigationRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  
  // Try cache first for faster loading
  const cachedResponse = await cache.match('/');
  if (cachedResponse) {
    // Fetch from network in background to update cache
    fetch(request).then(response => {
      if (response.ok) {
        cache.put(request, response.clone());
      }
    }).catch(() => {
      // Ignore network errors for background updates
    });
    
    return cachedResponse;
  }
  
  // If not in cache, try network
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    // Return offline page
    return await cache.match(OFFLINE_URL) || new Response('Offline');
  }
}

// Handle static asset requests - cache first, then network
async function handleStaticRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  
  // Try cache first
  const cachedResponse = await cache.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Try network and cache the response
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    throw error;
  }
}

// Handle background sync (if supported)
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Add your background sync logic here
      Promise.resolve()
    );
  }
});

// Handle push notifications (if needed)
self.addEventListener('push', (event) => {
  console.log('[SW] Push received');
  
  const options = {
    body: event.data ? event.data.text() : 'New notification from Axie Studio',
    icon: '/favicon generator/android-icon-192x192.png',
    badge: '/favicon generator/android-icon-96x96.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Open App',
        icon: '/favicon generator/android-icon-96x96.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/favicon generator/android-icon-96x96.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Axie Studio', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification click received.');
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

console.log('[SW] Service Worker loaded');
