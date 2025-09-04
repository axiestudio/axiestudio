import { create } from "zustand";
import type { DarkStoreType } from "../types/zustand/dark";

const startedStars = Number(window.localStorage.getItem("githubStars")) ?? 0;

export const useDarkStore = create<DarkStoreType>((set, get) => ({
  dark: (() => {
    const stored = window.localStorage.getItem("isDark");
    return stored !== null ? JSON.parse(stored) : false;
  })(),
  stars: startedStars,
  version: "",
  latestVersion: "",
  refreshLatestVersion: (v: string) => {
    set(() => ({ latestVersion: v }));
  },
  setDark: (dark) => {
    set(() => ({ dark: dark }));
    window.localStorage.setItem("isDark", dark.toString());
  },
  refreshVersion: (v) => {
    set(() => ({ version: v }));
  },
  refreshStars: () => {
    // Disabled GitHub API calls for Axie Studio
    window.localStorage.setItem("githubStars", "0");
    set(() => ({ stars: 0, lastUpdated: new Date() }));
  },
  discordCount: 0,
  refreshDiscordCount: () => {
    // Disabled Discord API calls for Axie Studio
    set(() => ({ discordCount: 0 }));
  },
}));
