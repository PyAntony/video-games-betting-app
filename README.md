# ROSHI BETS

Web app for video games betting using Django.


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
<kbd>![log-register]
(https://github.com/PyAntony/project3-PyAntony/blob/master/images/topmenu.png)
</kbd>
<br /><br /> 

**- Command Center:** 

Users have the option to sign up as gamers. Only gamers can create rooms and games. The Command Center is the area 
where gamers can interact with their assets and contact other gamers (this last feature needs to be implemented). 
Example: 

<br /><br />
<kbd>![log-register]
(https://github.com/PyAntony/project3-PyAntony/blob/master/images/command.png)
</kbd>
<br /><br />

**- Upcoming Games and Open Rooms:** 

Sections show top 10 upcoming games and chat rooms that can be sorted or searched by creator or room name.

<br /><br />
<kbd>![log-register]
(https://github.com/PyAntony/project3-PyAntony/blob/master/images/upcoming.png)
</kbd>
<br /><br />

**- Chat Rooms:** 

Rooms have a chat section and a streaming section. Gamers have buttons to create games and delete the room, 
whereas other users get the list of games created in that room and can bet. Example:

<br /><br />
<kbd>![log-register]
(https://github.com/PyAntony/project3-PyAntony/blob/master/images/chat.png)
</kbd>
<br /><br />

Chat implementation: AJAX is used to implement the chat section. In addition to the standard AJAX form there is a 
get request to the server that happens every second. Last 40 messages are rendered ONLY if new messages have been 
posted, else the query is not performed.  

**- Additional:**

Database can populated (seeded) with fake objects by running the file roshi_bets/seeder.py. Number of objects
to insert can be changed with the global variables.

















**- Placing an Order:** 

Users can update the order quantities, select toppings and extras before placing the order. 
Subtotals and Total prices are displayed:

<br /><br />
<kbd>![cart](https://github.com/PyAntony/project3-PyAntony/blob/master/images/cart.png)</kbd>
<br /><br />

**- Viewing Orders:** 

Orders are marked as 'sold' (in status field) after the user clicks the 'Place Order' 
button. They can be found in the admin UI.

**- Personal touch:** 

Ability to download sales as a CSV file using a GET request to the endpoint "csv/<date_time>". Users 
can specify the required time frame using the <date_time> parameter (Instructions in the function docstring). 
Functions to inspect and parse the string parameter are found in the "helpers.py" file. Only site 
administrators can use the endpoint, otherwise a forbidden error is thrown. Entire view/function here:

```Python
@login_required
def csv_view(request, date_time):
    '''
    URL format:
    ----------
        'csv/start:<date_time>*until:<date_time>'
    You can use 'start' (all sales since) or 'until' (all sales until) alone.

    date_time format:
        'Y-m-d*H:M*S' or 'Y-m-d'

    Examples:
        - csv/start:2019-04-03*02:30:00*until:2019-04-06*05:30:00
        - csv/start:2019-02-28
        - csv/until:2019-01-10*12:50:00

    Return:
    ------
        CSV file with sales requested.
    '''
    # endpoint can only be used by site administrators
    if not request.user.is_staff:
        return HttpResponseForbidden()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'

    dt_parameters = date_time_parser(date_time)

    if dt_parameters == 'error':
        msg = 'Unable to parse <date-time>. Review your request.'
        return render(request, "orders/csv.html", {'msg': msg})

    sales = filter_by_time(Order, dt_parameters)

    if not sales:
        msg = 'No sales found for the requested date-time period.'
        return render(request, "orders/csv.html", {'msg': msg})

    writer = csv.writer(response)
    writer.writerow(get_sale_data(sales[0], 'fields'))

    for sale in sales:
        writer.writerow(get_sale_data(sale))

    return response
```

