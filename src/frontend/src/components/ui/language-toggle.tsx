import React from 'react';
import { useTranslation } from "react-i18next";
import { Button } from './button';
import { cn } from '@/utils/utils';

interface LanguageToggleProps {
  className?: string;
}

export function LanguageToggle({ className }: LanguageToggleProps) {
  const { i18n } = useTranslation();
  
  const currentLanguage = i18n.language || 'en';
  
  const toggleLanguage = () => {
    const newLanguage = currentLanguage === 'en' ? 'sv' : 'en';
    i18n.changeLanguage(newLanguage);
  };
  
  const getLanguageLabel = () => {
    return currentLanguage === 'en' ? '🇸🇪 Svenska' : '🇬🇧 English';
  };
  
  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={toggleLanguage}
      className={cn(
        "text-sm font-medium text-muted-foreground hover:text-foreground transition-colors",
        className
      )}
    >
      {getLanguageLabel()}
    </Button>
  );
}
