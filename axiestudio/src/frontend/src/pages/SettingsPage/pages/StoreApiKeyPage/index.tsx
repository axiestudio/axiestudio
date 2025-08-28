import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const StoreApiKeyPage = () => {
  const navigate = useCustomNavigate();

  return (
    <div className="flex h-full w-full flex-col gap-6">
      <div className="flex w-full items-start gap-6">
        <div className="flex w-full flex-col">
          <h2 className="flex items-center text-lg font-semibold tracking-tight">
            Komponent- och flödesutställning
            <ForwardedIconComponent
              name="Package"
              className="ml-2 h-5 w-5 text-primary"
            />
          </h2>
          <p className="text-sm text-muted-foreground">
            Bläddra och ladda ner från vår samling av 1 600 professionella komponenter och flöden.
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ForwardedIconComponent name="Library" className="h-5 w-5" />
            AxieStudio Component Library
          </CardTitle>
          <CardDescription>
            Discover ready-to-use components and flows to accelerate your development.
            All items are available for immediate download and use in your projects.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <Badge variant="secondary" className="flex items-center gap-1">
              <ForwardedIconComponent name="Workflow" className="h-3 w-3" />
              1,172 Flows
            </Badge>
            <Badge variant="secondary" className="flex items-center gap-1">
              <ForwardedIconComponent name="Component" className="h-3 w-3" />
              428 Components
            </Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <ForwardedIconComponent name="Download" className="h-3 w-3" />
              Free Downloads
            </Badge>
          </div>

          <div className="space-y-3">
            <div className="text-sm text-muted-foreground">
              <strong>What you can do:</strong>
            </div>
            <ul className="text-sm text-muted-foreground space-y-1 ml-4">
              <li>• Browse all 1,600 components and flows</li>
              <li>• Search and filter by categories</li>
              <li>• Preview components before downloading</li>
              <li>• Download as JSON files for immediate use</li>
              <li>• Import directly into your flows</li>
            </ul>
          </div>

          <div className="pt-4">
            <Button
              onClick={() => navigate("/showcase")}
              className="w-full"
              size="lg"
            >
              <ForwardedIconComponent name="ExternalLink" className="mr-2 h-4 w-4" />
              Open Component Showcase
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default StoreApiKeyPage;
