import { Transition } from "@headlessui/react";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import IconComponent from "../../components/common/genericIconComponent";
import type { ErrorAlertType } from "../../types/alerts";

export default function ErrorAlert({
  title,
  list = [],
  id,
  removeAlert,
}: ErrorAlertType): JSX.Element {
  const [show, setShow] = useState(true);
  useEffect(() => {
    if (show) {
      setTimeout(() => {
        setShow(false);
        setTimeout(() => {
          removeAlert(id);
        }, 500);
      }, 5000);
    }
  }, [id, removeAlert, show]);

  return (
    <Transition
      show={show}
      appear={true}
      enter="transition-transform duration-500 ease-out"
      enterFrom={"transform translate-x-[-100%]"}
      enterTo={"transform translate-x-0"}
      leave="transition-transform duration-500 ease-in"
      leaveFrom={"transform translate-x-0"}
      leaveTo={"transform translate-x-[-100%]"}
    >
      <div
        onClick={() => {
          setShow(false);
          setTimeout(() => {
            removeAlert(id);
          }, 500);
        }}
        className="mt-4 w-96 rounded-xl bg-destructive/10 backdrop-blur-sm border border-destructive/20 p-4 shadow-lg cursor-pointer hover:shadow-xl transition-all duration-200 noflow nowheel nopan nodelete nodrag"
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 mt-0.5">
            <div className="h-2 w-2 rounded-full bg-destructive"></div>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-medium text-destructive line-clamp-2">{title}</h3>
            {list?.length !== 0 &&
            list?.some((item) => item !== null && item !== undefined) ? (
              <div className="mt-3 space-y-2">
                {list.map((item, index) => (
                  <div key={index} className="text-xs text-destructive/80 bg-destructive/5 rounded-md p-2 border border-destructive/10">
                    <Markdown
                      linkTarget="_blank"
                      remarkPlugins={[remarkGfm]}
                      components={{
                        a: ({ node, ...props }) => (
                          <a
                            href={props.href}
                            target="_blank"
                            className="underline hover:text-destructive transition-colors"
                            rel="noopener noreferrer"
                          >
                            {props.children}
                          </a>
                        ),
                        p({ node, ...props }) {
                          return (
                            <span className="inline-block w-fit max-w-full">
                              {props.children}
                            </span>
                          );
                        },
                      }}
                    >
                      {Array.isArray(item) ? item.join("\n") : item}
                    </Markdown>
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </Transition>
  );
}
