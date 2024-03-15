This project accesses Google News and scrapes the articles for a customizale query. The articles are saved in the JSON file with the following information: Link, Domain, Title, Description, Date.

Node.js+Express then takes this JSON data and feeds it to the OpenAI API, which summarizes the data, with a cutomizable prompt.

HOW TO RUN
---
1. First, in services/openaiService.js, replace 'INSERT KEY' with your OpenAI API key 
**'Authorization': 'INSERT KEY'**

2. Before you run the program, there are a few things that can be cutomized:
    //a. **scripts/news.py**
    You can customize the url, where the program will scrape news, the number of pages
    of news to scrape, as well as the max number of days ago the articles have been published. 
    
    These parameters are currently set to:
    base_url = 'https://www.google.com/search?q=hottest+korean+movies+2024&tbm=nws'
    num_pages = 5
    days_ago = 45

    //b. **routes/api.js**
    You can customize the promt with which chatGPT will analyze the news. It is currently set to 'Which Korean TV shows and movies were mentioned the most in the past month in the news?'

3. In terminal, go to the project directory and type in "node app.js". It should print out "Server is running on port 3000".

4. In the browser, go to the page: http://http://localhost:3000 and press "Get News". The output will be in the textbox.

5. The data folder has sample output.