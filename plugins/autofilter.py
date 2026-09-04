

def get_short_link(long_url: str, api_token: str) -> str:
    """
    URL Shortener API से Short Link जनरेट करने का पूरा फंक्शन।
    
    :param long_url: जिस ओरिजिनल लिंक को छोटा करना है।
    :param api_token: आपकी Shortener वेबसाइट का API Token/Key.
    :return: जनरेट किया गया Short Link या एरर मैसेज।
    """
    # अपनी Shortener वेबसाइट का बेस API Endpoint यहाँ बदलें
    api_url = "https://example-shortener.com/api"
    
    # API के लिए जरूरी पैरामीटर्स
    params = {
        'api': api_token,
        'url': long_url
    }
    
    try:
        # API को रिक्वेस्ट भेजना
        response = requests.get(api_url, params=params, timeout=10)
        
        # अगर सर्वर का रिस्पॉन्स OK (HTTP 200) है
        if response.status_code == 200:
            data = response.json()
            
            # रिस्पॉन्स फॉर्मेट चेक करना (अधिकांश शॉर्टनर 'shorturl' या 'url' की (key) रिटर्न करते हैं)
            if data.get("status") == "success" or "shorturl" in data:
                return data.get("shorturl")
            elif "url" in data:
                return data.get("url")
            else:
                return f"Error: API response missing link key. Response: {data}"
        else:
            return f"Error: Server returned status code {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "Error: Request timed out. API server isn't responding."
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to API ({str(e)})"


# ==========================================
# इस्तेमाल करने का तरीका (Example Usage):
# ==========================================
if __name__ == "__main__":
    MY_API_TOKEN = "YOUR_API_KEY_HERE"  # अपना API Token यहाँ डालें
    TEST_URL = "https://t.me/your_channel_name"
    
    short_link = get_short_link(TEST_URL, MY_API_TOKEN)
    print("Generated Short Link:", short_link)
