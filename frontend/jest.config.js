module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest',
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    'api_config\\.json$': '<rootDir>/tests/__mocks__/apiConfigMock.js',

  },
  testMatch: ['**/tests/**/*.spec.js'],
};
