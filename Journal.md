                                    POST CONSTRUCTION MODEL LOG


# Tags:[LSTM,TCN,SCRAPER,EXTRACT,BILSTM,API,REACT,BERT,CLEANUP]
__________________________


# Default Model [SCRAPER]

The default model used a beautiful soup model, that initially looked for keywords in queries ,as in searched the links itself for the certain keywords , which didnt work, then switched to google rss to get certain articles or links but since google rss only showed a limited amount of articles we switched from that as well

___________________________

# Iteration 1 [SCRAPER]

We swtiched the scraper to instead of checking google rss or we accessed certain economic sites link and searched for the keywords within these site links , which narrowed down the articles it has to parse through and get more results 

__________________________

# Iteration 2 [SCRAPER]

Beautiful soup only returned the static pages urls and links ,so the links it could acquire were limited since most sites nowadays used script for these links , to access these dynamic pages , we switched from beautiful soup to selenium which can scroll or move through these sites and access all the links present 

__________________________

# Iteration 3 [SCRAPER]

Fully utilizing Selenium now , instead of checking individual tags for certain keywords or links to articles , since BERT is a model that benefits from having "junk" fed to it , we instead removed all select loops and just grabbed every href link on all the pages , this returned around 1200 articles ,from economic times and livemint, moneycontrol had an antibot software "akami" that prevented us from scraping it , and since overcoming that obstacle would question the legality and ethics , i opted not to 

__________________________

# Iteration 4 [SCRAPER]

Since BERT requires a large volume of data , i decided to add more sites to scrape for the model , initially i decided to do this manually ,just adding links to url and then building the for loop myself , i realised it would take alot of time , so instead decided to automate the process ,uttilizing two arrays , one for the website links and one for the saved articles, i also added a bert scroller to this t access more links that might not have been previously accessible just through loading javascript using selenium

__________________________

# Iteration 5 [SCRAPER]

Added a blacklist array which indicates the sites to not scrape, this was done so that bert does not scrape or access junk sites , also added alot of try exception blocks so that program dosent crash when a single site dosent load

This iteration worked , added a few exception blocks here and there, added functions to check browser health , and make the system more redundant

__________________________

# Iteration 6 [SCRAPER]

So modularized the code and split it into smaller chunks

link_extract contains the main functions which extracts links from the sites 

robot contains the function that parses through robot.txt of sites

utils contains the supporting function that are not integral but are general purpose 

Scrape_run contains the main run program

___________________________

# Iteration 7 [SCRAPER]

So changed the data loading sequence , since if frontend have to manipulate the filters and sites then they have to be present outside of a python program,so created a new json file that contains the filters and sites , it was two initially but that could cause issues in frontend so made it one , added new functions to scraper to load these json files as needed 
___________________________

___________________________

# Default Model [EXTRACTOR]

The default model followed a similar architecture to that of the scraper since they both had a similar function , but this one used newpapery3k to parse through the articles whose links and titles were collected and stored in a json file , the loader is built to extract all the content in main articles and store it in a seperate folder as txt files with their respective title names 

__________________________

# Iteration 1 [EXTRACTOR]

Since newspapery3k class article was constantly reloaded on every scroll but the contents were not stored to a file or array,we lost all the data except the content that was present on the html doc on the last iteration or the last scroll , to fix this we implemented a string that is constantly concatenated on every loop of the scroll ,as in article writes its content into this string before new scroll is executed 

__________________________

# Iteration 2 [EXTRACTOR]

Sinces articles load the same url constantly even after scrolling the page that is loaded is the initial page ,so scrolling becomes irrelevant ,to prevent this we needed to store the links in an array and after every scroll append the new link to this list and have the article url be called afterwards , so that the url can be skipped and article skips all url that came beforehand ,which are the ones present in array 

Scroll-->Click-->Article loaded-->Content parsed-->content stored-->Scroll again
                                |
                                |
                                |
