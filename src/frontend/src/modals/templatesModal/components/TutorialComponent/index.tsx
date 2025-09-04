import { useParams } from "react-router-dom";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { track } from "@/customization/utils/analytics";
import { useGetTutorialQuery } from "@/controllers/API/queries/flows/use-get-tutorial";
import useAddFlow from "@/hooks/flows/use-add-flow";
import useFlowsManagerStore from "@/stores/flowsManagerStore";

export default function TutorialComponent() {
  const navigate = useCustomNavigate();
  const { folderId } = useParams();
  const addFlow = useAddFlow();
  const setCurrentFlow = useFlowsManagerStore((state) => state.setCurrentFlow);
  
  const { data: tutorialFlow, isLoading, error } = useGetTutorialQuery({});

  const handleStartTutorial = async () => {
    if (tutorialFlow) {
      // Create a new flow based on the tutorial
      const newFlowId = await addFlow();

      // Set the tutorial flow as the current flow
      const tutorialFlowCopy = {
        ...tutorialFlow,
        id: newFlowId as string,
        name: `${tutorialFlow.name} - Kopia`,
      };

      setCurrentFlow(tutorialFlowCopy);

      // Navigate to the new flow
      navigate(`/flow/${newFlowId}${folderId ? `/folder/${folderId}` : ""}`);

      // Track the tutorial start
      track("Tutorial Started", {
        tutorial_name: tutorialFlow.name,
        source: "templates_modal"
      });
    }
  };

  const handleViewTutorial = () => {
    if (tutorialFlow) {
      // Navigate directly to the tutorial flow
      navigate(`/flow/${tutorialFlow.id}${folderId ? `/folder/${folderId}` : ""}`);
      
      // Track the tutorial view
      track("Tutorial Viewed", { 
        tutorial_name: tutorialFlow.name,
        source: "templates_modal" 
      });
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center gap-2">
          <ForwardedIconComponent name="Loader2" className="h-4 w-4 animate-spin" />
          <span>Laddar tutorial...</span>
        </div>
      </div>
    );
  }

  if (error || !tutorialFlow) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="text-center">
          <ForwardedIconComponent name="AlertCircle" className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
          <p className="text-muted-foreground">Tutorial kunde inte laddas</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">🎓 Välkommen till Axie Studio Tutorial</h2>
        <p className="text-muted-foreground">
          Lär dig grunderna i Axie Studio genom vår interaktiva steg-för-steg guide
        </p>
      </div>

      <Card className="border-2 border-primary/20 bg-gradient-to-br from-primary/5 to-primary/10">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <ForwardedIconComponent name="GraduationCap" className="h-6 w-6 text-primary" />
            </div>
            <div>
              <CardTitle className="text-lg">{tutorialFlow.name}</CardTitle>
              <CardDescription className="mt-1">
                {tutorialFlow.description || "En komplett guide för att komma igång med Axie Studio"}
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-semibold flex items-center gap-2">
                <ForwardedIconComponent name="CheckCircle" className="h-4 w-4 text-green-500" />
                Vad du kommer att lära dig:
              </h4>
              <ul className="text-sm text-muted-foreground space-y-1 ml-6">
                <li>• Grundläggande gränssnitt och navigation</li>
                <li>• Hur man bygger ditt första AI-flöde</li>
                <li>• Arbeta med komponenter och kopplingar</li>
                <li>• Testa och köra dina flöden</li>
                <li>• Avancerade funktioner och tips</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold flex items-center gap-2">
                <ForwardedIconComponent name="Clock" className="h-4 w-4 text-blue-500" />
                Tutorial-information:
              </h4>
              <ul className="text-sm text-muted-foreground space-y-1 ml-6">
                <li>• Uppskattad tid: 15-20 minuter</li>
                <li>• Interaktiv steg-för-steg guide</li>
                <li>• Praktiska övningar</li>
                <li>• Kan pausas när som helst</li>
              </ul>
            </div>
          </div>
          
          <div className="flex gap-3 pt-4">
            <Button onClick={handleStartTutorial} className="flex-1">
              <ForwardedIconComponent name="Play" className="h-4 w-4 mr-2" />
              Starta tutorial
            </Button>
            <Button variant="outline" onClick={handleViewTutorial}>
              <ForwardedIconComponent name="Eye" className="h-4 w-4 mr-2" />
              Visa tutorial
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="text-center">
          <CardContent className="pt-6">
            <ForwardedIconComponent name="Zap" className="h-8 w-8 mx-auto mb-2 text-yellow-500" />
            <h4 className="font-semibold mb-1">Snabb start</h4>
            <p className="text-sm text-muted-foreground">
              Kom igång på bara några minuter
            </p>
          </CardContent>
        </Card>
        
        <Card className="text-center">
          <CardContent className="pt-6">
            <ForwardedIconComponent name="Users" className="h-8 w-8 mx-auto mb-2 text-blue-500" />
            <h4 className="font-semibold mb-1">Community</h4>
            <p className="text-sm text-muted-foreground">
              Lär från andra användare
            </p>
          </CardContent>
        </Card>
        
        <Card className="text-center">
          <CardContent className="pt-6">
            <ForwardedIconComponent name="BookOpen" className="h-8 w-8 mx-auto mb-2 text-green-500" />
            <h4 className="font-semibold mb-1">Dokumentation</h4>
            <p className="text-sm text-muted-foreground">
              Djupgående guider och referenser
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
