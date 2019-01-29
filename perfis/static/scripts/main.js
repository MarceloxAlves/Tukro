var modalConfirm = function(callback, action, param){
  var action = null
  $(".action").on("click", function(){
      action = $(this)
      $("#msg-confirm").text(action.attr('data-msg'))
    $("#mi-modal").modal('show');
  });

  $("#modal-btn-sim").on("click", function(){
    callback(action.attr('positive'), action.attr('param'));
    $("#mi-modal").modal('hide');
  });

  $("#modal-btn-nao").on("click", function(){
    callback(action.attr('negative'), action.attr('param'));
    $("#mi-modal").modal('hide');
  });
};
modalConfirm(function(action, param){
   window[action](param);
});

var msgFeedback = function(callback, actionFeedback){
  var actionFeedback = null
  $(".actionFeedback").on("click", function(){
      actionFeedback = $(this)
      $("#msg-body").text(actionFeedback.attr('data-msg'))
      $("#feedback-msg").addClass(actionFeedback.attr('data-type-alert'))
    $("#feedback-msg").css('display', 'block');
  });

};
msgFeedback(function(actionFeedback){
   window[actionFeedback]();
});
