import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import IconComponent from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import { useFavoritesStore } from "@/stores/favoritesStore";
import { cn } from "@/utils/utils";

export default function FavoritesPage(): JSX.Element {
  const navigate = useNavigate();
  const { favorites, removeFromFavorites, clearFavorites, getFavoritesByType } = useFavoritesStore();
  const [activeTab, setActiveTab] = useState("all");


  const getFilteredFavorites = () => {
    switch (activeTab) {
      case "flows":
        return getFavoritesByType("FLOW");
      case "components":
        return getFavoritesByType("COMPONENT");
      default:
        return favorites;
    }
  };

  const filteredFavorites = getFilteredFavorites();

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-50 border-b bg-background">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate("/flow")}
                className="flex items-center gap-2"
              >
                <IconComponent name="ArrowLeft" className="h-4 w-4" />
                Tillbaka
              </Button>
              <div className="h-6 w-px bg-border" />
              <div>
                <h1 className="text-2xl font-bold flex items-center gap-2">
                  <IconComponent name="Heart" className="h-5 w-5" />
                  Mina favoriter
                </h1>
                <p className="text-sm text-muted-foreground">
                  {favorites.length} sparade komponenter och flöden
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <IconComponent name="HardDrive" className="h-3 w-3 text-amber-500" />
                  <span className="text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded-md border border-amber-200">
                    Favoriter sparade lokalt
                  </span>
                </div>
              </div>
            </div>
            {favorites.length > 0 && (
              <Button
                variant="outline"
                onClick={clearFavorites}
                className="flex items-center gap-2"
              >
                <IconComponent name="Trash2" className="h-4 w-4" />
                Rensa alla favoriter
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        <div className="container mx-auto px-6 py-6">
        {favorites.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="p-4 bg-muted/50 rounded-full mb-4">
              <IconComponent name="Heart" className="h-12 w-12 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Inga favoriter än</h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              Börja utforska komponenter och flöden och lägg till dina favoriter genom att klicka på hjärtikonen.
            </p>
            <Button
              onClick={() => navigate("/showcase")}
              className="flex items-center gap-2"
            >
              <IconComponent name="Library" className="h-4 w-4" />
              Utforska biblioteket
            </Button>
          </div>
        ) : (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <div className="flex items-center justify-between mb-6">
              <TabsList className="grid w-auto grid-cols-3">
                <TabsTrigger value="all">
                  Alla ({favorites.length})
                </TabsTrigger>
                <TabsTrigger value="flows">
                  Flöden ({getFavoritesByType("FLOW").length})
                </TabsTrigger>
                <TabsTrigger value="components">
                  Komponenter ({getFavoritesByType("COMPONENT").length})
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value={activeTab} className="space-y-6">
              <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6">
                {filteredFavorites.map((item) => (
                  <FavoriteCard
                    key={item.id}
                    item={item}
                    onRemove={() => removeFromFavorites(item.id)}
                  />
                ))}
              </div>
            </TabsContent>
          </Tabs>
        )}
        </div>
      </div>
    </div>
  );
}

interface FavoriteCardProps {
  item: any;
  onRemove: () => void;
}

function FavoriteCard({ item, onRemove }: FavoriteCardProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('sv-SE');
  };

  return (
    <Card className="group relative flex h-96 flex-col justify-between overflow-hidden hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-1 border-muted-foreground/20 hover:border-primary/30">
      {/* Header with gradient background */}
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-red-500/50 to-pink-500/50" />

      <CardHeader className="pb-3 space-y-3">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <div className={cn(
              "p-2 rounded-lg",
              item.type === "COMPONENT"
                ? "bg-blue-500/10 text-blue-600"
                : "bg-green-500/10 text-green-600"
            )}>
              <IconComponent
                name={item.type === "COMPONENT" ? "ToyBrick" : "Workflow"}
                className="h-4 w-4"
              />
            </div>
            <Badge
              variant={item.type === "COMPONENT" ? "default" : "secondary"}
              className="text-xs font-medium"
            >
              {item.type === "COMPONENT" ? "KOMPONENT" : "FLÖDE"}
            </Badge>
          </div>
          <ShadTooltip content="Ta bort från favoriter">
            <Button
              variant="ghost"
              size="sm"
              onClick={onRemove}
              className="h-8 w-8 p-0 text-red-500 hover:text-red-600 hover:bg-red-50"
            >
              <IconComponent name="Heart" className="h-4 w-4 fill-current" />
            </Button>
          </ShadTooltip>
        </div>

        <div className="space-y-2">
          <CardTitle className="text-lg leading-tight font-semibold">
            <ShadTooltip content={item.name}>
              <div className="truncate group-hover:text-primary transition-colors">
                {item.name}
              </div>
            </ShadTooltip>
          </CardTitle>

          <CardDescription className="line-clamp-3 text-sm leading-relaxed">
            {item.description}
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="flex-1 pb-3 space-y-4">
        {/* Stats Row */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 text-xs">
            <ShadTooltip content={`${item.stats.downloads} nedladdningar`}>
              <div className="flex items-center gap-1 px-2 py-1 bg-muted/50 rounded-md">
                <IconComponent name="Download" className="h-3 w-3 text-blue-500" />
                <span className="font-medium">{item.stats.downloads}</span>
              </div>
            </ShadTooltip>
            <ShadTooltip content={`${item.stats.likes} gillningar`}>
              <div className="flex items-center gap-1 px-2 py-1 bg-muted/50 rounded-md">
                <IconComponent name="Heart" className="h-3 w-3 text-red-500" />
                <span className="font-medium">{item.stats.likes}</span>
              </div>
            </ShadTooltip>
          </div>
        </div>

        {/* Author & Date Info */}
        <div className="space-y-1 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <IconComponent name="User" className="h-3 w-3" />
            <span>av</span>
            <span className="font-medium text-foreground">{item.author.username}</span>
          </div>
          <div className="flex items-center gap-1">
            <IconComponent name="Heart" className="h-3 w-3 text-red-500" />
            <span>Tillagd {formatDate(item.addedToFavoritesAt)}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
