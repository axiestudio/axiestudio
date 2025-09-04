import { Transition } from "@headlessui/react";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CustomLink } from "@/customization/components/custom-link";
import IconComponent from "../../components/common/genericIconComponent";
import type { NoticeAlertType } from "../../types/alerts";

export default function NoticeAlert({
  title,
  list = [],
  id,
  link,
  removeAlert,
}: NoticeAlertType): JSX.Element {
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

  const handleClick = () => {
    setShow(false);
    setTimeout(() => {
      removeAlert(id);
    }, 500);
  };

  return (
    <Transition
      show={show}
      enter="transition-transform duration-500 ease-out"
      enterFrom={"transform translate-x-[-100%]"}
      enterTo={"transform translate-x-0"}
      leave="transition-transform duration-500 ease-in"
      leaveFrom={"transform translate-x-0"}
      leaveTo={"transform translate-x-[-100%]"}
    >
      <div
        onClick={handleClick}
        className="noflow nowheel nopan nodelete nodrag mt-4 w-96 rounded-xl bg-blue-50/80 dark:bg-blue-950/20 backdrop-blur-sm border border-blue-200/50 dark:border-blue-800/30 p-4 shadow-lg cursor-pointer hover:shadow-xl transition-all duration-200"
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 mt-0.5">
            <div className="h-2 w-2 rounded-full bg-blue-500"></div>
          </div>
          <div className="flex-1 min-w-0 space-y-2">
            <p className="text-sm font-medium text-blue-700 dark:text-blue-300">
              {title}
            </p>
            {link && (
              <CustomLink
                to={link}
                className="inline-flex text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200 transition-colors underline"
              >
                Visa detaljer
              </CustomLink>
            )}
          </div>
        </div>
      </div>
    </Transition>
  );
}
