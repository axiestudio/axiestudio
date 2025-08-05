# Axie Studio Documentation

This directory contains the documentation for Axie Studio, built with [Docusaurus](https://docusaurus.io/).

## Development

### Prerequisites

- Node.js 18.x or higher
- Yarn 1.22.x

### Installation

```bash
cd docs
yarn install
```

### Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

The documentation is automatically deployed when changes are pushed to the main branch.

## Structure

- `docs/` - Documentation content in Markdown format
- `static/` - Static assets (images, files, etc.)
- `src/` - Custom React components and pages
- `docusaurus.config.js` - Docusaurus configuration
- `sidebars.js` - Sidebar configuration

## Contributing

When adding new documentation:

1. Create or edit Markdown files in the `docs/` directory
2. Update `sidebars.js` if adding new sections
3. Add any images to `static/img/`
4. Test locally with `yarn start`
5. Submit a pull request

For more information on writing documentation, see the [Docusaurus documentation](https://docusaurus.io/docs).
