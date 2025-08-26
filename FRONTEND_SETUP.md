# AxieStudio Frontend Setup with Swedish Translations

## Quick Start

You now have a fully translated Swedish version of AxieStudio! Here's how to run it locally:

### Option 1: Using the Batch Script (Recommended)
1. Double-click `run-frontend.bat`
2. The script will automatically:
   - Use your Node.js binary
   - Install dependencies if needed
   - Start the development server
   - Open the app at http://localhost:3000

### Option 2: Using PowerShell
1. Right-click `run-frontend.ps1` and select "Run with PowerShell"
2. If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Option 3: Manual Setup
1. Open Command Prompt or PowerShell in this directory
2. Install dependencies:
   ```bash
   "C:\Users\mist24lk\Downloads\node-v22.18.0-win-x64\node.exe" npm install
   ```
3. Start the development server:
   ```bash
   "C:\Users\mist24lk\Downloads\node-v22.18.0-win-x64\node.exe" npm run start
   ```

## Configuration

The frontend is configured to:
- Run on **http://localhost:3000**
- Connect to your backend at **https://flow.axiestudio.se**
- Display the interface in **Swedish**

## What You'll See

Once running, you'll see the AxieStudio interface completely translated to Swedish:

### Translated Features:
- ✅ **Login/Signup pages** - "Logga in", "Registrera dig"
- ✅ **Flow building interface** - "Flöde", "Komponenter", "Bygg"
- ✅ **Component sidebar** - "Sök komponenter", "Filtrera"
- ✅ **Toolbar actions** - "Spara", "Exportera", "Dela"
- ✅ **Error messages** - All in Swedish
- ✅ **Settings page** - "Inställningar"
- ✅ **Admin interface** - "Administratör"

### Key Swedish Terms:
- **Flow** = "Flöde"
- **Component** = "Komponent"
- **Build** = "Bygg"
- **Save** = "Spara"
- **Export** = "Exportera"
- **Share** = "Dela"
- **Settings** = "Inställningar"
- **Playground** = "Lekplats"

## Troubleshooting

### If the app doesn't start:
1. Check that Node.js path is correct in the script
2. Make sure you're in the correct directory
3. Try deleting `node_modules` and running again

### If you see English instead of Swedish:
1. Hard refresh the browser (Ctrl+F5)
2. Clear browser cache
3. Check browser console for any errors

### If API calls fail:
1. Make sure your backend at https://flow.axiestudio.se is running
2. Check the browser network tab for failed requests
3. Verify the proxy configuration in `.env.local`

## Development

To make changes to translations:
1. Edit files in `src/` directory
2. The development server will automatically reload
3. All user-facing strings are now in Swedish

## Next Steps

1. Run the frontend locally
2. Test the Swedish interface
3. Verify all features work correctly
4. Enjoy your fully localized AxieStudio experience!

---

**Note**: The frontend will proxy all API calls to your backend at https://flow.axiestudio.se, so you don't need to run a local backend.
