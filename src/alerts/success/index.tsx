import { Transition } from "@headlessui/react";
import { useEffect, useState } from "react";
import IconComponent from "../../components/common/genericIconComponent";
import type { SuccessAlertType } from "../../types/alerts";

export default function SuccessAlert({
  title,
  id,
  removeAlert,
}: SuccessAlertType): JSX.Element {
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
          removeAlert(id);
        }}
        className="mt-4 w-96 rounded-xl bg-emerald-50/80 dark:bg-emerald-950/20 backdrop-blur-sm border border-emerald-200/50 dark:border-emerald-800/30 p-4 shadow-lg cursor-pointer hover:shadow-xl transition-all duration-200 noflow nowheel nopan nodelete nodrag"
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 mt-0.5">
            <div className="h-2 w-2 rounded-full bg-emerald-500"></div>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-emerald-700 dark:text-emerald-300 line-clamp-2">{title}</p>
          </div>
        </div>
      </div>
    </Transition>
  );
}