Scroll-->Click-->Url Stored-->Url check runs-->Article loads-->Content parsed-->Content stored-->Scroll again

___________________________

# Iteartion 3 [EXTRACTOR]

Build an advanced get function which creats a link with the site and receives logs from there , thus allowing more advanced debugging, added debugging into every single layer of the program and found the core issues which was a pathing issue , where new spaces caused error in the windows file naming system , updated the sanitizer of filenames  

___________________________

# Iteration 4 [EXTRACTOR]

Ran into issues where some sites where parsed properly and some werent ,this was caused by the issue that most sites dont use proper tags and instead just use " " and strong tags inside html for paragraphs , which breaks most libraries used for parsing , created a seperate function for dealing with such raw html tags by utilizing xpath 

___________________________

# Iteration 5 [EXTRACTOR]

Abandoned the xpath function and instead decided to use a new library playwright , which is capable of rendering and parsing even the most js heavy and complicated and with a few tweaks , it was capable of parsing through the most broken html sites , but since it was somewhat slow it is used alongside selenium-newspaper,as in certain links are fed into playwright and rest are fed into newspaper
___________________________

# Iteration 6 [EXTRACTOR]

So playwright began working for me , but certain articles became stuck on parsing for extremely long times ,so added a timeout function for playwright , also split everything into modules and its own seperate programs, there was a tiny issue with the loader where if the link of the site wasnt explicitly named then it would automatically go to selenium-newspaper which could cause issues , so instead of checking site name at loader , every link is sent to selenium , and if it fails then its sent to playwright

                                            Sucess
            LOADER---->SELENIUM-NEWSPAPER------------>FILE SAVED
                            |
                            | Fail
                            |
                        PLAYWRIGHT----->FILE SAVED
___________________________

# Iteration 7 [EXTRACTOR]

So i modularized the code , and split it into smaller chunks 

Utils file containing general functions that are not integral to code and act as supporting code

Selenium_newspaper contains the newspaper-selenium function that is used to load the content that can be extracted from non js heavy sites 

Playwright_extract contains the code to extract content from JS-heavy sites  

Content_Extract contains the main function that goes through site after site

Extract_Run Contains the main run program

___________________________
___________________________

# Default Model [API]

Created new json files where one stores goodlist and other stores websites , this was done so that api can directly interact with these lists which were previously inside .py files which could not be accessed 

Created save and fetch function for both of these json files so that they can be updated and viewed

Initially the api program was its own seperate folder but due to access issues for react it was moved inside the frontend

___________________________________

# Iteration 1 [API]

Created ts api that interacts with the frontend , since frontend cannot directly with python files had to built it using typescript , it contains fetch functions for viewing the lists and websites that were added , and save function for changing the lists and websites from the frontend itself , these were done through async functions to increase reliability

___________________________________

# Iteration 2 [API]

Advanced the apis especially typescript to receive inputs from the browser, changed the funcionalities a bit , now instead of adding and viewing only , we instead can now add filters and sites view them as well as remove any ones , these were all done in async , ran into a few glitches here and there , so added logging to the entire flask api 
___________________________________

# Iteration 3 [API]

Modularized the code ,split the flask api into two addition api and removal api and the same was also done to typescript apis , build a new run program for flask to avoid manually running the individual flask files ,but ran into some issues here due to the pathing issues 

___________________________________

# Iteration 4 [API]

The pathing issues were caused by parent directory being executing files directory , solved this by setting a python path and then running program ,also added two new api calls one to call scraper and one to call extractor each executing their respective python files 

___________________________________
___________________________________

# Default Model [REACT]

So changed the components section as in list editor and site editor to be aligned with the app program ,set up interfaces on both of them to properly define the parameters in functions , in App created an interface to properly define the data import coming in from api , and changed the function of all keyword (site,list,setsites,setlist) from  being a simple usestate to being a string

___________________________________


# Iteration 1 [REACT]

