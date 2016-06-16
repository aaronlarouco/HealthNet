/*

JPop JavaScript
==============================================================================
Version: 0.81
Author: Ryan Hochmuth
Last Modified: 10/15/2015
(c) 2015 Ryan Hochmuth under BSD license
------------------------------------------------------------------------------
A simple JavaScript popup box system useful for showing forms, messages,
or other quick same-screen popups.

NOTE: There is an optional CSS file that goes along with this script.  It isn't
      needed but having it adds animations and some more styles to the popups
      so it's recommended.

*/

window.addEventListener('load', initJPop, false);

var windowWidth = window.innerWidth
|| document.documentElement.clientWidth
|| document.body.clientWidth;

window.onresize = function(e) {
  windowWidth = window.innerWidth
  || document.documentElement.clientWidth
  || document.body.clientWidth;
};

// Find all elements in the document that should be initialized as JPops
// and setup the click events and hide the popup content.
function initJPop() {
  var popups = document.getElementsByClassName("jpop");
  for (x = 0; x < popups.length; x++) {
    popups[x].addEventListener('click', showJPop, false);
    document.getElementById(popups[x].getAttribute('popup')).style.display = 'none';
  }
}

function initJPopInParent(parent) {
  var popups = parent.getElementsByClassName("jpop");
  for (x = 0; x < popups.length; x++) {
    popups[x].addEventListener('click', showJPop, false);
    document.getElementById(popups[x].getAttribute('popup')).style.display = 'none';
  }
}

function initSpecificJPop(element) {
  element.addEventListener('click', showJPop, false);
  document.getElementById(element.getAttribute('popup')).style.display = 'none';
}

