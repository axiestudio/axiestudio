import LoadingComponent from "@/components/common/loadingComponent";
import { ENABLE_DATASTAX_AXIESTUDIO } from "../feature-flags";

type CustomLoaderProps = {
  remSize?: number;
};

const CustomLoader = ({ remSize = 30 }: CustomLoaderProps) => {
  return ENABLE_DATASTAX_AXIESTUDIO ? (
    <></>
  ) : (
    <LoadingComponent remSize={remSize} />
  );
};

export default CustomLoader;
