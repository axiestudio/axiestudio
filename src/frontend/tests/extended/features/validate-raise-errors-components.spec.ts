import { expect, test } from "@playwright/test";
import { addCustomComponent } from "../../utils/add-custom-component";
import { awaitBootstrapTest } from "../../utils/await-bootstrap-test";
import { zoomOut } from "../../utils/zoom-out";

test(
  "user should be able to see errors on popups when raise an error",
  { tag: ["@release", "@workspace", "@components"] },
  async ({ page }) => {
    const customComponentCodeWithRaiseErrorMessage = `
# from axiestudio.field_typing import Data
from axiestudio.custom import Component
from axiestudio.io import MessageTextInput, Output
from axiestudio.schema import Data


class CustomComponent(Component):
    display_name = "Anpassad komponent"
    description = "Använd som mall för att skapa din egen komponent."
    documentation: str = "https://docs.axiestudio.se/components-custom-components"
    icon = "code"
    name = "CustomComponent"

    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="Inmatningsvärde",
            info="Detta är en anpassad komponentinmatning",
            value="Hello, World!",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Utmatning", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        msg = "DETTA ÄR ETT TESTFELMEDDELANDE"
        raise ValueError(msg)
        data = Data(value=self.input_value)
        self.status = data
        return data
    `;

    await awaitBootstrapTest(page);
    await page.getByTestId("blank-flow").click();

    await page.waitForSelector(
      '[data-testid="sidebar-custom-component-button"]',
      {
        timeout: 3000,
      },
    );

    await addCustomComponent(page);

    await page.getByTestId("fit_view").click();
    await page.getByTestId("zoom_out").click();

    await page.waitForTimeout(1000);

    await page.waitForSelector('[data-testid="title-Custom Component"]', {
      timeout: 3000,
    });
    await page.getByTestId("title-Custom Component").click();

    await page.getByTestId("code-button-modal").click();

    await page.locator(".ace_content").click();
    await page.keyboard.press(`ControlOrMeta+A`);
    await page
      .locator("textarea")
      .fill(customComponentCodeWithRaiseErrorMessage);

    await page.getByText("Check & Save").last().click();

    await page.getByTestId("button_run_custom component").click();

    await page.waitForSelector("text=THIS IS A TEST ERROR MESSAGE", {
      timeout: 3000,
    });

    const numberOfErrorMessages = await page
      .getByText("THIS IS A TEST ERROR MESSAGE")
      .count();

    expect(numberOfErrorMessages).toBeGreaterThan(0);
  },
);
