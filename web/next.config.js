const { i18n } = require('./next-i18next.config');

module.exports = {
  i18n,
  swcMinify: true,
  // NOTE: HSTS
  async headers() {
    return [{
      source: '/:path*',
      headers: [{
        key: 'Strict-Transport-Security',
        value: 'max-age=63072000; includeSubDomains; preload',
      }],
    }];
  },
};
