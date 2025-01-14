from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import close_connection, init_db, login_gebruiker, insert_gebruiker, insert_contact, get_favorieten, insert_favoriet, delete_favoriet, get_activiteit, get_thema

app = Flask(__name__)
app.secret_key = 'jouw_geheime_sleutel'

@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

@app.route('/')
def index():
    return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/rust')
def rust():
    return render_template('rust.html')

@app.route('/balans')
def balans():
    return render_template('balans.html')

@app.route('/groei')
def groei():
    return render_template('groei.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        naam = request.form['naam']
        email = request.form['email']
        thema = request.form['thema']
        bericht = request.form['bericht']

        if insert_contact(naam, email, thema, bericht):
            flash('Je bericht is verzonden!', 'success')
        else:
            flash('Er is iets fout gegaan tijdens het verzenden, probeer het opnieuw.', 'danger')
    return render_template('contact.html')

@app.route('/aanmelden', methods=['GET', 'POST'])
def aanmelden():
    if request.method == 'POST':
        gebruikersnaam = request.form['gebruikersnaam']
        email = request.form['email']
        wachtwoord = request.form['wachtwoord']

        try:
            insert_gebruiker(gebruikersnaam, email, generate_password_hash(wachtwoord))
            gebruiker = login_gebruiker(email)

            if gebruiker is not None:
                session['Gebruiker_ID'] = gebruiker[0]
                session['Gebruikersnaam'] = gebruiker[1]
                session['Email'] = gebruiker[2]
                return redirect(url_for('homepage'))
            else:
                flash('Er is iets fout gegaan tijdens het aanmelden, is er al een account met die gebruikersnaam of email?', 'danger')
        except:
            flash('Er is iets fout gegaan tijdens het aanmelden, is er al een account met die gebruikersnaam of email?', 'danger')
    return render_template('aanmelden.html')

@app.route('/inloggen', methods=['GET', 'POST'])
def inloggen():
    if request.method == 'POST':
        email = request.form['email']
        wachtwoord = request.form['wachtwoord']

        gebruiker = login_gebruiker(email)
        if gebruiker is not None and check_password_hash(gebruiker[3], wachtwoord):
            session['Gebruiker_ID'] = gebruiker[0]
            session['Gebruikersnaam'] = gebruiker[1]
            session['Email'] = gebruiker[2]

            add_favorieten(gebruiker[0])

            return redirect(url_for('homepage'))
        else:
            flash('Onjuiste gebruikersnaam of wachtwoord', 'danger')
    return render_template('inloggen.html')

@app.route('/uitloggen')
def logout():
    session.pop('Gebruiker_ID', None)
    session.pop('Gebruikersnaam', None)
    session.pop('Email', None)
    session.pop('favorieten', None)
    return redirect(url_for('homepage'))

def add_favorieten(gebruiker_id):
    if 'favorieten' not in session:
        session['favorieten'] = []
    for favoriet in get_favorieten(gebruiker_id):
        thema = get_thema(favoriet['Activiteit_ID'])
        session['favorieten'].append(thema[1])

@app.route('/favoriet_toevoegen/<string:thema>', methods=['POST'])
def favoriet_toevoegen(thema):
    activiteit = get_activiteit(thema)
    if activiteit is None:
        redirect(url_for('homepage'))
    activiteit_id = activiteit[0]
    
    gebruiker_id = session.get('Gebruiker_ID')
    delete = False
    for favoriet in get_favorieten(gebruiker_id):
        if favoriet['Activiteit_ID'] is activiteit_id:
            delete = True
    
    if delete:
        delete_favoriet(gebruiker_id, thema)
    else:
        insert_favoriet(gebruiker_id, thema)

    if 'favorieten' not in session:
        session['favorieten'] = []
    
    if thema not in session['favorieten']:
        session['favorieten'].append(thema)
    else:
        session['favorieten'].remove(thema)
    session.modified = True  # Zodat de sessie wordt bijgewerkt

    return redirect(url_for(thema))

@app.route('/favorieten')
def favorieten():
    if 'Gebruiker_ID' not in session or 'favorieten' not in session:
        redirect(url_for('inloggen'))
    themas = []
    for favoriet in get_favorieten(session.get('Gebruiker_ID')):
        themas += [get_thema(favoriet['Activiteit_ID'])]
    return render_template('favorieten.html', themas=themas)

@app.route('/go_to_favoriet/<string:thema>')
def go_to_favoriet(thema):
    return redirect(url_for(thema))

@app.route('/rust/oefening/dankbaarheid')
def rust_dankbaarheid():
    return render_template('rust_dankbaarheid.html')

@app.route('/rust/oefening/meditatie')
def rust_mediteren():
    return render_template('rust_mediteren.html')

@app.route('/rust/oefening/ademhaling')
def rust_ademhaling():
    return render_template('rust_ademhaling.html')

@app.route('/rust/oefening/hierennu')
def rust_hier_en_nu():
    return render_template('rust_hier_en_nu.html')

@app.route('/rust/oefening/journal')
def rust_journal():
    return render_template('rust_journal.html')

@app.route('/balans/oefening/hobby')
def balans_hobby():
    return render_template('balans_hobby.html')

@app.route('/balans/oefening/grenzen')
def balans_grenzen():
    return render_template('balans_grenzen.html')

@app.route('/balans/oefening/planning')
def balans_planning():
    return render_template('balans_planning.html')

@app.route('/balans/oefening/ontspannen')
def balans_spieren_ontspannen():
    return render_template('balans_spieren_ontspannen.html')

@app.route('/balans/oefening/levensdomein')
def balans_levensdomein():
    return render_template('balans_levensdomein.html')

@app.route('/groei/oefening/uitdagingen')
def groei_uitdagingen_lijst():
    return render_template('groei_uitdagingen_lijst.html')

@app.route('/groei/oefening/evalueren')
def groei_moeilijke_momenten_evalueren():
    return render_template('groei_moeilijke_momenten_evalueren.html')

@app.route('/groei/oefening/bereidheid')
def groei_bereidheid():
    return render_template('groei_bereidheid.html')

@app.route('/groei/oefening/leerjezelfkennen')
def groei_leer_jezelf_beter_kennen():
    return render_template('groei_leer_jezelf_beter_kennen.html')

@app.route('/groei/oefening/zelfbewustzijn')
def groei_ontwikkel_je_zelfbewust_zijn():
    return render_template('groei_ontwikkel_je_zelfbewust_zijn.html')


if __name__ == "__main__":
    with app.app_context():
        init_db()  
    app.run(debug=True)
