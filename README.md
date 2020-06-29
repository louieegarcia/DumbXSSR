# DumbXSSR (XSS Reflected Scanner)
*** FOR EDUCATIONAL PURPOSES ONLY ***  
or like if you're doing a legal pentest or something. Keyword legal, ok?
## Description
DumbXSSR Reflection Scanner scans a webpage given by a URL that contains variables, and checks if a reflected XSS attack exists. If the attack exists, then DumbXSSR will test several payloads to see if they work.
Any payload that successfuly works will print to the screen for the user to verify. Right now only three payloads come with the script by default.
## Arguments
The current arguments you can pass are:
- URL (Necessary argument)
- Cookie (Optional)
- Payloads (Optional)

### URL
The URL needs to contain variables in order to test for XSS reflected attacks. I plan to add functionality for web forms.  
An example of how the URL should look like.
> somesite(dot)com?ooooVariable=SomeValue&AnotherVariable=SomeOtherValue

### Cookie
This argument allows you to specify cookie information, if needed to access a certain webpage.  
The values should be passed as an argument and should look like this.
> ./DumbXSSR --cookie user=admin,userid=0xdeadbeef,dumb=maybe URL

### Payloads
This argument allows you to load a list of payloads to try on a target via a path to the text file. List items must be seperated by a new line in order for it to work.
> ./DumbXSSR --path /path/to/juicy/payloads URL  
  
### Potential Future Ideas
- Would love to add the ability to add this script to other python scripts, and create a useful API.
-- Like adding this to a webcrawler easily and scan an entire website for XSS reflected attacks.
- Make a LATeX report for Pentesters, or any other useful format necessary
- Support for webforms
