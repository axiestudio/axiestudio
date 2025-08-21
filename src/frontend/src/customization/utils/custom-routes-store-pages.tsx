import { Route } from "react-router-dom";
import { StoreGuard } from "@/components/authorization/storeGuard";
import StoreApiKeyPage from "@/pages/SettingsPage/pages/StoreApiKeyPage";
import StorePage from "@/pages/StorePage";
import AxieStudioStorePage from "@/pages/AxieStudioStorePage";
import ShowcasePage from "@/pages/ShowcasePage";

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
      <Route
        path="showcase"
        element={<ShowcasePage />}
      />
    </>
  );
};

export default CustomRoutesStorePages;
