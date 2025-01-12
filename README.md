<h1>Draft Pick ML With Weighted Graph</h1>
This repository was created to fulfill the requirements of a discrete mathematics paper assignment about the implementation of weighted graph to get the best hero draft in Mobile Legend by using the counter and compatibility score provided by the official Mobile Legends: Bang Bang website. This implmentation is to suffice the 

<h2>Folder Structure</h2>
- Docs : Contain the file needed to supply the paper.
- Script : Contain script to scrape data from the web and combining it to make it usable for the program.
- Data : Contains all the data including the final data and the raw scraped data.

<h2>Run The Program</h2>
On running the program you may want to extract the data first to get the most recent data based on the web and then run the main script. Dont forget to install all the library that is being used including Selenium, Webdriver, and BeautifulSoup.

1. run weight_scraper.py
2. run scoreid_scraper.py
3. run extract_scoreid.py
4. run hero_mapper.py
5. run finaldata_combiner.py
6. run main.py

Note : run graph_visualization to get see how each hero connect with other hero in a graph.
