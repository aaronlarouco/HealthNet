/*

JVal CSS
==============================================================================
Version: 0.1
Author: Ryan Hochmuth
Last Modified: 10/16/2015
(c) 2015 Ryan Hochmuth under BSD license
------------------------------------------------------------------------------
A JavaScript module that adds nice visual effects to form validation.

*/

// Start JVal setup as soon as the document loads
window.addEventListener('load', inputSetup, false);

// Setup the form inputs to react to the :valid and :invalid pseudo-classes
// and only trigger the styles once the field has been interacted with.
function inputSetup() {
  var inputs = document.getElementsByTagName("input");
  var inputs_len = inputs.length;

  var addInteractedClass = function(e) {
    if (!hasClass(e.srcElement, "interacted") && hasClass(e.srcElement, "jval")) {
      e.srcElement.classList.toggle("interacted", true);
    }
  };

  for (var i = 0; i < inputs_len; i++) {
   var input = inputs[i];

   if (input.hasAttribute('skipjval')) {
     continue;
   }

   input.addEventListener("keyup", addInteractedClass);
   input.addEventListener("click", addInteractedClass);
   input.addEventListener("change", addInteractedClass);
   input.addEventListener("valid", addInteractedClass);
   input.addEventListener("invalid", addInteractedClass);
  }
}

function forceInputSetup(parent) {
  var inputs = parent.getElementsByTagName("input");
  var inputs_len = inputs.length;

  var addInteractedClass = function(e) {
    if (!hasClass(e.srcElement, "interacted") && hasClass(e.srcElement, "jval")) {
      e.srcElement.classList.toggle("interacted", true);
    }
  };

  for (var i = 0; i < inputs_len; i++) {
   var input = inputs[i];

   if (input.hasAttribute('skipjval')) {
     continue;
   }

   input.addEventListener("keyup", addInteractedClass);
   input.addEventListener("click", addInteractedClass);
   input.addEventListener("change", addInteractedClass);
   input.addEventListener("valid", addInteractedClass);
   input.addEventListener("invalid", addInteractedClass);
  }
}

// Setup the given input.
function specificInputSetup(input) {
  var addInteractedClass = function(e) {
    if (!hasClass(e.srcElement, "interacted")) {
      e.srcElement.classList.toggle("interacted", true);
    }
  };

   input.addEventListener("keyup", addInteractedClass);
   input.addEventListener("click", addInteractedClass);
   input.addEventListener("change", addInteractedClass);
   input.addEventListener("valid", addInteractedClass);
   input.addEventListener("invalid", addInteractedClass);
}

function startInputsInteracted() {
  var inputs = document.getElementsByTagName("input");
  var inputs_len = inputs.length;

  for (var i = 0; i < inputs_len; i++) {
   var input = inputs[i];

   if (input.hasAttribute('skipjval')) { continue; }

   if (!hasClass(input, "interacted")) {
     input.classList.toggle("interacted", true);
   }
 }
}

function hasClass(element, cls) {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
}
