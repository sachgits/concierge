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
    console.log(theme_bg);
    if(theme_bg){
        $('.account-theme').css('background-image','url(' + theme_bg + ')');
    }

    $('.login__check_account_type').on('click',function(){
      accounttype.validate();
    });
    $('.loginview__saml-regularlogin').on('click',function(){
      accounttype.show('login');
    });

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

      // TODO: de volgende regel weer inschakelen als juiste response van server komt. Regel daarna kan weg dan.
      // accounttype.check(email_val);
      accounttype.process({user:'duncan@projectfive.nl',idp:'Bedrijfsnaam',idp_url:'http://pleio.nl'});
    },

    check: function(email){
      $.post(url_accounttype,{email:email},function(r){
        if(r){
          accounttype.process(r);
        } else {
          accounttype.process();
        }
      },'json');
    },

    process: function(r){
      if(!r || !r.user && !r.idp){
        window.location.href = url_register;
        return false;
      }

      if(r.idp){
        if(!r.user){
          window.location.href = r.idp_url;
          return false;
        }
        $('.button__saml_login').attr('href',r.idp_url)
          .find('span').text(r.idp);
        accounttype.show('saml');
      } else if(r.user){
        accounttype.show('login');
      }
    },

    show: function(view){
      if(!view){ return false; }
      $('.loginview.' + classname_active).removeClass(classname_active);
      $('.loginview__' + view).addClass(classname_active);
    }
  };
})();
