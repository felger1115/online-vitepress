import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Echotron",
  description: "TTS (Text - to - Speech) is a free, open - source, cross - platform tech. It lets developers turn text into natural speech, build voice - enabled apps, interactive voice response systems, etc., and easily integrate speech into projects.",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Privacy', link: '/privacy' },
      { text: 'Terms', link: '/terms' }
    ],

    sidebar: [
      {
        items: [
          { text: 'Privacy Policy', link: '/privacy' },
          { text: 'Terms of Service', link: '/terms' }
        ]
      }
    ],
    footer: {
      message: 'Echotron',
      copyright: 'Copyright © 2025-present'
    },
    socialLinks: [
      // { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  },
  cleanUrls: true,
  ignoreDeadLinks: true,
  srcDir: 'public',
  srcExclude: ['**/private/**'],
  outDir: '../../dist',
})
