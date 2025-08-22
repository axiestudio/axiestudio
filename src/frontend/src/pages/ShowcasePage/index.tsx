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
import { Separator } from "../../components/ui/separator";
import IconComponent from "../../components/common/genericIconComponent";
import ShadTooltip from "../../components/common/shadTooltipComponent";
import { cn } from "../../utils/utils";
import { api } from "../../controllers/API";
import useAlertStore from "../../stores/alertStore";

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
      console.log('🔄 Loading store data from frontend files...');
      const response = await fetch('/store_components_converted/store_index.json');

      if (!response.ok) {
        throw new Error(`Failed to load store data: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Successfully loaded store data:', {
        total_items: data.summary?.total_items || 0,
        flows: data.summary?.total_flows || 0,
        components: data.summary?.total_components || 0
      });

      // Debug: Log first few items to verify structure
      if (data.flows && data.flows.length > 0) {
        console.log('📋 Sample flow:', data.flows[0]);
      }
      if (data.components && data.components.length > 0) {
        console.log('🧩 Sample component:', data.components[0]);
      }

      setStoreData(data);
    } catch (error) {
      console.error("❌ Failed to load store data:", error);
      setErrorData({
        title: "Failed to load showcase data",
        list: [
          "Could not load store data from frontend files",
          "Please ensure store_components_converted folder is accessible",
          error instanceof Error ? error.message : "Unknown error"
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (item: StoreItem) => {
    if (downloadingItems.has(item.id)) return;

    setDownloadingItems(prev => new Set(prev).add(item.id));

    try {
      // FRONTEND-ONLY SOLUTION: Load files directly from static folder
      const folder = item.type === "FLOW" ? "flows" : "components";
      // Use the exact name as it appears in the store index
      const filePath = `/store_components_converted/${folder}/${item.id}_${item.name}.json`;

      console.log(`🔄 Downloading ${item.type}: ${item.name} from ${filePath}`);

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

      console.log(`✅ Successfully downloaded: ${item.name}`);
      setSuccessData({
        title: `${item.type === "FLOW" ? "Flow" : "Component"} downloaded successfully!`
      });
    } catch (error) {
      console.error("❌ Download failed:", error);
      setErrorData({
        title: "Download failed",
        list: [
          `Could not download ${item.name}`,
          error instanceof Error ? error.message : "Unknown error",
          "Please try again later"
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
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="relative">
            <IconComponent name="Library" className="h-16 w-16 text-muted-foreground/30" />
            <IconComponent name="Loader2" className="absolute inset-0 h-16 w-16 animate-spin text-primary" />
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">Loading Showcase</h3>
            <p className="text-sm text-muted-foreground">
              Preparing 1600+ components and flows for you...
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate("/flow")}
                className="flex items-center gap-2 hover:bg-muted/50 transition-colors"
              >
                <IconComponent name="ArrowLeft" className="h-4 w-4" />
                Back to Flow
              </Button>
              <div className="space-y-1">
                <div className="flex items-center gap-3">
                  <IconComponent name="Library" className="h-8 w-8 text-primary" />
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
                    Component & Flow Showcase
                  </h1>
                </div>
                <p className="text-muted-foreground text-lg">
                  Discover and download from our collection of {storeData?.summary.total_items || 0} professional components and flows
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="px-3 py-1">
                    <IconComponent name="ToyBrick" className="h-3 w-3 mr-1" />
                    {storeData?.summary.total_components || 0} Components
                  </Badge>
                  <Badge variant="secondary" className="px-3 py-1">
                    <IconComponent name="Group" className="h-3 w-3 mr-1" />
                    {storeData?.summary.total_flows || 0} Flows
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground">
                  Updated {storeData?.summary.downloaded_at ? new Date(storeData.summary.downloaded_at).toLocaleDateString() : 'recently'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Filters */}
      <div className="border-b bg-muted/30 backdrop-blur">
        <div className="container mx-auto px-4 py-4 space-y-4">
          <div className="flex flex-wrap items-center gap-4">
            <div className="relative flex-1 min-w-[300px] max-w-md">
              <IconComponent name="Search" className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search components and flows..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-background/50 border-muted-foreground/20 focus:border-primary transition-colors"
              />
              {searchTerm && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSearchTerm("")}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 p-0 hover:bg-muted"
                >
                  <IconComponent name="X" className="h-3 w-3" />
                </Button>
              )}
            </div>

            <div className="relative min-w-[200px]">
              <IconComponent name="User" className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Filter by author..."
                value={authorFilter}
                onChange={(e) => setAuthorFilter(e.target.value)}
                className="pl-10 bg-background/50 border-muted-foreground/20 focus:border-primary transition-colors"
              />
            </div>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-44 bg-background/50 border-muted-foreground/20">
                <IconComponent name="ArrowUpDown" className="h-4 w-4 mr-2" />
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="popular">
                  <div className="flex items-center gap-2">
                    <IconComponent name="TrendingUp" className="h-4 w-4" />
                    Popular
                  </div>
                </SelectItem>
                <SelectItem value="recent">
                  <div className="flex items-center gap-2">
                    <IconComponent name="Clock" className="h-4 w-4" />
                    Recent
                  </div>
                </SelectItem>
                <SelectItem value="alphabetical">
                  <div className="flex items-center gap-2">
                    <IconComponent name="SortAsc" className="h-4 w-4" />
                    Alphabetical
                  </div>
                </SelectItem>
                <SelectItem value="downloads">
                  <div className="flex items-center gap-2">
                    <IconComponent name="Download" className="h-4 w-4" />
                    Downloads
                  </div>
                </SelectItem>
                <SelectItem value="likes">
                  <div className="flex items-center gap-2">
                    <IconComponent name="Heart" className="h-4 w-4" />
                    Likes
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>

            <div className="flex items-center space-x-2 bg-background/50 rounded-md px-3 py-2 border border-muted-foreground/20">
              <Checkbox
                id="private-only"
                checked={showPrivateOnly}
                onCheckedChange={setShowPrivateOnly}
              />
              <Label htmlFor="private-only" className="text-sm cursor-pointer">
                <IconComponent name="Lock" className="h-3 w-3 inline mr-1" />
                Private only
              </Label>
            </div>
          </div>

          {/* Tag Filters */}
          {allTags.length > 0 && (
            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between">
                <Label className="text-sm font-medium flex items-center gap-2">
                  <IconComponent name="Tag" className="h-4 w-4" />
                  Filter by tags ({selectedTags.length} selected)
                </Label>
                {selectedTags.length > 0 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSelectedTags([])}
                    className="text-xs h-6 px-2"
                  >
                    <IconComponent name="X" className="h-3 w-3 mr-1" />
                    Clear
                  </Button>
                )}
              </div>
              <div className="flex flex-wrap gap-2 max-h-24 overflow-y-auto p-2 bg-background/30 rounded-md border border-muted-foreground/10">
                {allTags.slice(0, 30).map((tag) => (
                  <Badge
                    key={tag}
                    variant={selectedTags.includes(tag) ? "default" : "outline"}
                    className="cursor-pointer text-xs hover:scale-105 transition-transform"
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
                {allTags.length > 30 && (
                  <Badge variant="outline" className="text-xs">
                    +{allTags.length - 30} more
                  </Badge>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full">
          <div className="border-b px-4">
            <TabsList>
              <TabsTrigger value="all">All ({filteredItems.length})</TabsTrigger>
              <TabsTrigger value="flows">Flows ({storeData?.flows.length || 0})</TabsTrigger>
              <TabsTrigger value="components">Components ({storeData?.components.length || 0})</TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value={activeTab} className="h-full overflow-auto">
            <div className="p-4 space-y-4">
              {/* Results Info */}
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Showing {paginatedItems.length} of {filteredItems.length} items
                  {filteredItems.length !== (storeData?.summary.total_items || 0) &&
                    ` (filtered from ${storeData?.summary.total_items || 0} total)`
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
                      Previous
                    </Button>
                    <span className="text-sm">
                      Page {currentPage} of {totalPages}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                      disabled={currentPage === totalPages}
                    >
                      Next
                    </Button>
                  </div>
                )}
              </div>

              {/* Items Grid */}
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
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
                <div className="flex h-64 items-center justify-center text-muted-foreground">
                  <div className="text-center">
                    <IconComponent name="Search" className="mx-auto h-12 w-12 mb-4" />
                    <p>No items found matching your filters.</p>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setSearchTerm("");
                        setSelectedTags([]);
                        setAuthorFilter("");
                        setShowPrivateOnly(false);
                      }}
                      className="mt-2"
                    >
                      Clear all filters
                    </Button>
                  </div>
                </div>
              )}

              {/* Bottom Pagination */}
              {totalPages > 1 && (
                <div className="flex justify-center pt-4">
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(1)}
                      disabled={currentPage === 1}
                    >
                      First
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                      disabled={currentPage === 1}
                    >
                      Previous
                    </Button>
                    <span className="text-sm px-4">
                      Page {currentPage} of {totalPages}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                      disabled={currentPage === totalPages}
                    >
                      Next
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(totalPages)}
                      disabled={currentPage === totalPages}
                    >
                      Last
                    </Button>
                  </div>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
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
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <Card className="group relative flex h-96 flex-col justify-between overflow-hidden hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-1 border-muted-foreground/20 hover:border-primary/30">
      {/* Header with gradient background */}
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-primary/50 to-primary/20" />

      <CardHeader className="pb-3 space-y-3">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <div className={cn(
              "p-2 rounded-lg",
              item.type === "COMPONENT"
                ? "bg-component-icon/10 text-component-icon"
                : "bg-flow-icon/10 text-flow-icon"
            )}>
              <IconComponent
                name={item.type === "COMPONENT" ? "ToyBrick" : "Group"}
                className="h-4 w-4"
              />
            </div>
            <Badge
              variant={item.type === "COMPONENT" ? "default" : "secondary"}
              className="text-xs font-medium"
            >
              {item.type}
            </Badge>
          </div>
          <div className="flex items-center gap-1">
            {item.technical?.private && (
              <ShadTooltip content="Private component">
                <IconComponent name="Lock" className="h-4 w-4 text-amber-500" />
              </ShadTooltip>
            )}
            {item.stats.likes > 10 && (
              <ShadTooltip content="Popular component">
                <IconComponent name="Star" className="h-4 w-4 text-yellow-500" />
              </ShadTooltip>
            )}
          </div>
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
            <ShadTooltip content={`${item.stats.downloads} downloads`}>
              <div className="flex items-center gap-1 px-2 py-1 bg-muted/50 rounded-md">
                <IconComponent name="Download" className="h-3 w-3 text-blue-500" />
                <span className="font-medium">{item.stats.downloads}</span>
              </div>
            </ShadTooltip>
            <ShadTooltip content={`${item.stats.likes} likes`}>
              <div className="flex items-center gap-1 px-2 py-1 bg-muted/50 rounded-md">
                <IconComponent name="Heart" className="h-3 w-3 text-red-500" />
                <span className="font-medium">{item.stats.likes}</span>
              </div>
            </ShadTooltip>
          </div>
          <div className="text-xs text-muted-foreground">
            {item.technical?.last_tested_version && (
              <span className="px-2 py-1 bg-green-500/10 text-green-700 dark:text-green-400 rounded-md">
                v{item.technical.last_tested_version}
              </span>
            )}
          </div>
        </div>

        {/* Author & Date Info */}
        <div className="space-y-1 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <IconComponent name="User" className="h-3 w-3" />
            <span>by</span>
            <span className="font-medium text-foreground">{item.author.username}</span>
          </div>
          <div className="flex items-center gap-1">
            <IconComponent name="Calendar" className="h-3 w-3" />
            <span>Updated {formatDate(item.dates.updated)}</span>
          </div>
        </div>

        {/* Tags */}
        {item.tags && Array.isArray(item.tags) && item.tags.length > 0 && (
          <div className="space-y-1">
            <div className="flex flex-wrap gap-1">
              {item.tags.slice(0, 3).map((tag, index) =>
                tag?.tags_id?.name ? (
                  <Badge
                    key={tag.tags_id.id || `tag-${index}`}
                    variant="outline"
                    className="text-xs px-2 py-0.5 hover:bg-primary/10 transition-colors"
                  >
                    {tag.tags_id.name}
                  </Badge>
                ) : null
              )}
              {item.tags.length > 3 && (
                <ShadTooltip content={`${item.tags.length - 3} more tags: ${item.tags.slice(3).filter(t => t?.tags_id?.name).map(t => t.tags_id.name).join(', ')}`}>
                  <Badge variant="outline" className="text-xs px-2 py-0.5">
                    +{item.tags.length - 3}
                  </Badge>
                </ShadTooltip>
              )}
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter className="pt-3 pb-4">
        <Button
          onClick={onDownload}
          disabled={isDownloading}
          className="w-full group/btn hover:shadow-md transition-all duration-200 bg-gradient-to-r from-primary to-primary/90 hover:from-primary/90 hover:to-primary"
          size="sm"
        >
          {isDownloading ? (
            <>
              <IconComponent name="Loader2" className="mr-2 h-4 w-4 animate-spin" />
              <span>Downloading...</span>
            </>
          ) : (
            <>
              <IconComponent name="Download" className="mr-2 h-4 w-4 group-hover/btn:animate-bounce" />
              <span>Download JSON</span>
              <IconComponent name="ExternalLink" className="ml-2 h-3 w-3 opacity-0 group-hover/btn:opacity-100 transition-opacity" />
            </>
          )}
        </Button>
      </CardFooter>
    </Card>
  );
}
