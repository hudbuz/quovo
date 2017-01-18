To run program using cik, enter python holdings.py -cik ******** into the command line, with * being replaced with CIK
To run program using ticker, enter 'python holdings.py -tik ****** into the command line, with * being replaced with Ticker


To crawl through the multiple SEC.gov document pages, I utilized Selenium and Chromedriver to open a browser,
find the appropriate documents, and open the 13F-HR in the browser. Once I reached the final 13F-HR report, I used BeautifulSoup to parse through the XML and generate the appropriate holdings tab separated file. In the file, I included each holdings Name, Title Class, CUISP, Value, SSHPRNAMT, SSHPRNAMTTYPE, VotingSole, and Voting Share. I also included the name of the fund in the title of the file.

To test I used the following three Funds and CIK's:

Bill and Melinda Gates: 0001166559
Bridgewater Associates: 0001350694
AQR Capital Management: 0001167557
