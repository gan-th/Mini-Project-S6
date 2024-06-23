let availableKeywords=['Asian Paints','Eicher Motors','Hero MotorCrop', 'Reliance Industries Limited','Tata Steel Limited',"Dr Reddy's Laboratories Limited", 'Shriram Finance Limited','Infosys Limited','Sun Pharmaceutical Industries Limited','Tata Consultancy Services Limited','Maruti Suzuki India Limited','HCL TECHNOLOGIES','Coal India Limited','LTIMindtree Limited','HDFC Life Insurance Company Limited','Bajaj Auto Limited', 'Britannia Industries Limited','Nestlé India Limited','Hindalco Industries Limited','Larsen & Toubro Limited','Tata Consumer Products Limited', 'Wipro Limited','Titan Company Limited','Bharat Petroleum Corporation Limited','Bajaj Finance Limited','JSW Steel Limited','ICICI Bank Limited','Oil and Natural Gas Corporation Limited','Bharti Airtel Limited', "Divi's Laboratories Limited",'SBI Life Insurance Company Limited','Cipla Limited','Grasim Industries Limited','Hindustan Unilever Limited','MAHINDRA &MAHINDRA','Tata Motors Limited','Apollo Hospitals Enterprise Limited','State Bank of India','Kotak Mahindra Bank Limited','Adani_Enterprise','HDFC Bank Limited','Power Grid Corporation of India Limited','Axis Bank Limited','NTPC Limited','Tech Mahindra Limited', 'Adani Ports and Special Economic Zone Limited','UltraTech Cement Limited'];

const resultsBox=document.querySelector(".result_box");

const inputBox=document.getElementById("input_box");

inputBox.onkeyup =function(){
  let result = [];
  let input=inputBox.value;
  if(input.length){
    result = availableKeywords.filter((keyword)=>{
      return keyword.toLowerCase().includes(input.toLowerCase());
    });
    console.log(result);
  }
  display(result);

  if(!result.length){
    resultsBox.innerHTML='';
  }
}

function display(result){
  const content =result.map((list)=>{
    return "<li onclick=selectInput(this)>" + list + "</li>";
  });

  resultsBox.innerHTML="<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
  inputBox.value=list.innerHTML;
  resultsBox.innerHTML='';
}
