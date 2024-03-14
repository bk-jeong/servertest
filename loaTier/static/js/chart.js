function test(testalldata) {

  var datakeys=Object.keys(testalldata);
  //각 각인별 데이터 분리하기
  var testdatas=Object.values(testalldata);
  votecount=testdatas.pop()
  datakeys.pop()
  var zero=new Array(datakeys.length)
  // 빈 변수값 
  var testdata='';
  // 그래프 에 들어갈 정보들을 한번에 모아두기
  var pieChartData=new Array(datakeys.length);
  var pieChartData2=new Array(datakeys.length);
  
  for (let i = 0; i < testdatas.length; i++) {  //각인 수만큼 작업하게 하기
      testdata=testdatas[i];
      var testkey=Object.keys(testdata);  //키값 가져오기
      var testvalue=Object.values(testdata); // 벨류값 가져오기
      vote=testvalue.pop();
      testkey.pop();
      
      
      zero[i]=testvalue;
      for (let index = 0; index < testkey.length; index++) {  //키값에 벨류값을 퍼센트로 계산하여 넣어주는 작업
        testkey[index]= testkey[index]+"("+(testvalue[index]*100).toFixed(1)+"%)"
      }
      
      pieChartData[i]={   // 그래프에 들어갈 데이터를 정리하는 작업
        labels:testkey,  // 그래프 분류기준인 이름값이 들어가는곳
        datasets: [{  // 분류된 데이터 
          data:testvalue,  // 데이터 값
          backgroundColor:['red','#FF9900','#FFFF00','#99FF00','#99CCFF','#084EE7'], // 데이터별 색상 선택 * 나중에 같이 수정할 사항
        }]
      };
      vote=vote/votecount*100
      pieChartData2[i]={   // 그래프에 들어갈 데이터를 정리하는 작업
        labels:["총 참여인원:"+votecount+"명","투표 인원("+(100-vote).toFixed(1)+"%)","미투표("+vote.toFixed(1)+"%)"],  // 그래프 분류기준인 이름값이 들어가는곳
        datasets: [{  // 분류된 데이터 
          data:[0,100-vote.toFixed(1),vote.toFixed(1)],  // 데이터 값
          backgroundColor:['balck','#99FF00','gray'], // 데이터별 색상 선택 * 나중에 같이 수정할 사항
        }]
      };
    };
  //let pieChartDraw=function(){  // 데이터를 그래프로 만드는 작업
    for (let i = 0; i < datakeys.length; i++) {
        let ctx= document.getElementById(datakeys[i]+"a").getContext('2d');  // 2D형 데이터를 만든다 선언
        window.pieChert= new Chart(ctx,{   //만들 그래프의 옵션 설정
          type:'pie',   // 그래프 타입은 원형 (파이구조)
          data:pieChartData[i],  // 만들어둔 데이터 등록
          options: {   // 여러 옵션 설정
              responsive:false,  // 윈도우 사이즈변동에 따른 그래프 그기 변동 막아주는 기능
              elements :{
                arc:{
                  borderColor : ['#EC423C','#EC7310','#ECE001','#1EEB16','#07E0E7'],  //* 나중에 같이 수정할 사항
                  borderWidth : 3,  // 파이 차트 보더크기
                  borderAlign : 'inner', // 보더가 겹쳐지지 않게 하기
                    
                },
              },
              plugins:{  // 그래프 내부 옵션 변경을 위한 세부 설정
                  legend: { // 나눈 티어 이름들을 보여주는 옵션
                      position: 'top', // 우측으로 이동
                      align:'start', // 상단으로 이동
                      maxWidth : 200, // 사이즈
                      labels:{
                          boxWidth: 15,
                          usePointStyle: true,
                          pointStyle: 'circle', // 라벨의 색상 표시가 둥근 모양으로 보이게
                          color : 'black', // 라벨 색상 * 나중에 수정할 사항
                          filter: function(legendItem) { // 라벨에 결과값이 0프로 인게 안보이게 해주는 필터
                              return zero[i][legendItem.index] != 0 
                          }
                        }
                      },
                  tooltip: {  // 마우스 올리면 보이는 툴팁 설정
                      enabled:false // 툴팁 해제
                  },
                }
            }
        });
        document.getElementsByClassName("tooltip_image")[i].style.display = 'none';
    //}
      };

      for (let i = 0; i < datakeys.length; i++) {
        let ctx= document.getElementById(datakeys[i]+"b").getContext('2d');  // 2D형 데이터를 만든다 선언
        window.pieChert= new Chart(ctx,{   //만들 그래프의 옵션 설정
          type:'pie',   // 그래프 타입은 원형 (파이구조)
          data:pieChartData2[i],  // 만들어둔 데이터 등록
          options: {   // 여러 옵션 설정
              responsive:false,  // 윈도우 사이즈변동에 따른 그래프 그기 변동 막아주는 기능
              elements :{
                arc:{
                  borderColor : ['white','#1EEB16','gray'],  //* 나중에 같이 수정할 사항
                  borderWidth : 3,  // 파이 차트 보더크기
                  borderAlign : 'inner', // 보더가 겹쳐지지 않게 하기
                    
                },
              },
              plugins:{  // 그래프 내부 옵션 변경을 위한 세부 설정
                  legend: { // 나눈 티어 이름들을 보여주는 옵션
                      position: 'top', // 우측으로 이동
                      align:'start', // 상단으로 이동
                      maxWidth : 200, // 사이즈
                      labels:{
                          boxWidth: 15,
                          usePointStyle: true,
                          pointStyle: 'circle', // 라벨의 색상 표시가 둥근 모양으로 보이게
                          color : 'black', // 라벨 색상 * 나중에 수정할 사항
                          // filter: function(legendItem) { // 라벨에 결과값이 0프로 인게 안보이게 해주는 필터
                          //     return zero[i][legendItem.index] != 0 
                          // }
                        }
                      },
                  tooltip: {  // 마우스 올리면 보이는 툴팁 설정
                      enabled:false // 툴팁 해제
                  },
                }
            }
        });
        document.getElementsByClassName("tooltip_image")[i].style.display = 'none';
    //}
      };
  }
