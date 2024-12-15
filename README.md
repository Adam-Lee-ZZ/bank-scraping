**Glory to Hong Kong**

# bank-scrapping
Crawler for the data of the Bank of East Asia's online real estate valuation system in Hong Kong. If you need to crawl some data that needs to be selected in a given table, it will be helpful to refer to this program.
You can adjust the parameters in the program, especially in the get_building function, to adapt it to your project.
If the site is designed with an anti-crawler mechanism, such as validating random token values, you may need to use the following code.
```
url = 'https://www.hkbea-cyberbanking.com/ibk/loan/property/valuation/pub/input'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': 'token'})
    
    if token_input:
        token = token_input['value']
        post_url = 'https://www.hkbea-cyberbanking.com/ibk/loan/property/valuation/pub/confirm'
        headers = {...} #based on your website
        data = {
            ...
            'struts.token.name':'token'
            'token':'token'
            ...  #based on your data
          }
        post = request.post(post_url, data = data, headers = headers)
```

**May liberation & democrocy back to China**
