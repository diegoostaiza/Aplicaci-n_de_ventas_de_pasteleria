

const radio1 = document.getElementById('form-1-radio');
const radio2 = document.getElementById('form-2-radio');

radio2.addEventListener("click", (e) =>{
    const form1 = document.getElementById('form-1');
    const form2 = document.getElementById('form-2');
    form2.classList.toggle("hidden");
    form1.classList.add("hidden");
    
})
radio1.addEventListener("click", (e) =>{
    const form1 = document.getElementById('form-1');
    const form2 = document.getElementById('form-2');
    form1.classList.toggle("hidden");
    form2.classList.add("hidden");
    
})