# Flask and Object 

How to write a simple blog using Flask and ORM Object module.

*** No more schema and database ***

``` 
python flaskObject.py
```

Start a microblog in port 8000

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






