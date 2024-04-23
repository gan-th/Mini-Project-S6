const showPopupBTN = document.querySelector(".login-btn");
const hidePopupBTN = document.querySelector(".form-popup .close-btn");
const formPopup = document.querySelector(".form-popup");
const loginSignupLink=document.querySelectorAll(".form-box .bottom-link a");

//shows login
showPopupBTN.addEventListener("click",()=>{
    document.body.classList.toggle("show-popup");
});

//closes login
hidePopupBTN.addEventListener("click",()=>showPopupBTN.click());

loginSignupLink.forEach(link=>{
    link.addEventListener("click",(e)=>{
      e.preventDefault();
      //if signup is clicked then add "show-signup class to form popup else remove class"
      formPopup.classList[link.id==="signup-link" ? 'add' :'remove']("show-signup");
    });
});
