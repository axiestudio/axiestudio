# MCP Server Online Deployment Configuration

## 🚨 CRITICAL: Environment Variables for Online Deployment

When deploying Axie Studio online, you MUST set these environment variables for MCP servers to work correctly:

### **Required Environment Variables**

```bash
# Set this to enable online mode
AXIESTUDIO_ONLINE=true

# Set your actual domain (without https://)
AXIESTUDIO_HOST=your-domain.com

# Example for production:
AXIESTUDIO_ONLINE=true
AXIESTUDIO_HOST=axiestudio.example.com
```

### **How External Clients Connect**

#### **Before (Localhost)**
```json
{
  "mcpServers": {
    "axie-project": {
      "command": "uvx",
      "args": ["mcp-proxy", "http://localhost:7860/api/v1/mcp/project/PROJECT_ID/sse"]
    }
  }
}
```

#### **After (Online)**
```json
{
  "mcpServers": {
    "axie-project": {
      "command": "uvx", 
      "args": ["mcp-proxy", "https://your-domain.com/api/v1/mcp/project/PROJECT_ID/sse"]
    }
  }
}
```

### **Client Connection Instructions**

#### **Cursor IDE**
1. Open Cursor settings
2. Add to MCP configuration:
```json
{
  "mcpServers": {
    "axiestudio": {
      "command": "uvx",
      "args": ["mcp-proxy", "https://your-domain.com/api/v1/mcp/project/YOUR_PROJECT_ID/sse"]
    }
  }
}
```

#### **Claude Desktop**
1. Open `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)
2. Add the same configuration as above

#### **Windsurf**
1. Open Windsurf settings
2. Configure MCP servers with the online URL

### **Security Considerations**

1. **HTTPS Required**: Online deployment automatically uses HTTPS
2. **Authentication**: MCP servers support OAuth authentication
3. **CORS**: Properly configured for cross-origin requests
4. **Rate Limiting**: Consider implementing rate limiting for production

### **Testing Your Configuration**

1. Check if environment variables are set:
```bash
echo $AXIESTUDIO_ONLINE
echo $AXIESTUDIO_HOST
```

2. Test MCP endpoint accessibility:
```bash
curl -I https://your-domain.com/api/v1/mcp/project/PROJECT_ID/sse
```

3. Verify in browser: Visit your MCP server tab and copy the configuration

### **Troubleshooting**

#### **Common Issues:**
- **Wrong URL in config**: Check environment variables
- **HTTPS errors**: Ensure SSL certificate is valid
- **Connection refused**: Verify firewall and port settings
- **Authentication failures**: Check OAuth configuration

#### **Debug Steps:**
1. Check server logs for MCP connection attempts
2. Verify environment variables are loaded
3. Test direct SSE endpoint access
4. Validate MCP client configuration

## 🎯 Implementation Status

✅ **Fixed**: Port configuration (now uses 7860)
✅ **Fixed**: Online/localhost detection
✅ **Fixed**: HTTPS/HTTP protocol selection
✅ **Fixed**: Frontend URL generation
✅ **Added**: Environment variable support

## 🚀 Next Steps

1. Set environment variables in your deployment
2. Test MCP connections from external clients
3. Update client configurations with new URLs
4. Monitor connection logs for issues
