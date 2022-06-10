from flask import Flask, render_template_string, request
from wtforms import Form, SelectField

application = app = Flask('wsgi')

class LanguageForm(Form):
    language = SelectField(u'Opções', choices=['Sala Precisa', 'Sala de Jogos', 'Sala de Música'])

template_form = """
{% block content %}
<h1>Selecione uma sala</h1>

<form method="POST" action="/">
    <div>{{ form.language.label }} {{ form.language(rows=3, multiple=True) }}</div>
    <button type="submit" class="btn">Submit</button>    
</form>
{% endblock %}

"""

completed_template = """
{% block content %}
<h1>Language Selected</h1>

<div>{{ language }}</div>

{% endblock %}

"""

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LanguageForm(request.form)

    if request.method == 'POST' and form.validate():
        print ("POST request and form is valid")
        language =  request.form['language']
        print ("languages in wsgi.py: %s" % request.form['language'])
        return render_template_string(completed_template, language=language)

    else:

        return render_template_string(template_form, form=form)

if __name__ == '__main__':
    app.run(debug=True)