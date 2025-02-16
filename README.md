# Phishing awareness website

## What is this website for?
This website is made as part of the research on the efficiency of social engineering in the education sector.
You can find more about it here https://github.com/users/H3LL0U/projects/8?pane=info
It is built using the Flask framework and is using MongoDB as it's database.

## What is this website's functionality?
This website is made to educate people who clicked on a "phshing link". Only the users whose email address is known are tracked.

### Main page
Contains various information on how to protect yourself from phishing. There are tips on how you can recognize phishing attempts, including common red flags
to look out for, such as suspicious links, urgent requests for personal information, and unexpected emails from unknown senders. 

### Data page
Gives an overview on the data from the research such as: procentage of users who clicked on the phishing link, procentage of users who started typing in the password field,
which e-mail types had the most success.

### About page
Contains information about the project

### Secret page that can only be accessed through e-mail
Contains a fake login page. If the user starts typing a password in the password field he gets redirected to the Main page. It is important to note that the user gets redirected immediately (even after typing a single letter) 
as to avoid any panic.

## Contribution
If you want to help to improve the website or contribute in any other way please create an issue!
