function checkPassword(event) {
    const passwordInput = event.target.value;
    if (passwordInput) {
        window.location.href = '/typed';
    }
}
//checks if the user cookie coresponds with the provided email
async function validateUserWithCookie(user) {
    try {
        
        const response = await fetch('/api/validate_user_with_cookie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user: user }) 
        });

        
        if (response.ok) {
            const data = await response.json(); 
            return data.response; 
        } else {
            console.error('Error:', response.statusText); 
            return false; 
        }
    } catch (error) {
        console.error('Request failed:', error); 
        return false; 
    }
}