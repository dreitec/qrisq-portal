export const environment = {
  API_URL: window['env']['API_URL'] || 'http://localhost:8000/api',
  COGNITO_IDENTITY_POOL: window['env']['COGNITO_IDENTITY_POOL'] || '',
  QRISQ_ENV: window['env']['QRISQ_ENV'] || 'local',
  production: window['env']['QRISQ_ENV'] === 'prod',
  FLUID_PAY_SANDBOX_URL: 'https://sandbox.convenupay.com',
  FLUID_PAY_PRODUCTION_URL: 'https://app.convenupay.com',
  FLUID_PAY_PUBLIC_KEY: window['env']['QRISQ_ENV'] === 'prod' ? 'pub_29yl8SuwSG3xXne7mezGgj6h6Du' : 'pub_28IpFFyqkBUo05gAQFKFVNquxcD',
};