Decidied to stop development of gui until the api functionalities were all working , decided to develop a barebones structure with each api call having a button and sharing the same textfield , gui will be further developed once all the api calls are properly working

___________________________________

# Iteration 2 [REACT]

So since all the apis calls were working properly decided to move forward with react ui and build a minimal and clean ui that is enough for demo representation , further additions will be made once the full system is complete and mostly just to add polish

__________________________________

# Iteration 3 [REACT]

So decided to create a presentable ui in the event of any demos , instead of just using react-vite we also added tailwind and shadcn to increase the aesthetics of it , especially since shadcn provides so many boilerplates for many functions , the api calls functionality didnt change though , but the input validation became more complex due to the inputs being validated outside of app and inside inputs present in components

__________________________________

# Default Model [CLEANER]

So the extracted txt files had junk present inside of it that was not necessary for a high quality dataset so that was cleaned using a combination of methods , regex, clean text and spacy were used initially to acquire high quality data and these were pipelined

regex --> clean text --> spacy

__________________________________

# Iteration 1 [CLEANER]

So there were still some issues with the txt files in that were some junk files that had very short words present in the nav bar that were accepted and alot of files had continue reading at the , these were removed using a 2 custom heuristics
__________________________________

# Default Model [PARAPHRASE]

Decided to use a paraphrasing model instead of a backtranslation one , since backtranslation didnt introduce as much changes as needed , so the model used was pegasus which has a high level of paraphrasing capability ,so the initial stage was breaking the text down into encodings or smaller chunks , these were then tokenized and passed into the model to generate paraphrased content 

_________________________________

# Iteration 1 [PARAPHRASE]

So a slight issue occured with the amount of nesting present , since we first have to access directory , then the files , and then acquire the chunks , there is a 3 tier hierarchy present , which made every step difficult , initial approach to this was list datastructure ,but an issue occured where we needed the filename alongside the chunks , which made list have a 3 tier structure and a matrix in the 2nd tier due to addition of files , which made it more complex , to solve this dictionary was used 

_________________________________

# Iteration 2 [PARAPHRASE]

Since one text file had multiple chunks inside of it and had to be stored as one single file ,storing them became an issue due to no real identification properties being present in the lowest tier, so we had to go 2nd tier where filenames were present , and enumerate them accordingly with filenames being the main condition used to ensure that duplication or mismatching did not occur

_________________________________

# Default Model [SBERT]

Decided to implement an sbert to compare semantic values between the paraphrased and original content , to ensure that lower quality content isnt passed through to the final datasets ,this was achieved by deleting paraphrased files with very high semantci scores(0.9>) and very low (<0.3) , to do this we reused the text encodings and acquiring functions previously developed and reused them in this , to ensure that no difference in parameters occurs 

_________________________________

# Iteration 1 [SBERT]

So again the hierarchy issues present in paraphrasing presented itself , but this time it was worse since , we had to ensure hierarchy between two directories , this was handled by acquiring both at the same time , and then zipping them together to ensure synchronization , the resulting encodings semantic scores were added alongside their filename to a dictionary 

________________________________

# Iteration 2 [SBERT]

So a slight issue occured in that multiple embeddings for a file name were present , since we check the embedded values itself and there are many embeddings present for a file depending on file size if even one embedding had differing semantic scores then the entire file was deleted , so instead of appending semantic scores directly into final dictionary , we introduced a placeholder one to hold semantic scores , then these semantic scores were averaged based on filenames , and that was used to check semantic value

________________________________

# Iteration 3 [SBERT]

Since paraphrased content was usually shorter than original content , final embeddings had alot of empty spaces in paraphrased unlike originals , which caused a slight issue in actual semantic value of entire file ,due to these last chunks having very low semantic score , so these were removed with a custom heuristic

________________________________

# Iteration 5 [API]

Introduced a new api call to run the entire synthetic data generation pipeline , similar to the scraper functions , but this has lazy loading due to the models being heavy and not necessary in other uses except for synthetic data generation , 


