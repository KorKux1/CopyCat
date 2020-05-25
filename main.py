# Flask
from flask import Flask, render_template, redirect


# App
from app import create_app
from app.forms import  SearchForm

app = create_app()


@app.route('/', methods=['GET','POST'])
def index():
    """
    This function controls the flow of requests to the index 

    Returns:
        [redirect] -- [Redirects to page when form is filled correctly]
        [render_template] -- [It is in charge of rendering the index passing the context parameters]
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
