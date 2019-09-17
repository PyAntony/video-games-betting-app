# ROSHI BETS

Mobile responsive application for video games betting using Django (Final Project: CSCI E-33A).


## Usage

    - Clone repository & navigate to repository directory.
    - Run "pip3 install -r requirements.txt".
    - Run "python manage.py migrate && python manage.py runserver".


### Requirements and Description

The purpose of this application is to get together gamers and followers (gamblers). In contrast with other
apps that target the big video game industry events and professional gamers and fans, this application targets amateur 
gamers that would like to earn some money while playing their favorite video games at home and people that would
like to bet on these games while live streamed. Application can be used for small local events; for example, to spark 
some real competitiveness in a friday night video game tournament with friends.  

Note: not all visible features have been implemented, only the necessary to demo the main functionality.     

**- Top Menu:** 

Top menu includes links to navigate to the different sections in the same html document and buttons which display 
forms to sign up and login. If the user is found to be authenticated in the request, buttons change to display 
user account and logout. Example:

<br /><br />
<kbd>![log-register](https://github.com/PyAntony/final-project-PyAntony/blob/master/images/topmenu.png)</kbd>
<br /> <br />

**- Command Center:** 

Users have the option to sign up as gamers. Only gamers can create rooms and games. The Command Center is the area 
where gamers can interact with their assets and contact other gamers (this last feature needs to be implemented). 
Example: 

<br /><br />
<kbd>![log-register](https://github.com/PyAntony/final-project-PyAntony/blob/master/images/command.png)</kbd>
<br /><br />

**- Upcoming Games and Open Rooms:** 

Sections show top 10 upcoming games and chat rooms that can be sorted or searched by creator or room name.

<br /><br />
<kbd>![log-register](https://github.com/PyAntony/final-project-PyAntony/blob/master/images/upcoming.png)</kbd>
<br /><br />

**- Chat Rooms:** 

Rooms have a chat section and a streaming section. Gamers have buttons to create games and delete the room, 
whereas other users get the list of games created in that room and can bet. Example:

<br /><br />
<kbd>![log-register](https://github.com/PyAntony/final-project-PyAntony/blob/master/images/chat.png)</kbd>
<br /><br />

Chat implementation: AJAX is used to implement the chat section. In addition to the standard AJAX form there is a 
get request to the server that happens every second. Last 40 messages are rendered ONLY if new messages have been 
posted, else the query is not performed.  

**- Additional:**

Database can be populated (seeded) with fake objects by running the file roshi_bets/seeder.py. Number of objects
to insert can be changed with the global variables.

