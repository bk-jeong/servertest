checkboxs = document.getElementsByClassName("bonus").length;

for (var i = 0; i < checkboxs; i++) {
  document.getElementsByClassName("bonus")[i].addEventListener("change", (e) => {
    if (e.target.checked == false) {
      document.getElementById("allbonus").checked = false;
    }
  });
}

const stage2select = document.getElementById("stage2");
const stage3select = document.getElementById("stage3");
const stage4select = document.getElementById("stage4");


stage4select.addEventListener("change", () => {
  if (stage4select.options[0].selected == true) {
    document.getElementById("auction").checked = false;
  }
  if (stage3select.options[stage3select.selectedIndex].value=="dont"){
    stage4select.options[1].selected = true;
  }
});

stage3select.addEventListener("change", () => {
  if (stage2select.options[stage2select.selectedIndex].value=="dont"){
    stage3select.options[2].selected = true;
  }
  if (stage3select.options[stage3select.selectedIndex].value=="dont"){
    stage4select.options[1].selected = true;
  }
});

stage2select.addEventListener("change", () => {
  if (stage2select.options[stage2select.selectedIndex].value=="dont"){
    stage3select.options[2].selected = true;
    stage4select.options[1].selected = true;
  }
});

invennum = 0;
function invencheck() {
  invenvalue = document.getElementById("inven").value;
  if (invenvalue == "") {
    document.getElementById("inven").value = invennum;
  }
  invennum = document.getElementById("inven").value;
}

function hendscheck() {
  handvalue = document.getElementById("hands").value;
  range = "9123456780";
  if (handvalue.length > 1) {
    str = document.getElementById("hands").value.toString();
    str = str.substr(1, 1);
    num = Number(str);
    document.getElementById("hands").value = num;
    if (num > 5) {
      document.getElementById("hands").value = 5;
    }
  }
  if (range.indexOf(handvalue) == 0) {
    document.getElementById("hands").value = 0;
  }
  if (num < 5) {
    document.getElementById("fstreward").checked = false;
  } else {
    document.getElementById("fstreward").checked = true;
  }
}

document.getElementById("fstreward").addEventListener("change", (e) => {
  if (document.getElementById("hands").value <5) {
    document.getElementById("fstreward").checked = false;
  }
});


document.getElementById("collCalc").onclick = function () {
  deleteCookie("opts");
  var invenv = document.getElementById("inven").value; // 소지 재료 개수

  var stage1 = document.getElementById("stage1"); // 입장 정보
  var stage2 = document.getElementById("stage2");
  var stage3 = document.getElementById("stage3");
  var stage4 = document.getElementById("stage4");
  var stage1v = stage1.options[stage1.selectedIndex].value;
  var stage2v = stage2.options[stage2.selectedIndex].value;
  var stage3v = stage3.options[stage3.selectedIndex].value;
  var stage4v = stage4.options[stage4.selectedIndex].value;

  var handsv = document.getElementById("hands").value; // 손길 체크

  var fstrewardv = document.getElementById("fstreward").checked; // 첫 클리어 체크

  // 더보기 체크
  var stage1Plus = document.getElementById("stage1Plus").checked;
  var stage2Plus = document.getElementById("stage2Plus").checked;
  var stage3Plus = document.getElementById("stage3Plus").checked;
  var stage4Plus = document.getElementById("stage4Plus").checked;

  var auctionv = document.getElementById("auction").checked; // 경매 체크

  enterv = [0, 0, 0, 0];

  if (stage1v == "normal" && stage1Plus) {
    enterv[0] = 1;
  } else if (stage1v == "normal" && !stage1Plus) {
    enterv[0] = 2;
  } else if (stage1v == "hard" && stage1Plus) {
    enterv[0] = 3;
  } else if (stage1v == "hard" && !stage1Plus) {
    enterv[0] = 4;
  }
  if (stage2v == "normal" && stage2Plus) {
    enterv[1] = 1;
  } else if (stage2v == "normal" && !stage2Plus) {
    enterv[1] = 2;
  } else if (stage2v == "hard" && stage2Plus) {
    enterv[1] = 3;
  } else if (stage2v == "hard" && !stage2Plus) {
    enterv[1] = 4;
  }

  if (stage3v == "normal" && stage3Plus) {
    enterv[2] = 1;
  } else if (stage3v == "normal" && !stage3Plus) {
    enterv[2] = 2;
  } else if (stage3v == "hard" && stage3Plus) {
    enterv[2] = 3;
  } else if (stage3v == "hard" && !stage3Plus) {
    enterv[2] = 4;
  }

  if (stage4v == "hard" && stage4Plus) {
    enterv[3] = 3;
  } else if (stage4v == "hard" && !stage4Plus) {
    enterv[3] = 4;
  }

  const optsObject = {
    entries: enterv,
    auction: auctionv,
    fstreward: fstrewardv,
    hands: handsv,
    inven: invenv,
  };
  opts = JSON.stringify(optsObject);
  document.cookie = `opts=${opts}; path=/; max-age=600;`;
  location.href = "/calc/";
};

function deleteCookie(name) {
  document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}
