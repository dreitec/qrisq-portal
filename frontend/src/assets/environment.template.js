(function(window) {
  window["env"] = window["env"] || {};
  window["env"]["API_URL"] = "${API_URL}";
  window["env"]["COGNITO_IDENTITY_POOL"] = "${COGNITO_IDENTITY_POOL}";
  window["env"]["QRISQ_ENV"] = "${QRISQ_ENV}"
  window["env"]["RECAPTCHA_SITE_KEY"] = "${RECAPTCHA_SITE_KEY}";
})(this);
