import { useState, useEffect } from 'react';

export function useTutorial() {
  const [isTutorialOpen, setIsTutorialOpen] = useState(false);
  const [hasCompletedTutorial, setHasCompletedTutorial] = useState(false);

  useEffect(() => {
    // Check if user has completed tutorial
    const completed = localStorage.getItem('axiestudio-tutorial-completed') === 'true';
    setHasCompletedTutorial(completed);
  }, []);

  const openTutorial = () => {
    setIsTutorialOpen(true);
  };

  const closeTutorial = () => {
    setIsTutorialOpen(false);
  };

  const markTutorialCompleted = () => {
    localStorage.setItem('axiestudio-tutorial-completed', 'true');
    setHasCompletedTutorial(true);
  };

  const resetTutorial = () => {
    localStorage.removeItem('axiestudio-tutorial-completed');
    setHasCompletedTutorial(false);
  };

  return {
    isTutorialOpen,
    hasCompletedTutorial,
    openTutorial,
    closeTutorial,
    markTutorialCompleted,
    resetTutorial,
  };
}
