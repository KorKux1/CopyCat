# Flask
from flask import Flask, render_template, redirect


# App
from app import create_app
from app.forms import  SearchForm

app = create_app()


@app.route('/', methods=['GET','POST'])
def index():
    """
    Return Types

    Returns:
        [type] -- [description]
    """
    search_form = SearchForm()

    context = {
        'search_form': search_form
    }

    if search_form.validate_on_submit():
        search = search_form.search.data
        print(search)
        return redirect('/')

    return render_template('index.html', **context)


@app.route('/mugs-scrapper')
def mugs_scrapper():
   return "Mugs Scrapper"


if __name__ == '__main__':
    app.run()