// Build and show the popup on the screen.
function showJPop() {
  document.body.style.overflow = "hidden";

  var innerContainer = document.createElement("div");
  innerContainer.setAttribute("id", "jpop-inner");

  // Get the popup content now so attributes can be used
  var popupContent = document.getElementById(this.getAttribute('popup'));

  // Create the faded black background that covers the entire page
  var fadedBg = document.createElement("div");
  fadedBg.className += " jpop-faded-bg";
  fadedBg.setAttribute('id', 'jpop-faded-bg');
  fadedBg.style.backgroundColor = "rgba(0, 0, 0, 0.6)";
  fadedBg.style.position = "fixed";
  fadedBg.style.top = "0";
  fadedBg.style.left = "0";
  fadedBg.style.width = "100%";
  fadedBg.style.height = "100%";
  fadedBg.addEventListener('click', function(e) {
    if (e.target.getAttribute("id") == "jpop-faded-bg") {
      closeJPop(fadedBg, innerContainer, popupContent);
    }
  } , false);
  fadedBg.style.opacity = "0";
  fadedBg.className = "jpop-fade-in";
  fadedBg.style.zIndex = 5000;

  // Create the JPop container that holds all the content
  var container = document.createElement("div");
  container.style.position = "absolute";
  container.style.overflow = "hidden";

  if (popupContent.hasAttribute('width'))
    container.style.width = popupContent.getAttribute('width');
  else
    container.style.width = "400px";

  var mTrigger = 768;
  if (popupContent.hasAttribute('mtrigger'))
    mTrigger = parseInt(popupContent.getAttribute('mtrigger'));

  var mWidth = "95%";
  if (popupContent.hasAttribute('mwidth'))
    mWidth = popupContent.getAttribute('mwidth');

  if (windowWidth <= mTrigger)
    container.style.width = mWidth;
  else {
    if (popupContent.hasAttribute('width'))
      container.style.width = popupContent.getAttribute('width');
    else
      container.style.width = "400px";
  }

  if (popupContent.hasAttribute('height'))
    container.style.height = popupContent.getAttribute('height');

  var transVert = false;
  if (popupContent.hasAttribute('top'))
    container.style.top = popupContent.getAttribute('top');
  else {
    container.style.top = "50%";
    transVert = true;
  }

  var transHor = false;
  if (popupContent.hasAttribute('left'))
    container.style.left = popupContent.getAttribute('left');
  else {
    container.style.left = "50%";
    transHor = true;
  }

  if (transVert && transHor)
    container.style.transform = "translate(-50%, -50%)";
  else if (transVert && !transHor)
    container.style.transform = "translate(0%, -50%)";
  else if (!transVert && transHor)
    container.style.transform = "translate(-50%, 0%)";

  // Create the inner container that animates and shows the popup content
  innerContainer.style.width = "100%";
  innerContainer.style.height = "100%";
  innerContainer.style.paddingBottom = "10px";
  // innerContainer.style.overflow = "hidden";

  if (popupContent.hasAttribute('bgcolor'))
    innerContainer.style.backgroundColor = popupContent.getAttribute('bgcolor');
  else
    innerContainer.style.backgroundColor = "#ffffff";

  if (popupContent.hasAttribute('roundcorners'))
    innerContainer.style.borderRadius = popupContent.getAttribute('roundcorners');
  else
    innerContainer.style.borderRadius = "10px";

  innerContainer.style.opacity = "0";
  innerContainer.style.transform = "scale(0)";
  innerContainer.className = "jpop-fade-grow-in";
  container.appendChild(innerContainer);

  // Create the X button at the top-right of the container
  var exitIcon = document.createElement("p");
  exitIcon.className += " jpop-x";
  exitIcon.style.position = "absolute";
  exitIcon.style.width = "32px";
  exitIcon.style.height = "32px";
  exitIcon.style.top = "10px";
  exitIcon.style.right = "4px";
  exitIcon.innerHTML = "X";
  exitIcon.style.textAlign = "center";
  exitIcon.style.verticalAlign = "middle";
  exitIcon.style.fontSize = "24px";
  exitIcon.style.fontWeight = "bold";

  if (popupContent.hasAttribute('xcolor'))
    exitIcon.style.color = popupContent.getAttribute('xcolor');
  else
    exitIcon.style.color = "#525151";

  exitIcon.addEventListener('click', function(e){
    closeJPop(fadedBg, innerContainer, popupContent);
  } , false);

  var showDivider = popupContent.getAttribute('showdivider');
  if (popupContent.hasAttribute('showdivider')) {
    if (showDivider === "true") {
      innerContainer.appendChild(exitIcon);
    }
  }
  else {
    innerContainer.appendChild(exitIcon);
  }

  // Create a divider at the top of the JPop container to separate the content
  var divider = document.createElement("div");
  divider.setAttribute("id", "jpop-header");
  divider.style.width = "100%";
  divider.style.height = "50px";
  divider.style.margin = "0 auto 8px auto";

  if (popupContent.hasAttribute('headercolor')) {
  divider.style.backgroundColor = popupContent.getAttribute('headercolor');
  }
  else {
    divider.style.backgroundColor = "#dfdfdf";
  }

  if (popupContent.hasAttribute('roundcorners')) {
    divider.style.borderTopLeftRadius = popupContent.getAttribute('roundcorners');
    divider.style.borderTopRightRadius = popupContent.getAttribute('roundcorners');
  }
  else {
    divider.style.borderTopLeftRadius = "8px";
    divider.style.borderTopRightRadius = "8px";
  }

  if (popupContent.hasAttribute('jpoptitle')) {
    var title = document.createElement("h2");
    title.innerHTML = popupContent.getAttribute('jpoptitle');
    title.style.margin = "0";
    title.style.fontSize = "28px";
    title.style.color = "#525151";
    divider.style.paddingLeft = "10px";
    divider.style.paddingTop = "10px";
    divider.appendChild(title);
  }

  var showDivider = popupContent.getAttribute('showdivider');
  if (popupContent.hasAttribute('showdivider')) {
    if (showDivider === "true") {
      divider.style.borderBottom = "1px solid rgba(136, 136, 136, 0.6)";
      innerContainer.appendChild(divider);
    }
  }
  else {
    divider.style.borderBottom = "1px solid rgba(136, 136, 136, 0.6)";
    innerContainer.appendChild(divider);
  }

  // Add the desired content to the popup
  popupContent.style.overflowY = "auto";
  popupContent.classList.add("jpop-scrollbars")
  popupContent.style.height = "90%";
  popupContent.style.display = 'block';
  innerContainer.appendChild(popupContent);

  // Add the container to the fadedBg
  fadedBg.appendChild(container);
  // Add the entire popup to the screen
  document.body.appendChild(fadedBg);
}

// Set the jpop title to the given value
function setJpopTitle(element, text) {
  var jpop = document.getElementById(element);

  if (jpop.hasAttribute('jpoptitle')) {
    var header = document.getElementById("jpop-header");
    var title = header.getElementsByTagName("h2");
    title[0].innerHTML = text;
  }
}

// Remove the popup from the screen.
function closeJPop(element, inner, popupContent) {
  document.body.style.overflow = "initial";

  element.className = "jpop-fade-out";
  inner.className = "jpop-fade-grow-out";

  setTimeout(function() {
    popupContent.style.display = "none";
    document.body.appendChild(popupContent);
    element.parentNode.removeChild(element);
  }, 200);
}

function forceCloseJPop() {
  document.body.style.overflow = "initial";

  var bg = document.getElementById("jpop-faded-bg");
  var inner = document.getElementById("jpop-inner");

  var content = inner.children[2];

  bg.className = "jpop-fade-out";
  inner.className = "jpop-fade-grow-out";

  setTimeout(function() {
    content.style.display = "none";
    document.body.appendChild(content);
    bg.parentNode.removeChild(bg);
  }, 200);
}
