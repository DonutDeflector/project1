# Project 1

Web Programming with Python and JavaScript

## Premise

Rainy day allows users to search up cities and towns in order to view the
weather and register an account in order to login for the purpose of submiting
check-ins.

## File Overview

### /

#### application.py

The back-end workhorse of the project. It is able to handle user login,
registration, and logout. It also displays the results of searches that query
the zipcode or name of a city. When a user navigates to a location, it will
display basic information about it and fetch the weather report and check-ins
for the location.

#### import.py

This script the `zips.csv` file by looping over each row (except the header) and
inserting it into the `locations` table. It prints the information of each row
while doing so for the sake of debugging.

### templates/

#### login_register.html

This file contains the login/registration card. The logic to decide weather
to display the login or registration version of the card is handled by Jinga.

#### search.html

The default search page of the website. It's a simple searhc form that is
vertically and horizontally centered.

#### search_results.html

When the user makes their first query, this page is displayed. The search bar is
moved to the top and results are displayed below it.

#### location_info.html

When the user clicks on a result on the search results page or navigates to a
location by manually inputting it into the URL bar, this page is displayed. The
back-end generates basic information about the location, fetches the weather
report, and displays check-ins. The submission of check-ins is disabled if
the user has already submitted a check-in or is not logged in.

#### 404.html

A custom 404 page. When a user navigates to a page that doesn't exist, it'll
give the user a humorous message and image while providing them with a button
that takes them back to the search page.

### templates/includes/

#### flash.html

A little component that allows me to display short messages to the user. This
handles things like displaying confirmation and error messages to the user.

#### navbar.html

The navigation bar component, which is included on nearly every page of the
site. On the right side of the navigation bar, the Logout button is displayed if
the user is logged in and the Login and Register buttons if the user is not
logged in. Along with these buttons, a link to the main search page is on the
right side. Snazzy branding occupies the left side of the navigation bar.

#### searchbar.html

The search bar component. This is included on the main search page as well as
on the search results page.

### templates/layouts/

#### default.html

The template that each of the pages shares. It imports all of the CSS, JS, and
fonts needed to make the site look nice in the `<head>`. Page titles are also
handled here.
