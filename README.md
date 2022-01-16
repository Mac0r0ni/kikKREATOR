# kikKREATOR
Automated kik account creator (kinda)

# Setup
- Must have Chromedriver installed. To find out your Chromedriver version and instructions on installing, please visit: https://chromedriver.chromium.org/downloads/version-selection After extracting, place it in any drive.
You need to replace the file path of your chromedriver.exe on line 104 in register.py


- Must have the following installed also: https://github.com/tomer8007/kik-bot-api-unofficial
- Open up register.csv in your prefered text editor. Replace the values to your liking.
- Remember, every email and username must NOT be in use!
- If you are making a lot of accounts, i would suggust using the following to check username availability:
- https://github.com/Mac0r0ni/KikNameChecker

#More Set-up instructions:
After you enter the usernames(and other info) you want to make in the register.csv run register.py. It will open up chromedriver.exe and open a browser window going to Kiks captcha, and you will have to solve only 2 (the ones where you "flip" the Animal right side up.
After you have solved the captha, go back to the register.py window and it will show you instructions (just push any key and enter) it will then take the captcha complete token from the chromedriver.exe dev tools, and send that to kik. It will then repeat this process for every account you wish to create.

- 
