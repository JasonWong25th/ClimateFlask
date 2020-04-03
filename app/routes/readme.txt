The routes directory contains the files that generate the content that is deisplayed on the pages.  This 
is different from the Templates directory which contains the files which actually control how the page looks.
A route is a function that catches what the user put in to the browser and then retrieves that data and sends
it to the template. Routes are Flask's magic.  Each route has a decorator which, if the route matches what
the user requests then that code for that route is run.

See the feedback.py file for detailed description of how this works.