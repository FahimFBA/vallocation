// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Vehicle Allocation (Vallocation)',
  tagline: 'FastAPI & MongoDB based Vehicle Management Backend System',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://fahimfba.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/vallocation/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'FahimFBA', // Usually your GitHub org/user name.
  projectName: 'vallocation', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/FahimFBA/vallocation/docs-docusaurus',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/FahimFBA/vallocation/docs-docusaurus',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/vallocation_banner.png',
      navbar: {
        title: 'Vallocation',
        logo: {
          alt: 'Vehicle Allocation (Vallocation)',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Tutorial',
          },
          // { to: '/blog', label: 'Blog', position: 'left' },
          {
            href: 'https://blog.fahimbinamin.com',
            label: 'Blog',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Demonstration',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/FahimFBA',
              },
              {
                label: 'LinkedIn',
                href: 'https://www.linkedin.com/in/fahimfba/',
              },
              {
                label: 'Twitter/X',
                href: 'https://x.com/Fahim_FBA',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: 'https://blog.fahimbinamin.com/',
              },
              {
                label: 'YouTube',
                href: 'https://www.youtube.com/@FahimAmin/videos',
              },
              {
                label: 'Kaggle',
                href: 'https://www.kaggle.com/mdfahimbinamin',
              },
              {
                label: 'LeetCode',
                href: 'https://leetcode.com/u/FahimFBA/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Project VehicleAllocation (Vallocation). Built by Md. Fahim Bin Amin`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
