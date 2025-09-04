import React, { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{
    outcome: 'accepted' | 'dismissed';
    platform: string;
  }>;
  prompt(): Promise<void>;
}

declare global {
  interface WindowEventMap {
    beforeinstallprompt: BeforeInstallPromptEvent;
  }
}

interface PWAInstallPromptProps {
  className?: string;
  onInstall?: () => void;
  onDismiss?: () => void;
}

export const PWAInstallPrompt: React.FC<PWAInstallPromptProps> = ({
  className = '',
  onInstall,
  onDismiss,
}) => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showPrompt, setShowPrompt] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isIOS, setIsIOS] = useState(false);

  useEffect(() => {
    // Check if app is already installed
    const checkIfInstalled = () => {
      // Check for standalone mode (installed PWA)
      if (window.matchMedia('(display-mode: standalone)').matches) {
        setIsInstalled(true);
        return;
      }
      
      // Check for iOS standalone mode
      if ((window.navigator as any).standalone === true) {
        setIsInstalled(true);
        return;
      }
    };

    // Check if iOS
    const checkIfIOS = () => {
      const isIOSDevice = /iPad|iPhone|iPod/.test(navigator.userAgent);
      setIsIOS(isIOSDevice);
    };

    checkIfInstalled();
    checkIfIOS();

    // Listen for the beforeinstallprompt event
    const handleBeforeInstallPrompt = (e: BeforeInstallPromptEvent) => {
      console.log('PWA install prompt available');
      e.preventDefault();
      setDeferredPrompt(e);
      setShowPrompt(true);
    };

    // Listen for app installed event
    const handleAppInstalled = () => {
      console.log('PWA was installed');
      setIsInstalled(true);
      setShowPrompt(false);
      setDeferredPrompt(null);
      onInstall?.();
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, [onInstall]);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    try {
      await deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      
      if (outcome === 'accepted') {
        console.log('User accepted the install prompt');
        onInstall?.();
      } else {
        console.log('User dismissed the install prompt');
        onDismiss?.();
      }
      
      setDeferredPrompt(null);
      setShowPrompt(false);
    } catch (error) {
      console.error('Error during PWA installation:', error);
    }
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    onDismiss?.();
  };

  // Don't show if already installed
  if (isInstalled) {
    return null;
  }

  // iOS install instructions
  if (isIOS && !isInstalled) {
    return (
      <div className={`pwa-install-prompt ios-prompt ${className}`}>
        <div className="pwa-prompt-content">
          <div className="pwa-prompt-icon">📱</div>
          <div className="pwa-prompt-text">
            <h3>Install Axie Studio</h3>
            <p>
              To install this app on your iPhone/iPad, tap the share button{' '}
              <span className="share-icon">⬆️</span> and then "Add to Home Screen".
            </p>
          </div>
          <button 
            className="pwa-prompt-dismiss"
            onClick={handleDismiss}
            aria-label="Dismiss install prompt"
          >
            ✕
          </button>
        </div>
      </div>
    );
  }

  // Standard install prompt
  if (showPrompt && deferredPrompt) {
    return (
      <div className={`pwa-install-prompt ${className}`}>
        <div className="pwa-prompt-content">
          <div className="pwa-prompt-icon">⚡</div>
          <div className="pwa-prompt-text">
            <h3>Install Axie Studio</h3>
            <p>Get the full app experience with offline access and faster loading.</p>
          </div>
          <div className="pwa-prompt-actions">
            <button 
              className="pwa-install-button"
              onClick={handleInstallClick}
            >
              Install App
            </button>
            <button 
              className="pwa-dismiss-button"
              onClick={handleDismiss}
            >
              Not Now
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

// CSS styles (you can move this to a separate CSS file)
export const PWAInstallPromptStyles = `
.pwa-install-prompt {
  position: fixed;
  bottom: 20px;
  left: 20px;
  right: 20px;
  max-width: 400px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  animation: slideUp 0.3s ease-out;
}

.pwa-install-prompt.ios-prompt {
  background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
}

.pwa-prompt-content {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
  position: relative;
}

.pwa-prompt-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.pwa-prompt-text {
  flex: 1;
}

.pwa-prompt-text h3 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
}

.pwa-prompt-text p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.4;
}

.share-icon {
  display: inline-block;
  font-size: 16px;
  margin: 0 2px;
}

.pwa-prompt-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

.pwa-install-button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pwa-install-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.pwa-dismiss-button {
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
  border: none;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  text-decoration: underline;
}

.pwa-prompt-dismiss {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 480px) {
  .pwa-install-prompt {
    left: 10px;
    right: 10px;
    bottom: 10px;
  }
  
  .pwa-prompt-content {
    padding: 12px;
  }
  
  .pwa-prompt-actions {
    flex-direction: row;
  }
}
`;

export default PWAInstallPrompt;
