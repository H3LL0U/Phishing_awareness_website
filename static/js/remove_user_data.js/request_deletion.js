InnerHTMLRemoveDataPopUp = `    <div class="modal">
        <p>Bent u zeker dat u door wilt gaan met het wissen van uw gegevens?</p>
        <p>We zouden het warderen als u mee doet aan het onderzoek</p>
        <button class="btn confirm" onclick="confirmAction()">Ja, wis mijn data</button>
        <button class="btn cancel" onclick="closeModal()">Nee, ik wil toch meedoen aan het onderzoek</button>
    </div>`

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  function deleteCookie(cookieName) {
    
    document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

function askConfirmation() {
    
    document.getElementById("confirmationModal").innerHTML = InnerHTMLRemoveDataPopUp //reset the pop-up
    document.getElementById("confirmationModal").classList.add("show");
}

function closeModal() {
    document.getElementById("confirmationModal").classList.remove("show");
}

async function confirmAction() {
    
    const modalContent = document.querySelector('#confirmationModal .modal');
    modalContent.innerHTML = `<p>Aan het wissen...</p>
    <p>Momentje</p>`
    try {
        const requestStatus = await removeUser(); // Await the response

        // Update the modal content based on the response
        const modalContent = document.querySelector('#confirmationModal .modal');
        
        if (requestStatus && requestStatus.error) {
            // If there's an error in the response
            modalContent.innerHTML = `
                <p>Er is een fout opgetreden:</p>
                <p>${requestStatus.error}</p>
                <button class="btn cancel" onclick="closeModal()">Sluiten</button>
            `;
        } else {
            // If the request was successful
            modalContent.innerHTML = `
                <p>Je gegevens zijn succesvol gewist.</p>
                <button class="btn cancel" onclick="closeModal()">Sluiten</button>
            `;
        }
    } catch (error) {
        console.error('Error during user removal:', error);
        // Update the modal to show an error message
        const modalContent = document.querySelector('#confirmationModal .modal');
        modalContent.innerHTML = `
            <p>Er is een probleem opgetreden bij het verwijderen van uw gegevens.</p>
            <button class="btn cancel" onclick="closeModal()">Sluiten</button>
        `;
    }
}


async function validateUser(userEmail) {
    try {
        const response = await fetch('/api/validate_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user: userEmail }), // Send the user email in the request body
        });

        if (response.ok) {
            const data = await response.json();
            return data.response; // Return the boolean value from the response
        } else {
            console.error('Error validating user:', response.status, response.statusText);
            return false; // Return false if response is not OK
        }
    } catch (error) {
        console.error('Network error:', error);
        return false; // Return false in case of a network error
    }
}




async function removeUser() {
    
    const loginCookie = getCookie("login")
        

    
    if (!loginCookie) {
        console.error('Login cookie not found.');
        return;
    }

    // Create the request payload
    const payload = {
        user: loginCookie 
    };

    try {
        // Send the POST request
        const response = await fetch('/api/remove_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        // Check the response status
        if (response.ok) {
            const data = await response.json();
            deleteCookie("login")
        } else {
            const errorData = await response.json();
            console.error('Error:', errorData); // Handle error (e.g., Wrong request)
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

async function submitSymbols() {
    
    const inputField = document.getElementById("symbolInput"); 
    if (!inputField.value){
        
            showModalMessage("Fout", "Voer eerst de symbolen in!"); 
            return;
        
    }
    const userSymbols = inputField.value



    // Show loading state in the modal
    showModalMessage("Bezig met valideren...", "Even geduld alstublieft.");

    const isValid = await validateUser(userSymbols); // Validate symbols

    if (isValid) {
        
        document.cookie = `login=${userSymbols}; path=/; max-age=${7 * 24 * 60 * 60}`;

        // Refresh the page
        location.reload();
    } else {
        showModalMessage("Fout", "De ingevoerde symbolen zijn niet geldig.");
    }
}
function showModalMessage(title, message) {
    const modal = document.getElementById("confirmationModal");
    const modalContent = modal.querySelector(".modal");

    modalContent.innerHTML = `
        <p><strong>${title}</strong></p>
        <p>${message}</p>
        <button class="btn cancel" onclick="closeModal()">Sluiten</button>
    `;

    modal.classList.add("show"); // Show the modal
}