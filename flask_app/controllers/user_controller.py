from flask import render_template, request, redirect, flash, session
from flask_app import app, bcrypt

from flask_app.models.user_model import User
from flask_app.models.part_model import Part

#? ==================== DASHBOARD ====================
#* render the dashboard html
@app.route('/dashboard')
def landing():
    return render_template('dashboard.html')

#? ==================== PERSONAL ITEM ====================
@app.route('/personal/<int:uid>')
def display_user_parts(uid):
    # prevent other users from accessing others' part list
    if 'uid' not in session or session['uid'] != uid:
        return redirect('/login')
    
    parts = Part.get_one_user({'id' : uid})
    user = User.get_by_id({'id' : uid})
    return render_template('personal_parts.html', user=user, parts=parts)

#? ==================== SELL ====================
@app.route('/sell')
def redirect_to_sell():
    if 'uid' not in session:
        return redirect('/login')
    return redirect('/sell/add') 

#? ==================== LOGOUT ====================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#? ==================== COOKIE ====================
@app.route('/cookie_toggled')
def toggle_cookie():
    if ('cookie' not in session) or (session['cookie'] == False):
        session['cookie'] = True
    return redirect('/dashboard')

@app.route('/reset_cookie')
def reset_cookie():
    if 'cookie' not in session:
        session['cookie'] = False;
    return redirect('/dashboard')


