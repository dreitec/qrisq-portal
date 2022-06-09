#!/usr/bin/env sh

export COGNITO_IDENTITY_POOL=$(aws ssm get-parameters --names "/copilot/apps/${QRISQ_ENV}/secrets/cognito_identity_pool" --with-decryption --query "Parameters[0].Value" | tr -d '"')
export API_URL=$(aws ssm get-parameters --names "/copilot/apps/${QRISQ_ENV}/secrets/api_url" --with-decryption --query "Parameters[0].Value" | tr -d '"')
export RECAPTCHA_SITE_KEY=$(aws ssm get-parameters --names "/copilot/apps/${QRISQ_ENV}/secrets/recaptcha_site_key" --with-decryption --query "Parameters[0].Value" | tr -d '"')
envsubst < /usr/share/nginx/html/assets/environment.template.js > /usr/share/nginx/html/assets/environment.js
nginx -g 'daemon off;'
