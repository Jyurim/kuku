// export default config;
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    // paths: { base: "/" },
    adapter: adapter({
      // default options are shown
      pages: 'build',
      assets: 'build',
      fallback: '/404.html',
      precompress: false
    }),
    prerender: {
      // This can be false if you're using a fallback (i.e. SPA mode)
      default: true
    },
    trailingSlash: 'always',
  }
};

export default config;