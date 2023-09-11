const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Unistore',
  tagline: 'Unistore help desk',
  url: 'https://help.unistore.com',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'unistorecom',
  projectName: 'unistorecom/docs',
  plugins: ['docusaurus-plugin-sass'],
  stylesheets: [
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;display=swap',
  ],
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          breadcrumbs: true,
        },
        theme: {
          customCss: require.resolve('./src/css/index.scss'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    {
      colorMode: {
        defaultMode: 'light',
        disableSwitch: true,
        respectPrefersColorScheme: false,
      },
      navbar: {
        title: 'Unistore',
        logo: {
          alt: 'My Site Logo',
          src: '/img/icons/logo.svg',
          height: 24,
          width: 24,
        },
        items: [
          {
            type: 'doc',
            docId: 'getting-started',
            position: 'left',
            label: 'Getting started',
          },
          {
            type: 'doc',
            docId: 'topics/dashboard/dashboard',
            position: 'left',
            label: 'Topics',
          },
          // {
          //   type: 'localeDropdown',
          //   position: 'right',
          // },
        ],
      },
      footer: {
        style: 'light',
        logo: {
          alt: 'Unistore logo',
          src: '/img/icons/logo.svg',
          width: 24,
          height: 24,
          href: '/',
        },
        copyright: `Unistore, ${new Date().getFullYear()} ©`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 5,
      },
    },
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
    localeConfigs: {
      en: {
        htmlLang: 'en-GB',
      },
    },
  },
};

module.exports = config;
