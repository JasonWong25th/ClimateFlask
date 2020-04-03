templates are the files that create the html pages that the user sees in their browser. These files are are not 
static meaning they can be different every time a user sees them.  They are not static, they are dynamic.  That 
is achieved via the magic of Jinja.  Jinja is what is called a templating language. Jinja lets you run python 
code inside of html.  The easiest and most common thing is to simply display a variable.  For example, if you 
have a simple route like this.

@app.route('/user/<name>')
def userpage(name):
    hobbies = ['fishing','knitting','other stuff']
    return render_template('userpage.html', name=name, hobbies=hobbies)

Then you could have a userpage.html template that was something like:

...
<body>
    {{ name }}
    {% for hobby in hobbies %}
        {{ hobby }}
    {% endfor %}
</body>
...

The double curly brackets are Jinja's way of displaying a variable.
The {% python %} notation is Jinja's way of running some limited python
Check Jinja's documentation for more 