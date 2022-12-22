from flask import render_template, redirect, session
from flask_app import app 
from flask_app.models.user_model import User
from flask_app.models.part_model import Part
from flask_app.models.cart_model import Cart

#? ==================== BUY ====================
@app.route('/cart/add/<int:part_id>')
def add_to_cart(part_id):
    if 'uid' not in session:
        return redirect('/login')
    
    data = {
        'owner_id' : session['uid'],
        'part_id' : part_id
    }

    Cart.create(data)

    return redirect('/cart')

@app.route('/cart')
def visit_cart():
    if 'uid' not in session:
        return redirect('/login')

    parts_in_cart = Cart.get_one_user({'id' : session['uid']})
    # calculate the total price
    total = 0;
    for part in parts_in_cart:
        total += part.price
    user = User.get_by_id({'id' : session['uid']})
    return render_template('cart.html', user=user, parts=parts_in_cart, total=total)

#? ==================== DELETE ====================
@app.route('/cart/delete/<int:part_id>')
def delete_from_cart(part_id):
    if 'uid' not in session:
        return redirect('/login')
    
    data = {
        'owner_id' : session['uid'],
        'part_id' : part_id
    }

    Cart.delete_one_part(data)

    return redirect('/cart')

@app.route('/cart/place_order')
def place_order():
    if 'uid' not in session:
        return redirect('/login')
    
    parts_in_cart = Cart.get_one_user({'id' : session['uid']})
    for part in parts_in_cart:
        data = {
            'owner_id' : session['uid'],
            'part_id' : part.id
        }
        Cart.delete_one_part(data)
        Part.delete_one({'id' : part.id})
    return render_template('after_purchase.html')
