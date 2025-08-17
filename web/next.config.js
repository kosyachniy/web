const { i18n } = require('./next-i18next.config');

module.exports = {
  i18n,
  swcMinify: true,
  // Skip ESLint during build in Docker environments
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Ensure proper JSX transform
  compiler: {
    emotion: false,
  },
  experimental: {
    forceSwcTransforms: true,
  },
  // Fix webpack configuration for JSX
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      config.resolve.alias = {
        ...config.resolve.alias,
        'react/jsx-dev-runtime': 'react/jsx-dev-runtime',
        'react/jsx-runtime': 'react/jsx-runtime',
      };
    }
    return config;
  },
};
