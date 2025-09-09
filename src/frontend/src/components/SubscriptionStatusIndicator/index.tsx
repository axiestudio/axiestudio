/**
 * Real-time Subscription Status Indicator
 * Shows current subscription status with live updates and manual refresh capability
 */

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { RefreshCw, CheckCircle, AlertTriangle, Clock, Crown, XCircle } from 'lucide-react';
import { useGetSubscriptionStatus } from '@/controllers/API/queries/subscriptions';
import { useRealtimeSubscriptionContext } from '@/components/providers/RealtimeSubscriptionProvider';
import { cn } from '@/lib/utils';

interface SubscriptionStatusIndicatorProps {
  showRefreshButton?: boolean;
  showLastUpdated?: boolean;
  compact?: boolean;
  className?: string;
}

export const SubscriptionStatusIndicator: React.FC<SubscriptionStatusIndicatorProps> = ({
  showRefreshButton = true,
  showLastUpdated = true,
  compact = false,
  className
}) => {
  const { data: subscriptionStatus, isLoading } = useGetSubscriptionStatus();
  const { forceRefresh, isRefreshing, lastRefresh } = useRealtimeSubscriptionContext();
  const [refreshCount, setRefreshCount] = useState(0);

  const handleRefresh = async () => {
    try {
      await forceRefresh('manual refresh');
      setRefreshCount(prev => prev + 1);
    } catch (error) {
      console.error('Failed to refresh subscription status:', error);
    }
  };

  const getStatusInfo = () => {
    if (isLoading || !subscriptionStatus) {
      return {
        icon: Clock,
        label: 'Laddar...',
        color: 'bg-gray-500',
        textColor: 'text-gray-700',
        variant: 'secondary' as const
      };
    }

    const status = subscriptionStatus.subscription_status;
    const trialExpired = subscriptionStatus.trial_expired;

    switch (status) {
      case 'active':
        return {
          icon: CheckCircle,
          label: 'Aktiv Prenumeration',
          color: 'bg-green-500',
          textColor: 'text-green-700',
          variant: 'default' as const
        };
      case 'trial':
        if (trialExpired) {
          return {
            icon: XCircle,
            label: 'Provperiod Utgången',
            color: 'bg-red-500',
            textColor: 'text-red-700',
            variant: 'destructive' as const
          };
        }
        return {
          icon: Clock,
          label: `Provperiod (${subscriptionStatus.trial_days_left || 0} dagar kvar)`,
          color: 'bg-blue-500',
          textColor: 'text-blue-700',
          variant: 'secondary' as const
        };
      case 'canceled':
        return {
          icon: AlertTriangle,
          label: 'Avbruten Prenumeration',
          color: 'bg-orange-500',
          textColor: 'text-orange-700',
          variant: 'outline' as const
        };
      case 'admin':
        return {
          icon: Crown,
          label: 'Administratör',
          color: 'bg-purple-500',
          textColor: 'text-purple-700',
          variant: 'default' as const
        };
      default:
        return {
          icon: XCircle,
          label: 'Okänd Status',
          color: 'bg-gray-500',
          textColor: 'text-gray-700',
          variant: 'secondary' as const
        };
    }
  };

  const statusInfo = getStatusInfo();
  const StatusIcon = statusInfo.icon;

  const formatLastUpdated = () => {
    if (!lastRefresh) return 'Aldrig';
    const now = Date.now();
    const diff = now - lastRefresh;
    
    if (diff < 60000) return 'Just nu';
    if (diff < 3600000) return `${Math.floor(diff / 60000)} min sedan`;
    return `${Math.floor(diff / 3600000)} tim sedan`;
  };

  // Auto-refresh display every 30 seconds
  useEffect(() => {
    if (!showLastUpdated) return;
    
    const interval = setInterval(() => {
      // Force re-render to update "last updated" display
      setRefreshCount(prev => prev);
    }, 30000);

    return () => clearInterval(interval);
  }, [showLastUpdated]);

  if (compact) {
    return (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <div className={cn("flex items-center gap-2", className)}>
              <StatusIcon className={cn("h-4 w-4", statusInfo.textColor)} />
              <Badge variant={statusInfo.variant} className="text-xs">
                {statusInfo.label}
              </Badge>
              {showRefreshButton && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                  className="h-6 w-6 p-0"
                >
                  <RefreshCw className={cn("h-3 w-3", isRefreshing && "animate-spin")} />
                </Button>
              )}
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <div className="text-sm">
              <p><strong>Status:</strong> {statusInfo.label}</p>
              {showLastUpdated && (
                <p><strong>Senast uppdaterad:</strong> {formatLastUpdated()}</p>
              )}
              {subscriptionStatus?.subscription_id && (
                <p><strong>Prenumerations-ID:</strong> {subscriptionStatus.subscription_id.slice(-8)}</p>
              )}
            </div>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    );
  }

  return (
    <div className={cn("flex items-center justify-between p-3 border rounded-lg", className)}>
      <div className="flex items-center gap-3">
        <div className={cn("p-2 rounded-full", statusInfo.color)}>
          <StatusIcon className="h-4 w-4 text-white" />
        </div>
        <div>
          <p className="font-medium">{statusInfo.label}</p>
          {showLastUpdated && (
            <p className="text-sm text-muted-foreground">
              Senast uppdaterad: {formatLastUpdated()}
            </p>
          )}
        </div>
      </div>
      
      {showRefreshButton && (
        <Button
          variant="outline"
          size="sm"
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="flex items-center gap-2"
        >
          <RefreshCw className={cn("h-4 w-4", isRefreshing && "animate-spin")} />
          {isRefreshing ? 'Uppdaterar...' : 'Uppdatera'}
        </Button>
      )}
    </div>
  );
};

export default SubscriptionStatusIndicator;
