codecraft-ai-docs/docusaurus.config.js
module.exports = {
  title: 'CodeCraft AI',
  tagline: 'A showcase-ready, modular AI pipeline for code completion, documentation, and analysis',
  url: 'https://your-domain.com', // Replace with your domain
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'static/favicon.ico',
  organizationName: 'your-github-username', // Replace with your GitHub username
  projectName: 'codecraft-ai-docs',
  themeConfig: {
    navbar: {
      title: 'CodeCraft AI',
      items: [
        { to: 'docs/introduction', label: 'Introduction', position: 'left' },
        { to: 'docs/architecture', label: 'Architecture', position: 'left' },
        { to: 'docs/mlops', label: 'MLOps', position: 'left' },
        { to: 'docs/aws-integration', label: 'AWS Integration', position: 'left' },
        { to: 'docs/portfolio-showcase', label: 'Portfolio Showcase', position: 'left' },
        { to: 'docs/roadmap', label: 'Roadmap', position: 'left' },
        { to: 'docs/README', label: 'Documentation', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Introduction', to: 'docs/introduction' },
            { label: 'Architecture', to: 'docs/architecture' },
            { label: 'MLOps', to: 'docs/mlops' },
            { label: 'AWS Integration', to: 'docs/aws-integration' },
            { label: 'Portfolio Showcase', to: 'docs/portfolio-showcase' },
            { label: 'Roadmap', to: 'docs/roadmap' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'GitHub', href: 'https://github.com/your-github-username/codecraft-ai-docs' }, // Replace with your GitHub repo
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Your Name. Built with Docusaurus.`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/dracula'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-github-username/codecraft-ai-docs/edit/main/', // Replace with your GitHub repo
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
