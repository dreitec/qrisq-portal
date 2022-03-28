export const environment = {
  API_URL: window['env']['API_URL'] || 'http://localhost:8000/api',
  COGNITO_IDENTITY_POOL: window['env']['COGNITO_IDENTITY_POOL'] || '',
  QRISQ_ENV: window['env']['QRISQ_ENV'] || 'local',
  production: window['env']['QRISQ_ENV'] === 'prod'
};
