$(function() {
  $('.navbar-form').on('submit',function(e){
    e.preventDefault();
    var query = $('.form-control').val();
    if(url.length > 0 && query.length > 0){
      document.location =  query;
    }
  });
});