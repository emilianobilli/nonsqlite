# Flask and Object 

How to write a simple blog using Flask and ORM Object module.

*** No more schema and database ***

``` 
python flaskObject.py
```

Start a microblog in port 8000

## Define the class
```
class Entry(Object):
    _db_name = 'Blog.db' # If this class var is omitted use the default value Object.db
    def __init__(self):
        self.title = ''
        self.entry = ''
```

## Save Entry
```
e = Entry()
e.title = 'Some title'
e.text  = 'Some text'
e.save()
```
## Render Entry
```
def show_entries():
    return render_template('show_entries.html', entries=Entry.all())
```






