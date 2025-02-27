
let emailBox = document.getElementById('email-box');
let passwordBox = document.getElementById('password-box');
let loginArea = document.getElementById("login-area")
let emailInput = document.getElementById("email-input")
let errorMessage = document.getElementById("error-message")
document.getElementById('email-form').addEventListener('submit',async function(event) {



    event.preventDefault(); 
    
    result = await validateUserWithCookie(emailInput.value) 
    if (result ===false){
        errorMessage.style.display = "block"
        return
    }
    
    setTimeout(() =>{
        errorMessage.style.display = "none"
    emailBox.style.animation = '0.25s Scroll-left ease-in-out forwards';
    
    
    setTimeout(() => {
        
        passwordBox.style.display = "flex"
        emailBox.style.display = "none"
        passwordBox.style.animation = '0.25s Scroll-left ease-in-out reverse'; 
        setTimeout(() => {
        
        
        
        passwordBox.style.animation = "none"
        emailBox.style.animation = "none"
    }, 249); 
    }, 249); 
},250)

});


document.getElementById('backButton').addEventListener('click', function(event) {


passwordBox.style.animation = '0.25s Scroll-left ease-in-out forwards'; 



setTimeout(() => {
    
    emailBox.style.display = 'flex'; 
    passwordBox.style.display = 'none'
    emailBox.style.animation = '0.25s Scroll-left ease-in-out reverse'; 
    
    
    setTimeout(() => {
        
        
        passwordBox.style.animation = "none"
        emailBox.style.animation = "none"
    }, 249); 

}, 249); 
});


