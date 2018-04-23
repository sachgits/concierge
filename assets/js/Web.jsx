import "../less/all.less"

$(document).ready(function() {
   $(".password__toggle").on('click',function(e) {
       $(this).parent().find("input").each(function() {
           if ($(this).attr("type") == "password") {
               $(this).attr("type", "text");
           } else {
               $(this).attr("type", "password");
           }
        });
    });

    $("input").keypress(function(e) {
      var key = e.which || e.keyCode;
      if ($(this).attr("type") == "password") {
          var s = String.fromCharCode( e.which );
          if ( s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey ) {
              $(this).siblings(".capslock").text(gettext("Attention: CAPS LOCK is ON"));
          } else {
              $(".capslock").text("");
          }
      } else {
        if(key == 13 && $('.loginview__emailsubmit').hasClass('___active')){
          e.preventDefault();
          accounttype.validate();
        }
        $(".capslock").text("");
      }
    });

    $("input").blur(function(e) {
        $(".capslock").text("");
    });

    var theme_bg = $('.account-theme').data('bg');

    if(theme_bg){
        $('.account-theme').css('background-image','url(' + theme_bg + ')');
    }

    if($('form').data('step') != 'login'){
      localStorage.removeItem('user_idp');
    };

    if($('form').data('step') == 'login'){
      if($('.messages.error').children().length){ accounttype.show('login'); }
      $('.login__check_account_type').on('click',function(){
        accounttype.validate();
      });
      $('.loginview__saml-regularlogin').on('click',function(){
        accounttype.show('login');
      });
    }
    if($('form').data('step') == 'login' && $('form').data('samlconnect') == 'True'){
      try {
        var user_idp_data = JSON.parse(localStorage.getItem('user_idp'));
        if(user_idp_data.user_exists){
          accounttype.show('connect');
        } else {
          accounttype.show('connectanduser');
        }
      } catch(err){ accounttype.show('connectanduser'); }
    }
});

var accounttype = (function(){
  var classname_active = '___active',
    url_register = '/register/',
    url_accounttype = '/get_user_and_idp/';
  return {
    validate: function(){
      // TODO email validation
      var container = $('.loginview__email'),
        email_input = $('#id_username',container),
        email_val = email_input.val();
      if(!email_val){ return false; }

      accounttype.check(email_val);
    },

    check: function(email){
      $.post(url_accounttype,{ email:email, csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value },function(r){
        if(r){
          accounttype.process(r);
        } else {
          accounttype.process();
        }
      },'json');
    },

    process: function(r){
      if(!r || !r.user_exists && !r.idp){
        localStorage.removeItem('user_idp');
        window.location.href = url_register;
        return false;
      }

      localStorage.setItem('user_idp',JSON.stringify(r));

      if(r.idp){
        $('.button__saml_login')
          .attr('href', '/saml/sso/' + r.idp + '/')
          .find('span').text(r.idp);
        if(!r.user_exists){
          accounttype.show('saml');
          $('.button__saml_login').focus();
        } else {
          accounttype.show('samlanduser');
        }
      } else if(r.user_exists){
        accounttype.show('login');
        $('#id_password').focus();
      }
    },

    show: function(view){
      if(!view){ return false; }
      $('.loginview.' + classname_active).removeClass(classname_active);
      $('.loginview__' + view).addClass(classname_active);
      if(view == 'connect' || view == 'connectanduser'){
        $('.loginview__email').removeClass(classname_active);
      } else {
        $('.loginview__email').addClass(classname_active);
      }
    }
  };
})();
