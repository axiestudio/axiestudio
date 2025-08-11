import { XCircle } from "lucide-react";
import { useTranslation } from "react-i18next";
import type { crashComponentPropsType } from "../../../types/components";
import { Button } from "../../ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "../../ui/card";

function CrashErrorComponent({
  error,
  resetErrorBoundary,
}: crashComponentPropsType): JSX.Element {
  const { t }= useTranslation();
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
                  Sorry, we found an unexpected error!
                </p>
              </div>
            </CardHeader>

            <CardContent className="grid">
              <div>
                <p>
                  Please report errors and get support on the{" "}
                  <a
                    href="https://axiestudio.se"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium hover:underline"
                  >
                    Axie Studio website
                  </a>{" "}
                  or contact our support team.
                  <br></br>
                  Thank you!
                </p>
              </div>
            </CardContent>

            <CardFooter>
              <div className="m-auto mt-4 flex justify-center">
                <Button onClick={resetErrorBoundary}>Restart Axie Studio</Button>

                <a
                  href="https://axiestudio.se"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Button className="ml-3" ignoreTitleCase variant={"outline"}>
                    Visit Axie Studio
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


export default CrashErrorComponent;
export { CrashErrorComponent };