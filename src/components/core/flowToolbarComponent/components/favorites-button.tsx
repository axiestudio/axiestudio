import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import ShadTooltip from "@/components/common/shadTooltipComponent";
import ForwardedIconComponent from "@/components/common/genericIconComponent";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useFavoritesStore } from "@/stores/favoritesStore";

export default function FavoritesButton() {
  const navigate = useCustomNavigate();
  const { favorites } = useFavoritesStore();

  const handleFavoritesClick = () => {
    navigate("/favorites");
  };

  return (
    <ShadTooltip content="Visa mina favoriter">
      <Button
        variant="ghost"
        size="icon"
        onClick={handleFavoritesClick}
        className="h-9 w-9 relative"
      >
        <ForwardedIconComponent
          name="Heart"
          className="h-4 w-4"
        />
        {favorites.length > 0 && (
          <Badge 
            variant="destructive" 
            className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 text-xs flex items-center justify-center"
          >
            {favorites.length > 99 ? '99+' : favorites.length}
          </Badge>
        )}
      </Button>
    </ShadTooltip>
  );
}
