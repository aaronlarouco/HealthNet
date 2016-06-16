function setupPatientTutorial() {
  var tutorial0 = document.getElementById('tutorial0');

  // Create the faded black background that covers the entire page
  var fadedBg = document.createElement("div");
  fadedBg.setAttribute('id', 'tut-faded-bg');
  fadedBg.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
  fadedBg.style.position = "fixed";
  fadedBg.style.top = "0";
  fadedBg.style.left = "0";
  fadedBg.style.width = "100%";
  fadedBg.style.height = "100%";
  fadedBg.style.zIndex = "5000";
  document.body.appendChild(fadedBg);

  var container = document.createElement("div");
  container.style.position = "absolute";
  container.style.width = "70%";
  container.style.top = "50%";
  container.style.left = "50%";
  container.style.transform = "translate(-50%, -50%)";
  fadedBg.appendChild(container);

  var innerContainer = document.createElement("div");
  innerContainer.style.width = "100%";
  innerContainer.style.height = "100%";
  innerContainer.style.backgroundColor = "#ffffff";
  innerContainer.style.borderRadius = "10px";
  innerContainer.style.opacity = "0";
  innerContainer.style.transform = "scale(0)";
  innerContainer.className = "fade-grow-in";
  container.appendChild(innerContainer);

  var divider = document.createElement("div");
  divider.style.width = "100%";
  divider.style.padding = "5px";
  divider.style.margin = "0 auto 8px auto";
  divider.style.backgroundColor = "#dfdfdf";
  divider.style.borderTopLeftRadius = "8px";
  divider.style.borderTopRightRadius = "8px";
  var title = document.createElement("h1");
  title.style.textAlign = "center";
  title.style.marginTop = "5px";
  title.style.marginBottom = "5px";
  divider.appendChild(title);
  innerContainer.appendChild(divider);

  tutorial0.style.display = "block";
  title.innerHTML = tutorial0.getAttribute('divtitle');
  innerContainer.appendChild(tutorial0);

  $("#tutorial0-continue").click(function() {
    fadedBg.className = "fade-out";
    innerContainer.className = "fade-grow-out";

    setTimeout(function() {
      fadedBg.parentNode.removeChild(fadedBg);
    }, 200);

    var userHolder = document.getElementById('username-holder');
    var username = userHolder.getAttribute("username");

    $.ajax({
      url : "/profiles/" + username + "/endtut",
      dataType: "json",
      data : {
          client_response : "",
          csrfmiddlewaretoken: '{{ csrf_token }}'
      },
    });
    return false;
  });
}
