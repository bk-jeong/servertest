const imgtags = document.querySelectorAll(".imgtag"); // 각인 이미지 태그들 묶음
const renkins = document.querySelectorAll(".renkin"); // 이미지가 들어갈 구역(div) 들의 묶음

imgtags.forEach((imgtag) => {
  // 각각의 각인이미지 를 변수 imgtag로 나눔
  imgtag.addEventListener("dragstart", () => {
    // 각 이미지를 드래그 시작했을때
    imgtag.classList.add("dragging"); // 각 이미지에 드래그중 이라는 클래스 추가
  });

  imgtag.addEventListener("dragend", () => {
    // 드래그가 끝나면
    imgtag.classList.remove("dragging"); // 드래그중 클래스 삭제
  });
});

renkins.forEach((renkin) => {
  //각 이미지가 들어갈 구역을 나눔
  renkin.addEventListener("dragover", (e) => {
    // 드래그가 이미지 구역에 들어오면
    e.preventDefault(); // 기본 동작 캔슬
    const afterElement = getDragAfterElement(renkin, e.clientX, e.clientY); // 드래그중인 마우스의 위치지정
    const draggable = document.querySelector(".dragging"); // 드래그 중인 이미지 객체 지정 (function getDragAfterElement 참조)
    if (afterElement === undefined) {
      // 만약 드래그중인 이미지가 그 구역의 마지막이라면
      renkin.appendChild(draggable); // 이미지를 그구역 끝에 추가한다
    } else {
      // 끝이 아니라면 드래그중인 위치의 앞에 이미지를 추가한다
      renkin.insertBefore(draggable, afterElement);
    }
    e.target.classList.add("dragover"); // 드래그 중인 구역에 dragover 클래스 추가
  });

  renkin.addEventListener("dragenter", (e) => {
    // 드래그 구역에서 벗어나면
    e.target.classList.remove("dragover"); // dragover 클래스 삭제
  });

  renkin.addEventListener("dragleave", (e) => {
    e.target.classList.remove("dragover"); // 드래그중 취소되면 dragover 클래스 삭제
  });

  renkin.addEventListener("drop", (e) => {
    e.target.classList.remove("dragover"); // 드롭으로 드래그가 끝나면 dragover 클래스 삭제
    e.preventDefault();
  });
});

function getDragAfterElement(target, x, y) {
  // 드래그중인 구역에 현재 마우스 위치 찾는 function
  const draggableElements = [
    ...target.querySelectorAll(".imgtag:not(.dragging)"),
  ]; // 구역안에 드래그 중이지 않은 각 객채들을 감지
  return draggableElements.reduce(
    // 구역안의 드래그중인 객체와 안에 있던 객체의 위치를 비교하여 출력
    (closest, child) => {
      const box = child.getBoundingClientRect();
      const offsetx = x - box.left - box.width / 2; // 현재 위치의 정확한 x값을 세팅
      const offsety = y - box.top - box.height / 2; // 연재 위치의 정확한 y값을 세팅
      // console.log(offset);
      if (offsetx < 0 && offsetx > closest.offset) {
        // 기존에 있던 객체와의 x값 비교
        if (offsety < 0 && offsety > closest.offset) {
          // 기존에 있던 객체와의 y값 비교
          return { offset: (offsetx, offsety), element: child };
        } else {
          return closest;
        }
      } else {
        return closest;
      }
    },
    { offset: Number.NEGATIVE_INFINITY }
  ).element;
}

//셀렉터한개로 통일
const elements = document.getElementsByName("shop");

for (let i = 0; i < elements.length; i++) {
  elements[i].addEventListener("click", raidChange);
}

function raidChange(event) {
  if (document.getElementById("kamen").checked) {
    location.href = "/make/kamen";
  } else if (document.getElementById("illiakan").checked) {
    location.href = "/make/illiakan";
  } else if (document.getElementById("echidna").checked) {
    location.href = "/make/echidna";
  }
}

document.getElementById("send").onclick = function () {
  var sicon = "";
  var data = [, , , , ,];
  var T = 0;

  const lains = document.getElementsByClassName("renkin");
  for (let index = 0; index < lains.length; index++) {
    var lain = lains.item(index);
    var icons = lain.getElementsByClassName("imgtag");
    for (let index = 0; index < icons.length; index++) {
      var icon = icons.item(index);
      if (sicon == "") {
        sicon = sicon + icon.id;
      } else {
        sicon = sicon + "," + icon.id;
      }
    }
    data[T] = sicon;
    sicon = "";
    T++;
  }
  var raid = "";
  for (var radio of document.getElementsByName("shop")) {
    if (radio.checked) {
      raid = radio.value;
    }
  }

  const form = document.createElement("form");
  form.setAttribute("method", "post");
  form.setAttribute("action", `/res/${raid}/${pk}`)

  const Raid = document.createElement("input");
  Raid.setAttribute("type", "hidden");
  Raid.setAttribute("name", "raid");
  Raid.setAttribute("value", raid);

  const Atia = document.createElement("input");
  Atia.setAttribute("type", "hidden");
  Atia.setAttribute("name", "1tia");
  Atia.setAttribute("value", data[0]);

  const Btia = document.createElement("input");
  Btia.setAttribute("type", "hidden");
  Btia.setAttribute("name", "2tia");
  Btia.setAttribute("value", data[1]);

  const Ctia = document.createElement("input");
  Ctia.setAttribute("type", "hidden");
  Ctia.setAttribute("name", "3tia");
  Ctia.setAttribute("value", data[2]);

  const Dtia = document.createElement("input");
  Dtia.setAttribute("type", "hidden");
  Dtia.setAttribute("name", "4tia");
  Dtia.setAttribute("value", data[3]);

  const Etia = document.createElement("input");
  Etia.setAttribute("type", "hidden");
  Etia.setAttribute("name", "5tia");
  Etia.setAttribute("value", data[4]);

  const Tierout = document.createElement("input");
  Tierout.setAttribute("type", "hidden");
  Tierout.setAttribute("name", "tierout");
  Tierout.setAttribute("value", data[5]);

  form.appendChild(Raid);
  form.appendChild(Atia);
  form.appendChild(Btia);
  form.appendChild(Ctia);
  form.appendChild(Dtia);
  form.appendChild(Etia);
  form.appendChild(Tierout);

  document.body.appendChild(form);
  form.submit();
};
