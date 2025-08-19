import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Search, Filter, Download, Heart, Eye, Calendar, User, Tag } from "lucide-react";
import PageLayout from "@/components/common/pageLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import IconComponent from "@/components/common/genericIconComponent";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import FlowPreviewComponent from "@/components/common/flowPreviewComponent";
import { cn } from "@/utils/utils";

interface StoreItem {
  id: string;
  name: string;
  description: string;
  type: "FLOW" | "COMPONENT";
  author: {
    username: string;
    full_name: string;
  };
  store_url: string;
  stats: {
    downloads: number;
    likes: number;
  };
  dates: {
    created: string;
    updated: string;
    downloaded: string;
  };
  tags: Array<{
    tags_id: {
      name: string;
      id: string;
    };
  }>;
  conversion?: {
    converted_at: string;
    converted_from: string;
    converted_to: string;
    conversions_made: number;
  };
}

interface StoreData {
  summary: {
    total_items: number;
    total_flows: number;
    total_components: number;
    downloaded_at: string;
  };
  flows: StoreItem[];
  components: StoreItem[];
  conversion_info: {
    converted_at: string;
    converted_from: string;
    converted_to: string;
    original_source: string;
  };
}

export default function AxieStudioStorePage(): JSX.Element {
  const { id } = useParams();
  const [storeData, setStoreData] = useState<StoreData | null>(null);
  const [filteredItems, setFilteredItems] = useState<StoreItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedType, setSelectedType] = useState<"ALL" | "FLOW" | "COMPONENT">("ALL");
  const [sortBy, setSortBy] = useState<"popular" | "recent" | "alphabetical" | "downloads">("popular");
  const [selectedItem, setSelectedItem] = useState<StoreItem | null>(null);
  const [showPreview, setShowPreview] = useState(false);

  // Load store data
  useEffect(() => {
    const loadStoreData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/v1/axiestudio-store');
        const data: StoreData = await response.json();
        setStoreData(data);
        
        // Combine flows and components
        const allItems = [...data.flows, ...data.components];
        setFilteredItems(allItems);
      } catch (error) {
        console.error('Failed to load store data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStoreData();
  }, []);

  // Filter and sort items
  useEffect(() => {
    if (!storeData) return;

    let items = [...storeData.flows, ...storeData.components];

    // Filter by type
    if (selectedType !== "ALL") {
      items = items.filter(item => item.type === selectedType);
    }

    // Filter by search term
    if (searchTerm) {
      items = items.filter(item =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.author.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.tags.some(tag => tag.tags_id.name.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Sort items
    items.sort((a, b) => {
      switch (sortBy) {
        case "popular":
          return (b.stats.likes + b.stats.downloads) - (a.stats.likes + a.stats.downloads);
        case "recent":
          return new Date(b.dates.updated).getTime() - new Date(a.dates.updated).getTime();
        case "downloads":
          return b.stats.downloads - a.stats.downloads;
        case "alphabetical":
          return a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });

    setFilteredItems(items);
  }, [storeData, searchTerm, selectedType, sortBy]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const handleItemClick = (item: StoreItem) => {
    setSelectedItem(item);
    setShowPreview(true);
  };

  const handleClosePreview = () => {
    setShowPreview(false);
    setSelectedItem(null);
  };

  const handleImport = async (item: StoreItem) => {
    try {
      const response = await fetch(`/api/v1/axiestudio-store/${item.type.toLowerCase()}/${item.id}`);
      const itemData = await response.json();
      
      // Here you would integrate with your flow import logic
      console.log('Importing item:', itemData);
      
      // Show success message
      alert(`Successfully imported ${item.name}!`);
    } catch (error) {
      console.error('Failed to import item:', error);
      alert('Failed to import item. Please try again.');
    }
  };

  if (loading) {
    return (
      <PageLayout
        title="AxieStudio Store"
        description="Browse and import components and flows from the AxieStudio Store"
      >
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="AxieStudio Store"
      description="Browse and import components and flows from the AxieStudio Store"
    >
      <div className="space-y-6">
        {/* Header Stats */}
        {storeData && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Total Items</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{storeData.summary.total_items}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Flows</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{storeData.summary.total_flows}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Components</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{storeData.summary.total_components}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Last Updated</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-sm">{formatDate(storeData.conversion_info.converted_at)}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Search and Filters */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <Input
              placeholder="Search flows and components..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <Select value={selectedType} onValueChange={(value: any) => setSelectedType(value)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="All Types" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ALL">All Types</SelectItem>
              <SelectItem value="FLOW">Flows</SelectItem>
              <SelectItem value="COMPONENT">Components</SelectItem>
            </SelectContent>
          </Select>

          <Select value={sortBy} onValueChange={(value: any) => setSortBy(value)}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="popular">Popular</SelectItem>
              <SelectItem value="recent">Most Recent</SelectItem>
              <SelectItem value="downloads">Most Downloaded</SelectItem>
              <SelectItem value="alphabetical">Alphabetical</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Results */}
        <div className="text-sm text-muted-foreground">
          Showing {filteredItems.length} of {storeData?.summary.total_items || 0} items
        </div>

        {/* Items Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map((item) => (
            <Card key={item.id} className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg line-clamp-1">{item.name}</CardTitle>
                    <CardDescription className="line-clamp-2 mt-1">
                      {item.description}
                    </CardDescription>
                  </div>
                  <Badge variant={item.type === "FLOW" ? "default" : "secondary"}>
                    {item.type}
                  </Badge>
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-3">
                  {/* Author */}
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <User className="h-4 w-4" />
                    <span>{item.author.full_name || item.author.username}</span>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Download className="h-4 w-4" />
                      <span>{item.stats.downloads}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Heart className="h-4 w-4" />
                      <span>{item.stats.likes}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-4 w-4" />
                      <span>{formatDate(item.dates.updated)}</span>
                    </div>
                  </div>

                  {/* Tags */}
                  {item.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {item.tags.slice(0, 3).map((tag) => (
                        <Badge key={tag.tags_id.id} variant="outline" className="text-xs">
                          {tag.tags_id.name}
                        </Badge>
                      ))}
                      {item.tags.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{item.tags.length - 3}
                        </Badge>
                      )}
                    </div>
                  )}
                </div>
              </CardContent>

              <CardFooter className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleItemClick(item)}
                  className="flex-1"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  Preview
                </Button>
                <Button
                  size="sm"
                  onClick={() => handleImport(item)}
                  className="flex-1"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Import
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Empty State */}
        {filteredItems.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-muted-foreground">
              No items found matching your criteria.
            </div>
          </div>
        )}

        {/* Flow Preview Modal */}
        {selectedItem && (
          <FlowPreviewComponent
            isOpen={showPreview}
            onClose={handleClosePreview}
            item={selectedItem}
            onImport={handleImport}
          />
        )}
      </div>
    </PageLayout>
  );
}
