function switchForm(currentForm, newForm, newHeight) {
  currentForm.removeClass('fade-grow-in');
  currentForm.removeClass('fade-grow-out');
  newForm.removeClass('fade-grow-in');
  newForm.removeClass('fade-grow-out');

  currentForm.addClass('fade-grow-out');
  currentForm.animate({
      height: "0px",
      opacity: 0
  }, 300, function () {
      currentForm.addClass('hide');
  });

  newForm.removeClass('hide');
  newForm.animate({
      height: newHeight,
      opacity: 100
  }, 250, function () {
  });
  newForm.addClass('scale-0').addClass('fade-grow-in');
}
