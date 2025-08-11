/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

declare module "*.svg" {
  const content: string;
  export default content;
}

// Global process declaration for Vite environment variables
declare const process: {
  env: {
    [key: string]: string | undefined;
    ACCESS_TOKEN_EXPIRE_SECONDS?: string;
    AXIESTUDIO_FEATURE_MCP_COMPOSER?: string;
  };
};
