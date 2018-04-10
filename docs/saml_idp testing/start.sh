docker run --name=saml-idp-blue \
-p 8180:80 \
-p 8543:443 \
-e SIMPLESAMLPHP_SP_ENTITY_ID=http://172.17.0.1:8000/saml/metadata/ \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=http://172.17.0.1:8000/saml/acs/ \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=http://172.17.0.1:8000/saml/slo/ \
-v ~/saml_idp/test-saml-idp-user-blue.php:/var/www/simplesamlphp/config/authsources.php \
-v ~/saml_idp/gtk-dialog-authentication-blue.48x48.png:/var/www/simplesamlphp/www/resources/icons/experience/gtk-dialog-authentication.48x48.png \
-d kristophjunge/test-saml-idp

docker run --name=saml-idp-green \
-p 8280:80 \
-p 8643:443 \
-e SIMPLESAMLPHP_SP_ENTITY_ID=http://172.17.0.1:8000/saml/metadata/ \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=http://172.17.0.1:8000/saml/acs/ \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=http://172.17.0.1:8000/saml/slo/ \
-v ~/saml_idp/test-saml-idp-user-green.php:/var/www/simplesamlphp/config/authsources.php \
-v ~/saml_idp/gtk-dialog-authentication-green.48x48.png:/var/www/simplesamlphp/www/resources/icons/experience/gtk-dialog-authentication.48x48.png \
-d kristophjunge/test-saml-idp

docker run --name=saml-idp-red \
-p 8380:80 \
-p 8743:443 \
-e SIMPLESAMLPHP_SP_ENTITY_ID=http://172.17.0.1:8000/saml/metadata/ \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=http://172.17.0.1:8000/saml/acs/ \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=http://172.17.0.1:8000/saml/slo/ \
-v ~/saml_idp/test-saml-idp-user-red.php:/var/www/simplesamlphp/config/authsources.php \
-v ~/saml_idp/gtk-dialog-authentication-red.48x48.png:/var/www/simplesamlphp/www/resources/icons/experience/gtk-dialog-authentication.48x48.png \
-d kristophjunge/test-saml-idp

docker run --name=saml-idp-yellow \
-p 8480:80 \
-p 8843:443 \
-e SIMPLESAMLPHP_SP_ENTITY_ID=http://172.17.0.1:8000/saml/metadata/ \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=http://172.17.0.1:8000/saml/acs/ \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=http://172.17.0.1:8000/saml/slo/ \
-v ~/saml_idp/test-saml-idp-user-yellow.php:/var/www/simplesamlphp/config/authsources.php \
-v ~/saml_idp/gtk-dialog-authentication-yellow.48x48.png:/var/www/simplesamlphp/www/resources/icons/experience/gtk-dialog-authentication.48x48.png \
-d kristophjunge/test-saml-idp


