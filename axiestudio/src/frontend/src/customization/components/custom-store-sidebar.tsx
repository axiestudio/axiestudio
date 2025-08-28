import { ForwardedIconComponent } from "@/components/common/genericIconComponent";

export const CustomStoreSidebar = (
  hasApiKey: boolean = false,
  hasStore: boolean = false,
) => {
  const items: Array<{ title: string; href: string; icon: JSX.Element }> = [];

  if (hasApiKey) {
    items.push({
      title: "Axie Studio API-nycklar",
      href: "/settings/api-keys",
      icon: (
        <ForwardedIconComponent
          name="Key"
          className="w-4 flex-shrink-0 justify-start stroke-[1.5]"
        />
      ),
    });
  }

  if (hasStore) {
    items.push({
      title: "Komponentutställning",
      href: "/settings/store",
      icon: (
        <ForwardedIconComponent
          name="Package"
          className="w-4 flex-shrink-0 justify-start stroke-[1.5]"
        />
      ),
    });
  }

  return items;
};
