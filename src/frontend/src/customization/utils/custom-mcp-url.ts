import { api } from "@/controllers/API/api";

export const customGetMCPUrl = (projectId: string) => {
  // Get the base URL from API config or current window location
  let apiHost = api.defaults.baseURL || window.location.origin;

  // Ensure we use the correct protocol and remove any trailing slashes
  apiHost = apiHost.replace(/\/$/, '');

  // If baseURL is relative (starts with /), use window.location.origin
  if (apiHost.startsWith('/')) {
    apiHost = window.location.origin;
  }

  const apiUrl = `${apiHost}/api/v1/mcp/project/${projectId}/sse`;
  return apiUrl;
};
