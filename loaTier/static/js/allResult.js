window.onload = function(){
  window_heihgt=window.innerHeight; // 처음 페이지가 열렸을때 한번 윈도우의 사이즈를 측정하는 코드
  window_width=window.innerWidth;
  const tooltip_target = document.querySelectorAll(".icon");  // 빈공간이 아닌 아이콘에 만반응하도록 인식 태그 위치 수정
  //const tooltip_target = document.getElementsByClassName("ebox")
  const tooltip = document.querySelectorAll(".tooltip_image");
  window.addEventListener('resize',()=>{ // 이후 윈도우의 사이즈가 변경 되었을때 그 변경된 사이즈를 측정하는 코드
    window_heihgt=window.innerHeight;
    window_width=window.innerWidth;
  });

  tooltip_target.forEach( function (ebox,index){
    ebox.addEventListener('mouseover',()=>{
      // 기존 index방식으로는 툴팁이 마우스의 위치값과 실행값에 차이가 생겨서 툴팁창을 외부로 빼두었고
      // 그 위치를 index로는 가져올수없어서 이미지에 name으로 각인명을 지정하여 
      // 각인 명과 같은 id를 가진 툴팁이 인식되도록 코드를 수정함
      chack=ebox.getAttribute('name'); 
      document.getElementById(chack).style.display = 'block';
      //alert(e.clientY);
    })
    ebox.addEventListener('mousemove',(e)=>{ // 툴팁이 아이콘 위에 올라가면 마우스를 따라 이동하면서 보이도록 수정
      chack=ebox.getAttribute('name');
      if (e.clientY >= window_heihgt/2) { // 마우스가 윈도우창의 절반을 이동하면 표시되는 위치가 달라지게 설정하는 코드
       document.getElementById(chack).style.top = (e.pageY-320)+"px";
      }else {
        document.getElementById(chack).style.top = e.pageY+5+"px";
      }
      if (e.clientX >= window_width/2){
        document.getElementById(chack).style.left = (e.pageX-325)+"px";
      }else {
        document.getElementById(chack).style.left = e.pageX+5+"px";
      }
    })
  });
  
  // change display to 'none' on mouseleave
  tooltip_target.forEach(function(ebox,index){
    ebox.addEventListener('mouseleave', () => {
      chack=ebox.getAttribute('name');
      document.getElementById(chack).style.display = 'none';
      //tooltip[index].style.display = 'none';
    })
  }, false);
}

const raids = document.getElementsByName("shop");
raids.forEach((raid) => {
  raid.addEventListener('click', function () {
    location.href= `./?raid=${raid.value}`;
  });
});