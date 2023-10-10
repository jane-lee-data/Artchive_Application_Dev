# Ar(t)chive : Discover artworks from National Gallery of Art Collection
## Video Demo:  https://youtu.be/QlbuRCEdclY

## **Introduction**

Ar(t)chive is a web application that helps exploring artworks in [National Gallery of Art (Washington DC)](https://www.nga.gov/). The goal of this project is to showcase the collection and help users discover their taste in art by allowing them to save artworks they like in the collection in their own web archive.
All data in the application is from the [Open Data at National Gallery](https://www.nga.gov/open-access-images/open-data.html).


## **How it works**

This is a flask application that connects to a sqlite3 database to search for artworks in the collection and allow users to save their favorites into their own database for later use. The website incorporates HTML [bootstrap5](https://getbootstrap.com/) styling.

Once users are registered and logged in, they can:
1. Search artworks in the collection by keywords;
2. View artwork information, including its title, attribution, date, dimensions, medium and classification.
3. Discover artworks in the collection through randomly selected artworks displayed everytime they enter 'Discover' page;
4. Build their own list of artworks of their taste by saving (and deleting) artworks found through search and 'discover'.


## **Implementation**

### **1. Data: project.db**
The database includes following tables:

***objects*** : All general information on each object(artwork) is recorded in this table from [NGA Open Data](https://github.com/NationalGalleryOfArt/opendata).

***images*** : All image information, including the iiifurl, is recorded in this table from NGA Open Data.

***objects_images*** : This is the main table queried for Search and Discover pages. Created by joining objects and images tables on objectid.

***mylist*** : This table records objects saved by each user. Queried using the session's user_id to display My List.

***users*** : User information is stored in this table upon registration. Unique id is assigned to each user.


### **2. Python Flask**
***app.py*** : This file includes all the main routes in the app, including:
- user info: register, log in, log out
- fetch data: search objects by user input, randomly select 20 objects to showcase
- user-saved list: save/delete objects from user's own database

***helpers.py***: This file includes login-required function (from CS50x's Problem Set 9) and apology function.

### **3. templates**
***index.html*** : This is the homepage of the app. For every access, a random image of artwork in the collection is displayed.
The button over image directs to search page if logged in, and if not, it directs to register page.

***layout.html*** : This gives the common style for all pages, including the navbar and the footer based on bootstrap5.

***explore.html*** : A search engine. Queries for artworks that include user's input in the title.

***searchresult.html*** : Displays the query result from explore.html in card-column view from bootstrap5. Each card includes image thumnail, links to its objectinfo page, full image, and a button to save the object in the user's 'My List'

***discover.html*** : Displays 20 randomly selected images of artworks from the collection. Users can hover over each image see the button linking to its objectinfo page.

***objectinfo.html*** : Queries general information of the artwork selected by the user. Displays its title, attribution, image, date, dimensions, medium and classification.

***mylist.html*** : Displays all artworks saved by the user. They can access the objectinfo page and the full image. Can also delete the object from the list.

***register.html*** : This file registers a user and saves the id and password hash and assigns user_id.

***login.html*** : This file logs a user in.

***logout.html*** : This file logs a user out.

***apology.html*** : This file returns an apology that one of user's inputs in register/log-in is not accepted.



### **4. static**
***styles.css*** : This file includes css codes for styling on top of bootstrap5. CSS for hoverable images are from [W3schools](https://www.w3schools.com/howto/howto_css_image_overlay.asp)



### **5. Misc.**
***opendata*** : This folder includes documentation and license of National Gallery of Art (NGA)'s Open Data. Full data can be found on [NGA Open Data Github](https://github.com/NationalGalleryOfArt/opendata)

***objects.csv, published_images.csv*** : Two csv files imported for project.db


## **Design Choices**

1. index.html:

    For every access, a randomly selected image of an object from the collection is displayed. This is to expose and showcase various artworks from the collection to the users.

2. seachresult.html and mylist.html:

    Implemented bootstrap5 card-column layout with custom style choices. Cards (including card-body and card-footer) are set into uniform heights for cleaner and orderly view. Each image is also set with width:100%, object-fit:contain in order to show the full artwork with its original ratio secured. **limit-chars** class is implemented since some long titles overflow.

3. discover.html:

    Only shows the image of the randomly selected artworks since the Discover page is intended to help users find their taste uninterrupted by any preconceived information or impression on the title or the attributed artist. If interested, the user can easily hover over the image and click a button to access the object information page.


## **Installation**
1. Run the command `pip install -r requirements.txt`
2. Run the command `flask run`















