import type { Page } from "playwright/test";

export const loginAxie Studio = async (page: Page) => {
  await page.goto("/");
  await page.getByPlaceholder("Username").fill("axiestudio");
  await page.getByPlaceholder("Password").fill("axiestudio");
  await page.getByRole("button", { name: "Sign In" }).click();
};
