document.getElementById("viewAllResult").onclick = function () {
  const form = document.createElement("form");
  form.setAttribute("method", "get");
  form.setAttribute("action", "/res/all/");

  var raids = document.getElementsByName("shop");
  var raid;
  for (let i=0; i<raids.length; i++) {
    if (raids[i].checked) {
      raid=raids[i].value;
    }
  }
  const Raid = document.createElement("input");
  Raid.setAttribute("type", "hidden");
  Raid.setAttribute("name", "raid");
  Raid.setAttribute("value", raid);

  form.appendChild(Raid);
  document.body.appendChild(form);

  form.submit();
};
