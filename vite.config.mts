import react from "@vitejs/plugin-react-swc";
import * as dotenv from "dotenv";
import path from "path";
import { defineConfig, loadEnv } from "vite";
import svgr from "vite-plugin-svgr";
import tsconfigPaths from "vite-tsconfig-paths";
import {
  API_ROUTES,
  BASENAME,
  PORT,
  PROXY_TARGET,
} from "./src/customization/config-constants";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  const envAxiestudioResult = dotenv.config({
    path: path.resolve(__dirname, "../../.env"),
  });

  const envAxiestudio = envAxiestudioResult.parsed || {};

  const apiRoutes = API_ROUTES || ["^/api/v1/", "^/api/v2/", "/health"];

  const target =
    env.VITE_PROXY_TARGET || PROXY_TARGET || "http://localhost:7860";

  const port = Number(env.VITE_PORT) || PORT || 3000;

  const proxyTargets = apiRoutes.reduce((proxyObj, route) => {
    proxyObj[route] = {
      target: target,
      changeOrigin: true,
      secure: false,
      ws: true,
    };
    return proxyObj;
  }, {});

  return {
    base: BASENAME || "",
    build: {
      outDir: "build",
    },
    define: {
      "process.env.BACKEND_URL": JSON.stringify(
        envAxiestudio.BACKEND_URL ?? env.BACKEND_URL ?? "http://localhost:7860",
      ),
      "process.env.ACCESS_TOKEN_EXPIRE_SECONDS": JSON.stringify(
        envAxiestudio.ACCESS_TOKEN_EXPIRE_SECONDS ?? env.ACCESS_TOKEN_EXPIRE_SECONDS ?? 60,
      ),
      "process.env.CI": JSON.stringify(envAxiestudio.CI ?? env.CI ?? false),
      "process.env.AXIESTUDIO_AUTO_LOGIN": JSON.stringify(
        envAxiestudio.AXIESTUDIO_AUTO_LOGIN ?? env.AXIESTUDIO_AUTO_LOGIN ?? false,
      ),
      "process.env.AXIESTUDIO_FEATURE_MCP_COMPOSER": JSON.stringify(
        envAxiestudio.AXIESTUDIO_FEATURE_MCP_COMPOSER ?? env.AXIESTUDIO_FEATURE_MCP_COMPOSER ?? "false",
      ),
      "process.env.AXIESTUDIO_SECRET_KEY": JSON.stringify(
        envAxiestudio.AXIESTUDIO_SECRET_KEY ?? env.AXIESTUDIO_SECRET_KEY ?? "",
      ),
      "process.env.AXIESTUDIO_SUPERUSER": JSON.stringify(
        envAxiestudio.AXIESTUDIO_SUPERUSER ?? env.AXIESTUDIO_SUPERUSER ?? "",
      ),
      "process.env.AXIESTUDIO_SUPERUSER_PASSWORD": JSON.stringify(
        envAxiestudio.AXIESTUDIO_SUPERUSER_PASSWORD ?? env.AXIESTUDIO_SUPERUSER_PASSWORD ?? "",
      ),
      "process.env.AXIESTUDIO_NEW_USER_IS_ACTIVE": JSON.stringify(
        envAxiestudio.AXIESTUDIO_NEW_USER_IS_ACTIVE ?? env.AXIESTUDIO_NEW_USER_IS_ACTIVE ?? false,
      ),
      "process.env.AXIESTUDIO_CACHE_TYPE": JSON.stringify(
        envAxiestudio.AXIESTUDIO_CACHE_TYPE ?? env.AXIESTUDIO_CACHE_TYPE ?? "simple",
      ),
      "process.env.AXIESTUDIO_LOG_LEVEL": JSON.stringify(
        envAxiestudio.AXIESTUDIO_LOG_LEVEL ?? env.AXIESTUDIO_LOG_LEVEL ?? "info",
      ),
      "process.env.AXIESTUDIO_WORKERS": JSON.stringify(
        envAxiestudio.AXIESTUDIO_WORKERS ?? env.AXIESTUDIO_WORKERS ?? 1,
      ),
    },
    plugins: [react(), svgr(), tsconfigPaths()],
    server: {
      port: port,
      proxy: {
        ...proxyTargets,
      },
    },
  };
});
