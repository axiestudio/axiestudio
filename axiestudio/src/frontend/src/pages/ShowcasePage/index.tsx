import { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../../components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select";
import { Checkbox } from "../../components/ui/checkbox";
import { Label } from "../../components/ui/label";

import IconComponent from "../../components/common/genericIconComponent";
import ShadTooltip from "../../components/common/shadTooltipComponent";
import { cn } from "../../utils/utils";
import { api } from "../../controllers/API";
import useAlertStore from "../../stores/alertStore";
import { useFavoritesStore } from "../../stores/favoritesStore";

interface StoreItem {
  id: string;
  name: string;
  description: string;
  type: "FLOW" | "COMPONENT";
  author: {
    username: string;
    full_name?: string;
  };
  stats: {
    downloads: number;
    likes: number;
  };
  dates: {
    created: string;
    updated: string;
  };
  tags: Array<{
    tags_id: {
      name: string;
      id: string;
    };
  }>;
  technical?: {
    last_tested_version?: string;
    private?: boolean;
  };
}

interface StoreData {
  flows: StoreItem[];
  components: StoreItem[];
  summary: {
    total_items: number;
    total_flows: number;
    total_components: number;
  };
}

export default function ShowcasePage(): JSX.Element {
  const navigate = useNavigate();
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  
  const [storeData, setStoreData] = useState<StoreData | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("popular");
  const [activeTab, setActiveTab] = useState("all");
  const [downloadingItems, setDownloadingItems] = useState<Set<string>>(new Set());
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [authorFilter, setAuthorFilter] = useState("");
  const [showPrivateOnly, setShowPrivateOnly] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(24); // Show 24 items per page for better performance

  useEffect(() => {
    loadStoreData();
  }, []);

  const loadStoreData = async () => {
    try {
      setLoading(true);

      // FRONTEND-ONLY SOLUTION: Load store data directly from static files
      console.log('Loading store data from frontend files...');
      const response = await fetch('/store_components_converted/store_index.json');

      if (!response.ok) {
        throw new Error(`Failed to load store data: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Successfully loaded store data:', {
        total_items: data.summary?.total_items || 0,
        flows: data.summary?.total_flows || 0,
        components: data.summary?.total_components || 0
      });

      // Debug: Log first few items to verify structure
      if (data.flows && data.flows.length > 0) {
        console.log('Sample flow:', data.flows[0]);
      }
      if (data.components && data.components.length > 0) {
        console.log('Sample component:', data.components[0]);
      }

      setStoreData(data);
    } catch (error) {
      console.error("Failed to load store data:", error);
      setErrorData({
        title: "Misslyckades att ladda utställningsdata",
        list: [
          "Kunde inte ladda butiksdata från frontend-filer",
          "Se till att mappen store_components_converted är tillgänglig",
          error instanceof Error ? error.message : "Okänt fel"
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  // Sanitize filename to match how files were saved
  const sanitizeFilename = (name: string): string => {
    return name
      .replace(/[()]/g, '') // Remove parentheses: "(2)" → "2"
      .replace(/[<>:"/\\|?*]/g, '') // Remove other invalid filename characters
      .replace(/\s*\+\s*/g, '  ') // Replace " + " with double space: " + " → "  "
      .replace(/\s{3,}/g, '  ') // Replace 3+ spaces with double space
      .trim();
  };

  const handleDownload = async (item: StoreItem) => {
    if (downloadingItems.has(item.id)) return;

    setDownloadingItems(prev => new Set(prev).add(item.id));

    try {
      // FRONTEND-ONLY SOLUTION: Load files directly from static folder
      const folder = item.type === "FLOW" ? "flows" : "components";
      // Sanitize the filename to match how files were actually saved
      const sanitizedName = sanitizeFilename(item.name);
      const filePath = `/store_components_converted/${folder}/${item.id}_${sanitizedName}.json`;

      console.log(`Downloading ${item.type}: ${item.name} from ${filePath}`);

      const response = await fetch(filePath);
      if (!response.ok) {
        throw new Error(`Failed to download file: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      // Create download link
      const dataStr = JSON.stringify(data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);

      const link = document.createElement('a');
      link.href = url;
      link.download = `${item.name.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      console.log(`Successfully downloaded: ${item.name}`);
      setSuccessData({
        title: `${item.type === "FLOW" ? "Flöde" : "Komponent"} nedladdat framgångsrikt!`
      });
    } catch (error) {
      console.error("Download failed:", error);
      setErrorData({
        title: "Nedladdning misslyckades",
        list: [
          `Kunde inte ladda ner ${item.name}`,
          error instanceof Error ? error.message : "Okänt fel",
          "Vänligen försök igen senare"
        ]
      });
    } finally {
      setDownloadingItems(prev => {
        const newSet = new Set(prev);
        newSet.delete(item.id);
        return newSet;
      });
    }
  };

  // Get all unique tags for filtering
  const allTags = useMemo(() => {
    if (!storeData) return [];
    const tagSet = new Set<string>();
    [...storeData.flows, ...storeData.components].forEach(item => {
      // Handle items with tags safely
      if (item.tags && Array.isArray(item.tags)) {
        item.tags.forEach(tag => {
          // Ensure tag has the expected structure
          if (tag && tag.tags_id && tag.tags_id.name) {
            tagSet.add(tag.tags_id.name);
          }
        });
      }
    });
    return Array.from(tagSet).sort();
  }, [storeData]);

  // Get all unique authors for filtering
  const allAuthors = useMemo(() => {
    if (!storeData) return [];
    const authorSet = new Set<string>();
    [...storeData.flows, ...storeData.components].forEach(item => {
      // Handle items with author data safely
      if (item.author && item.author.username) {
        authorSet.add(item.author.username);
      }
    });
    return Array.from(authorSet).sort();
  }, [storeData]);

  const getFilteredItems = () => {
    if (!storeData) return [];

    let items: StoreItem[] = [];

    if (activeTab === "all") {
      items = [...storeData.flows, ...storeData.components];
    } else if (activeTab === "flows") {
      items = storeData.flows;
    } else if (activeTab === "components") {
      items = storeData.components;
    }

    // Apply search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      items = items.filter(item =>
        item.name.toLowerCase().includes(searchLower) ||
        item.description.toLowerCase().includes(searchLower) ||
        (item.author?.username && item.author.username.toLowerCase().includes(searchLower)) ||
        (item.tags && Array.isArray(item.tags) && item.tags.some(tag =>
          tag?.tags_id?.name && tag.tags_id.name.toLowerCase().includes(searchLower)
        )) ||
        (item.technical?.last_tested_version && item.technical.last_tested_version.toLowerCase().includes(searchLower))
      );
    }

    // Apply tag filter
    if (selectedTags.length > 0) {
      items = items.filter(item =>
        item.tags && Array.isArray(item.tags) && item.tags.some(tag =>
          tag?.tags_id?.name && selectedTags.includes(tag.tags_id.name)
        )
      );
    }

    // Apply author filter
    if (authorFilter) {
      items = items.filter(item =>
        item.author.username.toLowerCase().includes(authorFilter.toLowerCase())
      );
    }

    // Apply private filter
    if (showPrivateOnly) {
      items = items.filter(item => item.technical?.private === true);
    }

    // Apply sorting
    if (sortBy === "popular") {
      items.sort((a, b) => (b.stats.likes + b.stats.downloads) - (a.stats.likes + a.stats.downloads));
    } else if (sortBy === "recent") {
      items.sort((a, b) => new Date(b.dates.updated).getTime() - new Date(a.dates.updated).getTime());
    } else if (sortBy === "alphabetical") {
      items.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === "downloads") {
      items.sort((a, b) => b.stats.downloads - a.stats.downloads);
    } else if (sortBy === "likes") {
      items.sort((a, b) => b.stats.likes - a.stats.likes);
    }

    return items;
  };

  // Pagination logic
  const filteredItems = getFilteredItems();
  const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
  const paginatedItems = filteredItems.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, selectedTags, authorFilter, showPrivateOnly, activeTab]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center space-y-8 p-8">
          <div className="relative">
            <div className="w-24 h-24 mx-auto bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-2xl">
              <IconComponent name="Library" className="h-12 w-12 text-white" />
            </div>
            <div className="absolute inset-0 w-24 h-24 mx-auto border-4 border-blue-200 rounded-2xl animate-pulse"></div>
          </div>
          <div className="space-y-4">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Laddar Utställning
            </h2>
            <p className="text-lg text-slate-600 max-w-md mx-auto">
              Förbereder över 1600 komponenter och flöden för dig...
            </p>
            <div className="flex items-center justify-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Clean Header */}
      <div className="border-b bg-background sticky top-0 z-50">
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
                Tillbaka till flöde
              </Button>
              <div className="h-6 w-px bg-border" />
              <div>
                <h1 className="text-2xl font-bold">
                  Komponent & Flödesutställning
                </h1>
                <p className="text-sm text-muted-foreground">
                  Upptäck och ladda ner från vår kurerade samling av {storeData?.summary.total_items || 0} professionella resurser
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                onClick={() => navigate("/favorites")}
                className="flex items-center gap-2"
              >
                <IconComponent name="Heart" className="h-4 w-4" />
                Mina favoriter
                {useFavoritesStore.getState().favorites.length > 0 && (
                  <Badge variant="destructive" className="ml-1 h-5 w-5 rounded-full p-0 text-xs flex items-center justify-center">
                    {useFavoritesStore.getState().favorites.length}
                  </Badge>
                )}
              </Button>
              <div className="flex items-center gap-2">
                <Badge variant="secondary" className="px-3 py-1">
                  <IconComponent name="ToyBrick" className="h-3 w-3 mr-1" />
                  {storeData?.summary.total_components || 0} Komponenter
                </Badge>
                <Badge variant="secondary" className="px-3 py-1">
                  <IconComponent name="Workflow" className="h-3 w-3 mr-1" />
                  {storeData?.summary.total_flows || 0} Flöden
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Clean Filters Section */}
      <div className="border-b bg-background">
        <div className="container mx-auto px-6 py-4">
          <div className="flex flex-wrap items-center gap-4">
            <div className="relative flex-1 min-w-[300px] max-w-md">
              <IconComponent name="Search" className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Sök komponenter, flöden, författare..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
              {searchTerm && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSearchTerm("")}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 p-0"
                >
                  <IconComponent name="X" className="h-3 w-3" />
                </Button>
              )}
            </div>

            <div className="relative min-w-[200px]">
              <IconComponent name="User" className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Filtrera efter författare..."
                value={authorFilter}
                onChange={(e) => setAuthorFilter(e.target.value)}
                className="pl-10"
              />
            </div>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-48">
                <IconComponent name="ArrowUpDown" className="h-4 w-4 mr-2 text-muted-foreground" />
                <SelectValue placeholder="Sortera efter..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="popular">
                  <div className="flex items-center gap-2">
                    <IconComponent name="TrendingUp" className="h-4 w-4" />
                    Populära
                  </div>
                </SelectItem>
                <SelectItem value="recent">
                  <div className="flex items-center gap-2">
                    <IconComponent name="Clock" className="h-4 w-4" />
                    Senaste
                  </div>
                </SelectItem>
                <SelectItem value="alphabetical">
                  <div className="flex items-center gap-2">
                    <IconComponent name="SortAsc" className="h-4 w-4" />
                    Alfabetisk
                  </div>
                </SelectItem>
                <SelectItem value="downloads">
                  <div className="flex items-center gap-2">
                    <IconComponent name="Download" className="h-4 w-4" />
                    Nedladdningar
                  </div>
                </SelectItem>
                <SelectItem value="likes">
                  <div className="flex items-center gap-2">
                    <IconComponent name="Heart" className="h-4 w-4" />
                    Gillningar
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="private-only"
                checked={showPrivateOnly}
                onCheckedChange={(checked) => setShowPrivateOnly(checked === true)}
              />
              <Label htmlFor="private-only" className="text-sm cursor-pointer flex items-center gap-1">
                <IconComponent name="Lock" className="h-3 w-3" />
                Endast Privata
              </Label>
            </div>
          </div>

          {/* Tag Filters */}
          {allTags.length > 0 && (
            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between">
                <Label className="text-sm font-medium flex items-center gap-2">
                  <IconComponent name="Tag" className="h-4 w-4" />
                  Filtrera efter taggar ({selectedTags.length} valda)
                </Label>
                {selectedTags.length > 0 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSelectedTags([])}
                    className="text-xs h-7 px-2"
                  >
                    <IconComponent name="X" className="h-3 w-3 mr-1" />
                    Rensa alla
                  </Button>
                )}
              </div>
              <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto p-3 border rounded-lg">
                {allTags.slice(0, 40).map((tag) => (
                  <Badge
                    key={tag}
                    variant={selectedTags.includes(tag) ? "default" : "outline"}
                    className="cursor-pointer text-xs"
                    onClick={() => {
                      setSelectedTags(prev =>
                        prev.includes(tag)
                          ? prev.filter(t => t !== tag)
                          : [...prev, tag]
                      );
                    }}
                  >
                    {tag}
                    {selectedTags.includes(tag) && (
                      <IconComponent name="Check" className="h-3 w-3 ml-1" />
                    )}
                  </Badge>
                ))}
                {allTags.length > 40 && (
                  <Badge variant="outline" className="text-xs">
                    +{allTags.length - 40} fler taggar
                  </Badge>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        <div className="container mx-auto px-6 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <div className="flex items-center justify-between">
            <TabsList>
              <TabsTrigger value="all">
                <IconComponent name="Grid3X3" className="h-4 w-4 mr-2" />
                Alla ({filteredItems.length})
              </TabsTrigger>
              <TabsTrigger value="flows">
                <IconComponent name="Workflow" className="h-4 w-4 mr-2" />
                Flöden ({storeData?.flows.length || 0})
              </TabsTrigger>
              <TabsTrigger value="components">
                <IconComponent name="ToyBrick" className="h-4 w-4 mr-2" />
                Komponenter ({storeData?.components.length || 0})
              </TabsTrigger>
            </TabsList>

            {/* Results Info */}
            <div className="flex items-center gap-4">
              <p className="text-sm text-muted-foreground">
                Visar <span className="font-medium">{paginatedItems.length}</span> av <span className="font-medium">{filteredItems.length}</span> objekt
                {filteredItems.length !== (storeData?.summary.total_items || 0) &&
                  ` (filtrerat från ${storeData?.summary.total_items || 0} totalt)`
                }
              </p>
              {totalPages > 1 && (
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                    disabled={currentPage === 1}
                  >
                    <IconComponent name="ChevronLeft" className="h-4 w-4" />
                  </Button>
                  <span className="text-sm px-3 py-1 text-muted-foreground">
                    {currentPage} / {totalPages}
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                    disabled={currentPage === totalPages}
                  >
                    <IconComponent name="ChevronRight" className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>
          </div>

          <TabsContent value={activeTab} className="space-y-6">
            {/* Items Grid */}
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5">
              {paginatedItems.map((item) => (
                <ShowcaseCard
                  key={item.id}
                  item={item}
                  onDownload={() => handleDownload(item)}
                  isDownloading={downloadingItems.has(item.id)}
                />
              ))}
            </div>

            {filteredItems.length === 0 && (
              <div className="flex h-96 items-center justify-center">
                <div className="text-center space-y-6 p-8">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-r from-slate-200 to-slate-300 rounded-2xl flex items-center justify-center">
                    <IconComponent name="Search" className="h-12 w-12 text-slate-400" />
                  </div>
                  <div className="space-y-3">
                    <h3 className="text-xl font-semibold text-slate-700">Inga resultat hittades</h3>
                    <p className="text-slate-500 max-w-md">
                      Vi kunde inte hitta några objekt som matchar dina sökkriterier. Prova att justera dina filter.
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSearchTerm("");
                      setSelectedTags([]);
                      setAuthorFilter("");
                      setShowPrivateOnly(false);
                    }}
                    className="rounded-xl border-slate-300 hover:bg-slate-50"
                  >
                    <IconComponent name="RotateCcw" className="h-4 w-4 mr-2" />
                    Rensa alla filter
                  </Button>
                </div>
              </div>
            )}

            {/* Bottom Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center pt-8">
                <div className="flex items-center gap-2 bg-white/60 p-2 rounded-xl shadow-sm">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(1)}
                    disabled={currentPage === 1}
                    className="rounded-lg border-slate-300 hover:bg-slate-50"
                  >
                    Första
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                    disabled={currentPage === 1}
                    className="rounded-lg border-slate-300 hover:bg-slate-50"
                  >
                    <IconComponent name="ChevronLeft" className="h-4 w-4" />
                  </Button>
                  <span className="text-sm px-4 py-2 bg-white rounded-lg text-slate-600 font-medium">
                    Sida {currentPage} av {totalPages}
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                    disabled={currentPage === totalPages}
                    className="rounded-lg border-slate-300 hover:bg-slate-50"
                  >
                    <IconComponent name="ChevronRight" className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(totalPages)}
                    disabled={currentPage === totalPages}
                    className="rounded-lg border-slate-300 hover:bg-slate-50"
                  >
                    Sista
                  </Button>
                </div>
              </div>
            )}
          </TabsContent>
        </Tabs>
        </div>
      </div>
    </div>
  );
}

interface ShowcaseCardProps {
  item: StoreItem;
  onDownload: () => void;
  isDownloading: boolean;
}

function ShowcaseCard({ item, onDownload, isDownloading }: ShowcaseCardProps) {
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavoritesStore();
  const isItemFavorite = isFavorite(item.id);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const handleToggleFavorite = () => {
    if (isItemFavorite) {
      removeFromFavorites(item.id);
    } else {
      addToFavorites(item);
    }
  };

  return (
    <Card className="group relative flex h-[420px] flex-col justify-between overflow-hidden hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300 hover:-translate-y-2 bg-white/80 backdrop-blur-sm border-slate-200 hover:border-blue-300 rounded-2xl">
      {/* Gradient Header */}
      <div className={cn(
        "absolute inset-x-0 top-0 h-2 bg-gradient-to-r",
        item.type === "COMPONENT" 
          ? "from-blue-500 to-purple-500" 
          : "from-indigo-500 to-blue-500"
      )} />

      <CardHeader className="pb-4 space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className={cn(
              "p-3 rounded-xl shadow-sm",
              item.type === "COMPONENT"
                ? "bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600"
                : "bg-gradient-to-r from-indigo-100 to-blue-100 text-indigo-600"
            )}>
              <IconComponent
                name={item.type === "COMPONENT" ? "ToyBrick" : "Group"}
                className="h-5 w-5"
              />
            </div>
            <Badge
              variant={item.type === "COMPONENT" ? "default" : "secondary"}
              className={cn(
                "text-xs font-semibold px-3 py-1 rounded-full",
                item.type === "COMPONENT" 
                  ? "bg-blue-500 text-white" 
                  : "bg-indigo-500 text-white"
              )}
            >
              {item.type === "COMPONENT" ? "KOMPONENT" : "FLÖDE"}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            {item.technical?.private && (
              <ShadTooltip content="Privat komponent">
                <div className="p-1.5 bg-amber-100 rounded-lg">
                  <IconComponent name="Lock" className="h-3 w-3 text-amber-600" />
                </div>
              </ShadTooltip>
            )}
            {item.stats.likes > 10 && (
              <ShadTooltip content="Populär komponent">
                <div className="p-1.5 bg-yellow-100 rounded-lg">
                  <IconComponent name="Star" className="h-3 w-3 text-yellow-600" />
                </div>
              </ShadTooltip>
            )}
            <ShadTooltip content={isItemFavorite ? "Ta bort från favoriter" : "Lägg till i favoriter"}>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleToggleFavorite}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg transition-all duration-200",
                  isItemFavorite
                    ? "text-red-500 hover:text-red-600 hover:bg-red-50"
                    : "text-gray-400 hover:text-red-500 hover:bg-red-50"
                )}
              >
                <IconComponent
                  name="Heart"
                  className={cn(
                    "h-4 w-4 transition-all duration-200",
                    isItemFavorite && "fill-current"
                  )}
                />
              </Button>
            </ShadTooltip>
          </div>
        </div>

        <div className="space-y-3">
          <CardTitle className="text-lg leading-tight font-bold text-slate-800">
            <ShadTooltip content={item.name}>
              <div className="truncate group-hover:text-blue-600 transition-colors duration-200">
                {item.name}
              </div>
            </ShadTooltip>
          </CardTitle>

          <CardDescription className="line-clamp-3 text-sm leading-relaxed text-slate-600">
            {item.description}
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="flex-1 pb-4 space-y-4">
        {/* Enhanced Stats Row */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <ShadTooltip content={`${item.stats.downloads} nedladdningar`}>
              <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 rounded-lg border border-blue-100">
                <IconComponent name="Download" className="h-3 w-3 text-blue-500" />
                <span className="font-semibold text-blue-700 text-xs">{item.stats.downloads}</span>
              </div>
            </ShadTooltip>
            <ShadTooltip content={`${item.stats.likes} gillningar`}>
              <div className="flex items-center gap-2 px-3 py-1.5 bg-red-50 rounded-lg border border-red-100">
                <IconComponent name="Heart" className="h-3 w-3 text-red-500" />
                <span className="font-semibold text-red-700 text-xs">{item.stats.likes}</span>
              </div>
            </ShadTooltip>
          </div>
          {item.technical?.last_tested_version && (
            <div className="px-2 py-1 bg-green-50 text-green-700 rounded-lg border border-green-200 text-xs font-medium">
              v{item.technical.last_tested_version}
            </div>
          )}
        </div>

        {/* Author & Date Info */}
        <div className="space-y-2 text-xs">
          <div className="flex items-center gap-2 text-slate-500">
            <IconComponent name="User" className="h-3 w-3" />
            <span>Skapad av</span>
            <span className="font-semibold text-slate-700">{item.author.username}</span>
          </div>
          <div className="flex items-center gap-2 text-slate-500">
            <IconComponent name="Calendar" className="h-3 w-3" />
            <span>Uppdaterad {formatDate(item.dates.updated)}</span>
          </div>
        </div>

        {/* Enhanced Tags */}
        {item.tags && Array.isArray(item.tags) && item.tags.length > 0 && (
          <div className="space-y-2">
            <div className="flex flex-wrap gap-1.5">
              {item.tags.slice(0, 3).map((tag, index) =>
                tag?.tags_id?.name ? (
                  <Badge
                    key={tag.tags_id.id || `tag-${index}`}
                    variant="outline"
                    className="text-xs px-2 py-1 hover:bg-slate-50 transition-colors rounded-md border-slate-300 text-slate-600"
                  >
                    {tag.tags_id.name}
                  </Badge>
                ) : null
              )}
              {item.tags.length > 3 && (
                <ShadTooltip content={`${item.tags.length - 3} fler taggar: ${item.tags.slice(3).filter(t => t?.tags_id?.name).map(t => t.tags_id.name).join(', ')}`}>
                  <Badge variant="outline" className="text-xs px-2 py-1 border-slate-300 text-slate-500 rounded-md">
                    +{item.tags.length - 3} fler
                  </Badge>
                </ShadTooltip>
              )}
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter className="pt-4 pb-6">
        <Button
          onClick={onDownload}
          disabled={isDownloading}
          className={cn(
            "w-full group/btn hover:shadow-lg transition-all duration-300 rounded-xl font-semibold",
            item.type === "COMPONENT"
              ? "bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
              : "bg-gradient-to-r from-indigo-500 to-blue-500 hover:from-indigo-600 hover:to-blue-600"
          )}
          size="sm"
        >
          {isDownloading ? (
            <>
              <IconComponent name="Loader2" className="mr-2 h-4 w-4 animate-spin" />
              <span>Laddar ner...</span>
            </>
          ) : (
            <>
              <IconComponent name="Download" className="mr-2 h-4 w-4 group-hover/btn:animate-bounce" />
              <span>Ladda ner JSON</span>
              <IconComponent name="ExternalLink" className="ml-2 h-3 w-3 opacity-0 group-hover/btn:opacity-100 transition-opacity" />
            </>
          )}
        </Button>
      </CardFooter>
    </Card>
  );
}