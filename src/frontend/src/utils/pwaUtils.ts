// PWA Utility functions for Axie Studio

export interface PWAStatus {
  isInstalled: boolean;
  isStandalone: boolean;
  isOnline: boolean;
  hasServiceWorker: boolean;
  canInstall: boolean;
  platform: 'ios' | 'android' | 'desktop' | 'unknown';
}

export interface PWACapabilities {
  notifications: boolean;
  backgroundSync: boolean;
  pushMessaging: boolean;
  webShare: boolean;
  fullscreen: boolean;
  orientation: boolean;
}

/**
 * Check the current PWA status
 */
export function getPWAStatus(): PWAStatus {
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                      (window.navigator as any).standalone === true;
  
  const isInstalled = isStandalone || 
                     window.matchMedia('(display-mode: minimal-ui)').matches ||
                     window.matchMedia('(display-mode: window-controls-overlay)').matches;

  const hasServiceWorker = 'serviceWorker' in navigator && 
                          navigator.serviceWorker.controller !== null;

  const platform = detectPlatform();
  
  return {
    isInstalled,
    isStandalone,
    isOnline: navigator.onLine,
    hasServiceWorker,
    canInstall: !isInstalled && 'serviceWorker' in navigator,
    platform
  };
}

/**
 * Detect the current platform
 */
export function detectPlatform(): 'ios' | 'android' | 'desktop' | 'unknown' {
  const userAgent = navigator.userAgent.toLowerCase();
  
  if (/ipad|iphone|ipod/.test(userAgent)) {
    return 'ios';
  }
  
  if (/android/.test(userAgent)) {
    return 'android';
  }
  
  if (/windows|macintosh|linux/.test(userAgent)) {
    return 'desktop';
  }
  
  return 'unknown';
}

/**
 * Check PWA capabilities
 */
export function getPWACapabilities(): PWACapabilities {
  return {
    notifications: 'Notification' in window,
    backgroundSync: 'serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype,
    pushMessaging: 'serviceWorker' in navigator && 'PushManager' in window,
    webShare: 'share' in navigator,
    fullscreen: 'requestFullscreen' in document.documentElement,
    orientation: 'orientation' in screen
  };
}

/**
 * Request notification permission
 */
export async function requestNotificationPermission(): Promise<NotificationPermission> {
  if (!('Notification' in window)) {
    console.warn('This browser does not support notifications');
    return 'denied';
  }

  if (Notification.permission === 'granted') {
    return 'granted';
  }

  if (Notification.permission === 'denied') {
    return 'denied';
  }

  const permission = await Notification.requestPermission();
  return permission;
}

/**
 * Show a notification
 */
export function showNotification(title: string, options?: NotificationOptions): void {
  if (Notification.permission !== 'granted') {
    console.warn('Notification permission not granted');
    return;
  }

  const defaultOptions: NotificationOptions = {
    icon: '/favicon generator/android-icon-192x192.png',
    badge: '/favicon generator/android-icon-96x96.png',
    vibrate: [100, 50, 100],
    ...options
  };

  new Notification(title, defaultOptions);
}

/**
 * Register for push notifications
 */
export async function registerPushNotifications(): Promise<PushSubscription | null> {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    console.warn('Push messaging is not supported');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(
        // Replace with your VAPID public key
        'YOUR_VAPID_PUBLIC_KEY_HERE'
      )
    });

    console.log('Push subscription successful:', subscription);
    return subscription;
  } catch (error) {
    console.error('Failed to subscribe to push notifications:', error);
    return null;
  }
}

/**
 * Convert VAPID key
 */
function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

/**
 * Share content using Web Share API
 */
export async function shareContent(data: ShareData): Promise<boolean> {
  if (!('share' in navigator)) {
    console.warn('Web Share API not supported');
    return false;
  }

  try {
    await navigator.share(data);
    return true;
  } catch (error) {
    console.error('Error sharing:', error);
    return false;
  }
}

/**
 * Add to home screen prompt for iOS
 */
export function showIOSInstallPrompt(): void {
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
  const isInStandaloneMode = (window.navigator as any).standalone;

  if (isIOS && !isInStandaloneMode) {
    // Show custom iOS install instructions
    console.log('Show iOS install instructions');
  }
}

/**
 * Check if app needs update
 */
export async function checkForUpdates(): Promise<boolean> {
  if (!('serviceWorker' in navigator)) {
    return false;
  }

  try {
    const registration = await navigator.serviceWorker.getRegistration();
    if (!registration) {
      return false;
    }

    await registration.update();
    return registration.waiting !== null;
  } catch (error) {
    console.error('Error checking for updates:', error);
    return false;
  }
}

/**
 * Apply pending updates
 */
export async function applyUpdate(): Promise<void> {
  if (!('serviceWorker' in navigator)) {
    return;
  }

  try {
    const registration = await navigator.serviceWorker.getRegistration();
    if (!registration || !registration.waiting) {
      return;
    }

    registration.waiting.postMessage({ type: 'SKIP_WAITING' });
    
    // Reload the page to activate the new service worker
    window.location.reload();
  } catch (error) {
    console.error('Error applying update:', error);
  }
}

/**
 * Get app installation date (if available)
 */
export function getInstallationDate(): Date | null {
  const installDate = localStorage.getItem('pwa-install-date');
  return installDate ? new Date(installDate) : null;
}

/**
 * Set app installation date
 */
export function setInstallationDate(): void {
  localStorage.setItem('pwa-install-date', new Date().toISOString());
}

/**
 * Track PWA usage analytics
 */
export function trackPWAEvent(event: string, data?: any): void {
  const pwaStatus = getPWAStatus();
  const eventData = {
    event,
    timestamp: new Date().toISOString(),
    pwaStatus,
    ...data
  };

  // Send to your analytics service
  console.log('PWA Event:', eventData);
  
  // Example: Send to Google Analytics
  if ((window as any).gtag) {
    (window as any).gtag('event', event, {
      custom_parameter_1: pwaStatus.isInstalled ? 'installed' : 'browser',
      custom_parameter_2: pwaStatus.platform,
      ...data
    });
  }
}

/**
 * Initialize PWA features
 */
export function initializePWA(): void {
  const pwaStatus = getPWAStatus();
  
  // Track PWA load
  trackPWAEvent('pwa_load', pwaStatus);
  
  // Set installation date if first time
  if (pwaStatus.isInstalled && !getInstallationDate()) {
    setInstallationDate();
  }
  
  // Listen for online/offline events
  window.addEventListener('online', () => {
    trackPWAEvent('connection_online');
    console.log('App is online');
  });
  
  window.addEventListener('offline', () => {
    trackPWAEvent('connection_offline');
    console.log('App is offline');
  });
  
  // Listen for app install
  window.addEventListener('appinstalled', () => {
    trackPWAEvent('app_installed');
    setInstallationDate();
  });
  
  console.log('PWA initialized:', pwaStatus);
}
