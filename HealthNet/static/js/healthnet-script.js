function checkEnter(e) {
  e = e || event;
  var txtArea = /textarea/i.test((e.target || e.srcElement).tagName);
  return txtArea || (e.keyCode || e.which || e.charCode || 0) == 13;
}

function eventFire(el, etype) {
  if (el.fireEvent) {
    el.fireEvent('on' + etype);
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}
