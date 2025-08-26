import { XCircle } from "lucide-react";
import type { crashComponentPropsType } from "../../../types/components";
import { Button } from "../../ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "../../ui/card";

export default function CrashErrorComponent({
  error,
  resetErrorBoundary,
}: crashComponentPropsType): JSX.Element {
  return (
    <div className="z-50 flex h-screen w-screen items-center justify-center bg-foreground bg-opacity-50">
      <div className="flex h-screen w-screen flex-col bg-background text-start shadow-lg">
        <div className="m-auto grid w-1/2 justify-center gap-5 text-center">
          <Card className="p-8">
            <CardHeader>
              <div className="m-auto">
                <XCircle strokeWidth={1.5} className="h-16 w-16" />
              </div>
              <div>
                <p className="mb-4 text-xl text-foreground">
                  Ursäkta, vi hittade ett oväntat fel!
                </p>
              </div>
            </CardHeader>

            <CardContent className="grid">
              <div>
                <p>
                  Vänligen rapportera fel med detaljerade spårningar på{" "}
                  <a
                    href="https://github.com/axiestudio-ai/axiestudio/issues"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium hover:underline"
                  >
                    GitHub Issues
                  </a>{" "}
                  sidan.
                  <br></br>
                  Tack så mycket!
                </p>
              </div>
            </CardContent>

            <CardFooter>
              <div className="m-auto mt-4 flex justify-center">
                <Button onClick={resetErrorBoundary}>Starta Om Axie Studio</Button>

                <a
                  href="https://github.com/axiestudio-ai/axiestudio/issues/new"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Button className="ml-3" ignoreTitleCase variant={"outline"}>
                    Rapportera på GitHub
                  </Button>
                </a>
              </div>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}
