import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import ForwardedIconComponent from '@/components/common/genericIconComponent';
import { cn } from '@/utils/utils';

interface TutorialStep {
  id: number;
  title: string;
  content: string;
  target?: string;
  action?: string;
  image?: string;
}

interface TutorialModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const tutorialSteps: TutorialStep[] = [
  {
    id: 1,
    title: "Välkommen till Axie Studio!",
    content: "Axie Studio är en kraftfull plattform för att skapa AI-arbetsflöden utan kod. Låt oss gå igenom grunderna tillsammans!",
    action: "Kom igång"
  },
  {
    id: 2,
    title: "Skapa ditt första flöde",
    content: "Ett flöde är en sekvens av AI-komponenter som arbetar tillsammans. Klicka på 'Nytt flöde' för att börja.",
    target: "#new-project-btn",
    action: "Skapa flöde"
  },
  {
    id: 3,
    title: "Lägg till komponenter",
    content: "Komponenter är byggstenar i ditt flöde. Du kan dra och släppa dem från sidopanelen till arbetsytan.",
    action: "Förstått"
  },
  {
    id: 4,
    title: "Koppla komponenter",
    content: "Koppla komponenter genom att dra från en utport till en inport. Detta skapar dataflödet i ditt arbetsflöde.",
    action: "Nästa"
  },
  {
    id: 5,
    title: "Konfigurera komponenter",
    content: "Klicka på en komponent för att öppna dess inställningar. Här kan du anpassa beteende och parametrar.",
    action: "Nästa"
  },
  {
    id: 6,
    title: "Kör ditt flöde",
    content: "När ditt flöde är klart kan du köra det genom att klicka på play-knappen. Resultatet visas i utdata-komponenten.",
    action: "Nästa"
  },
  {
    id: 7,
    title: "Spara och dela",
    content: "Glöm inte att spara ditt flöde! Du kan också dela det med andra eller exportera det för användning i andra miljöer.",
    action: "Avsluta tutorial"
  }
];

export default function TutorialModal({ isOpen, onClose }: TutorialModalProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  const progress = ((currentStep + 1) / tutorialSteps.length) * 100;
  const step = tutorialSteps[currentStep];

  useEffect(() => {
    if (currentStep >= tutorialSteps.length) {
      setIsCompleted(true);
    }
  }, [currentStep]);

  const handleNext = () => {
    if (currentStep < tutorialSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    setIsCompleted(true);
    // Store tutorial completion in localStorage
    localStorage.setItem('axiestudio-tutorial-completed', 'true');
  };

  const handleClose = () => {
    onClose();
    // Reset tutorial state when closing
    setTimeout(() => {
      setCurrentStep(0);
      setIsCompleted(false);
    }, 300);
  };

  const handleSkip = () => {
    handleComplete();
    handleClose();
  };

  if (!isOpen) return null;

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <ForwardedIconComponent name="GraduationCap" className="h-5 w-5" />
            Axie Studio Tutorial
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Steg {currentStep + 1} av {tutorialSteps.length}</span>
              <span>{Math.round(progress)}% klart</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {!isCompleted ? (
            <>
              {/* Step Content */}
              <div className="space-y-4">
                <h3 className="text-xl font-semibold">{step.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {step.content}
                </p>
                
                {step.target && (
                  <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                    <div className="flex items-center gap-2 text-blue-700 dark:text-blue-300">
                      <ForwardedIconComponent name="Target" className="h-4 w-4" />
                      <span className="text-sm font-medium">Titta efter detta element på sidan</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Navigation Buttons */}
              <div className="flex justify-between items-center pt-4">
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    onClick={handlePrevious}
                    disabled={currentStep === 0}
                    className="flex items-center gap-2"
                  >
                    <ForwardedIconComponent name="ChevronLeft" className="h-4 w-4" />
                    Föregående
                  </Button>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    onClick={handleSkip}
                    className="text-muted-foreground"
                  >
                    Hoppa över
                  </Button>
                  <Button
                    onClick={handleNext}
                    className="flex items-center gap-2"
                  >
                    {step.action || "Nästa"}
                    <ForwardedIconComponent name="ChevronRight" className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </>
          ) : (
            /* Completion Screen */
            <div className="text-center space-y-4 py-8">
              <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
                <ForwardedIconComponent name="CheckCircle" className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold">Grattis! 🎉</h3>
              <p className="text-muted-foreground">
                Du har slutfört Axie Studio-tutorialen. Nu är du redo att skapa fantastiska AI-arbetsflöden!
              </p>
              <Button onClick={handleClose} className="mt-4">
                Börja skapa
              </Button>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
