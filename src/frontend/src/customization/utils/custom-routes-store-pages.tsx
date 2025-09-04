import { Route } from "react-router-dom";
import { StoreGuard } from "@/components/authorization/storeGuard";
import StoreApiKeyPage from "@/pages/SettingsPage/pages/StoreApiKeyPage";
import StorePage from "@/pages/StorePage";
import AxieStudioStorePage from "@/pages/AxieStudioStorePage";
import ShowcasePage from "@/pages/ShowcasePage";
import FavoritesPage from "@/pages/FavoritesPage";

export const CustomRoutesStorePages = () => {
  return (
    <>
      <Route
        path="store"
        element={
          <StoreGuard>
            <StorePage />
          </StoreGuard>
        }
      />
      <Route
        path="store/:id/"
        element={
          <StoreGuard>
            <StorePage />
          </StoreGuard>
        }
      />
      <Route
        path="axiestudio-store"
        element={<AxieStudioStorePage />}
      />
      <Route
        path="axiestudio-store/:id"
        element={<AxieStudioStorePage />}
      />
    </>
  );
};

export const CustomShowcaseRoutes = () => {
  return (
    <>
      <Route
        path="showcase"
        element={<ShowcasePage />}
      />
      <Route
        path="favorites"
        element={<FavoritesPage />}
      />
    </>
  );
};

export default CustomRoutesStorePages;
