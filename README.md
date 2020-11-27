### A comparative approach on chilling effect, from Wikipedia to Google Trend


#### Abstract

In his paper *Chilling effects: Online surveillance and Wikipedia use*, Jonathon W. Penney exhibits the existence of a chilling effect generated by the fear of online surveillance due to the revelation done by Snowden in 2013. Indeed, he has shown that Wikipedia users’ activity on terrorism-related articles has been decreasing after the Snowden revelations of May 2013.  

In this study, we would like to confirm the results obtained on a larger dataset. Wikipedia is a good tool to have a glance at the users’ searches, but it gathers a too small sample of the whole internet searches in comparison with the global activity of the Internet. This is why our choice fell on Google Trends, as the Google search engine vastly outnumbers Wikipedia article views and might be a better portrayal of the internet user population.

#### Research Questions

Using Google Trends, do we still observe a chilling effect after the Snowden revelations?
Do the results observed with Google Trends match those using Wikipedia? If not, how could we explain the differences? If yes, does the chilling effect last in the longer term (from 2015 when the original paper stops to 2020)?

#### Proposed dataset

As our dataset doesn’t exist, we plan to create our own dataset using unofficial APIs that access the official Google Trends platform.
We found these 2 interesting libraries that fill our requirements:
> * [Pytrends](https://pypi.org/project/pytrends/), a python library.  
> * [Google trends API](https://www.npmjs.com/package/google-trends-api), a javascript library.

As we aim to work in Python, we will focus first on the Pytrends library. This library allows us to reproduce the same queries as if we were on Google Trends.

#### Methods

The project aims to create a dataframe based on Google search data.  
For that, we will first scrape the data we need from the proposed dataset and put them in a unique dataframe. Note that :

1. Google Trend does not allow to retrieve more than five keywords,
2. it does not give the absolute number of searches per keyword, but only relative searches in comparison with the other keywords retrieved.

We intend to tackle both issues with the following procedure: we will retrieve the subjects we are interested in, those related to terrorism similarly to what J.W. Penney used for his research with Wikipedia, in groups of four with each time the same reference subject (e.g. Youtube) in order to have the same relative relation between all subjects.

After that, we will apply a similar analysis as the one performed in the original paper to see if we can observe a chilling effect on Google Trends.


#### Proposed timeline

Here is an overview of the timeline we plan to follow:
  				
![alt text](https://github.com/epfl-ada/ada-2020-project-milestone-p3-p3_pada1/raw/main/timeline.jpg "Timeline")


#### Organization within the team

We will meet regularly to work together on the project and split the work equally according to our progress (using Agile method).

The first task we will work on is to extract the data to create our dataset according to what we described in the method part.

#### Questions for TAs

> - As google trends platform is only giving a relative number of views to the maximum number of views between the different subjects, do you have any other suggestion than the one described in the method section to get an idea of how to estimate the absolute number of views of each subject?
> - Is this read-me the final form of our project or can we add or change elements after more research (as long as we are not deviating too strongly from the original ideas)?
