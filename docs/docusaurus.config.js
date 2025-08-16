// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");
const { remarkCodeHike } = require("@code-hike/mdx");

const isProduction = process.env.NODE_ENV === "production";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Axie Studio Documentation",
  tagline:
    "Axie Studio is a low-code app builder for RAG and multi-agent AI applications.",
  favicon: "img/favicon.ico",
  url: "https://docs.axiestudio.org",
  baseUrl: process.env.BASE_URL ? process.env.BASE_URL : "/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  onBrokenAnchors: "warn",
  organizationName: "axiestudio",
  projectName: "axiestudio",
  trailingSlash: false,
  staticDirectories: ["static"],
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },
  headTags: [
    {
      tagName: "link",
      attributes: {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Sora:wght@550;600&display=swap",
      },
    },
  ],
  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl: "https://github.com/axiestudio/axiestudio/tree/main/docs/",
          remarkPlugins: [
            [
              remarkCodeHike,
              {
                theme: "github-dark",
                lineNumbers: true,
                showCopyButton: true,
                staticMediaQuery: "not screen, (max-width: 768px)",
              },
            ],
          ],
        },
        blog: {
          showReadingTime: true,
          editUrl: "https://github.com/axiestudio/axiestudio/tree/main/docs/",
        },
        theme: {
          customCss: require.resolve("./css/custom.css"),
        },
      }),
    ],
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: "img/axiestudio-social-card.jpg",
      navbar: {
        title: "Axie Studio",
        logo: {
          alt: "Axie Studio Logo",
          src: "img/axiestudio-logo.svg",
        },
        items: [
          {
            type: "docSidebar",
            sidebarId: "tutorialSidebar",
            position: "left",
            label: "Docs",
          },
          { to: "/blog", label: "Blog", position: "left" },
          {
            href: "https://github.com/axiestudio/axiestudio",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Docs",
            items: [
              {
                label: "Get Started",
                to: "/docs/get-started-installation",
              },
              {
                label: "Components",
                to: "/docs/components",
              },
            ],
          },
          {
            title: "Community",
            items: [
              {
                label: "GitHub",
                href: "https://github.com/axiestudio/axiestudio",
              },
              {
                label: "Discord",
                href: "https://discord.gg/axiestudio",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "Blog",
                to: "/blog",
              },
              {
                label: "GitHub",
                href: "https://github.com/axiestudio/axiestudio",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Axie Studio. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
  plugins: [
    [
      "docusaurus-plugin-openapi-docs",
      {
        id: "openapi",
        docsPluginId: "classic",
        config: {
          axiestudio: {
            specPath: "openapi.json",
            outputDir: "docs/API-Reference",
            sidebarOptions: {
              groupPathsBy: "tag",
            },
          },
        },
      },
    ],
  ],
  themes: ["docusaurus-theme-openapi-docs"],
};

module.exports = config;
