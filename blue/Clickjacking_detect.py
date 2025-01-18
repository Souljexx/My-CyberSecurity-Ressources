import requests
from bs4 import BeautifulSoup

def check_clickjacking(url):
    try:
        response = requests.get(url)
        
        # Get the 'X-Frame-Options' and 'Set-Cookie' and 'Content-Security-Policy' headers
        x_frame_options = response.headers.get('X-Frame-Options')
        cookies = response.headers.get('Set-Cookie')
        content_security_policy = response.headers.get('Content-Security-Policy')

        # Parse the page content
        page = BeautifulSoup(response.content, 'html.parser')

        frame_busting = page.find_all(string=lambda text: "if (self ! == top)" in text or "window.top.location" in text)

        # Check for frame-busting script
        if frame_busting:
            print(f"The website at {url} includes frame-busting scripts.")
        else:
            print(f"The website at {url} does not include frame-busting scripts.")
        
        # Check for 'X-Frame-Options' header
        if x_frame_options:
            print(f"The website at {url} has X-Frame-Options header: {x_frame_options}")
        else:
            print(f"The website at {url} does not have an X-Frame-Options header.")

        # Check for SameSite=Strict in cookies 
        if (cookies):  
            if 'SameSite=Strict' in cookies:
                print(f"The website at {url} has 'SameSite=Strict' set in cookies.")
            
            else:
                print(f"The website at {url} does not have 'SameSite=Strict' set in cookies.")
        else:    
            print(f"No 'Set-Cookie' header found for the website at {url}.")
        
        # Check for 'frame-ancestors in Content-Security-Policy header
        if content_security_policy and 'frame-ancestors' in content_security_policy:
            print(f"The website at {url} has 'frame-ancestors' directive in Content-Security-Policy:{content_security_policy}")
        else:
            print(f"The website at {url} doesn't have 'frame-ancestors' directive in Content-Security-Policy.")



        # Check for 'X-Frame-Options', 'Set-Cookie', 'Content-Security-Policy headers and frame-busting script 
        if not (x_frame_options and cookies and content_security_policy and frame_busting):
            print("This site may be vulnerable to clickjacking.")

    except requests.exceptions.RequestException as e:
        print(f"An error occured while checking the website: {e}")

website = input("Enter your website URL (e.g., https://example.com): ")
check_clickjacking(website)
