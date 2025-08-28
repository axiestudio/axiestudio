import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface FavoriteItem {
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
  addedToFavoritesAt: string; // When it was added to favorites
}

interface FavoritesState {
  favorites: FavoriteItem[];
  addToFavorites: (item: Omit<FavoriteItem, 'addedToFavoritesAt'>) => void;
  removeFromFavorites: (id: string) => void;
  isFavorite: (id: string) => boolean;
  clearFavorites: () => void;
  getFavoritesByType: (type: "FLOW" | "COMPONENT") => FavoriteItem[];
}

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set, get) => ({
      favorites: [],
      
      addToFavorites: (item) => {
        const favoriteItem: FavoriteItem = {
          ...item,
          addedToFavoritesAt: new Date().toISOString(),
        };
        
        set((state) => ({
          favorites: [...state.favorites, favoriteItem],
        }));
      },
      
      removeFromFavorites: (id) => {
        set((state) => ({
          favorites: state.favorites.filter((item) => item.id !== id),
        }));
      },
      
      isFavorite: (id) => {
        return get().favorites.some((item) => item.id === id);
      },
      
      clearFavorites: () => {
        set({ favorites: [] });
      },
      
      getFavoritesByType: (type) => {
        return get().favorites.filter((item) => item.type === type);
      },
    }),
    {
      name: 'axiestudio-favorites', // localStorage key
      version: 1,
    }
  )
);
