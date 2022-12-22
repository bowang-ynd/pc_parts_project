import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, flash, session, url_for
from flask_app import app, ALLOWED_EXTENSIONS
from flask_app.models.user_model import User
from flask_app.models.part_model import Part


# function cited from flask documentation about uploading and storing file
# link: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#? ==================== DISPLAY PARTS ====================
@app.route('/dashboard/cpu')
def display_cpu():
    cpus = Part.display_cpus()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=cpus)

@app.route('/dashboard/motherboard')
def display_motherboard():
    motherboards = Part.display_motherboards()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=motherboards)

@app.route('/dashboard/gpu')
def display_gpu():
    gpus = Part.display_gpus()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=gpus)

@app.route('/dashboard/memory')
def display_memory():
    memories = Part.display_memories()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=memories)

@app.route('/dashboard/storage')
def display_storage():
    storages = Part.display_storages()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=storages)

@app.route('/dashboard/cooler')
def display_cooler():
    coolers = Part.display_coolers()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=coolers)

@app.route('/dashboard/power')
def display_power():
    powers = Part.display_powers()
    if 'uid' in session:
        last_name = User.get_by_id({'id' : session['uid']}).last_name
    else:
        last_name = 'Guest'
    return render_template('part_by_category.html', last_name=last_name, parts=powers)

#? ==================== SELL ====================
@app.route('/sell/add')
def add_sell():
    if 'uid' not in session:
        return redirect('/login')
    return render_template('sell.html')

@app.route('/sell/process', methods=['POST'])
def process_sell():
    if 'uid' not in session:
        return redirect('/login')

    # validate the necessary input from user
    is_valid = Part.validate(request.form)

    # check if request has file part
    if 'file' not in request.files:
        is_valid = False
        return redirect('/sell/add')
    file = request.files['file']

    # then checks if user selected a file for upload
    if file.filename == '':
        flash('Please upload an image of your part!', 'component')
        is_valid = False
    elif not allowed_file(file.filename):
        flash('Please choose your image in jpg, jpeg, or png!', 'component')
        is_valdid = False
    
    if not is_valid:
        return redirect('/sell/add')

    # if user has uploaded a file and the file is in correct type
    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        print(file_name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    
    data = {
        **request.form,
        'img' : file_name,
        'owner_id' : session['uid']
    }
    # add the part to db
    Part.create(data)

    id = session['uid']

    return redirect(f'/personal/{id}')

#? ==================== UPDATE ====================
@app.route('/edit/<int:part_id>')
def edit(part_id):
    if 'uid' not in session:
        return redirect('/login')

    return render_template('edit_part.html', part_id=part_id)

@app.route('/sell/edit', methods=['POST'])
def edit_process():
    if 'uid' not in session:
        return redirect('/login')

    part_id = request.form['part_id']

    # validate the necessary input from user
    is_valid = Part.validate(request.form)

    # check if request has file part
    if 'file' not in request.files:
        is_valid = False
        return redirect(f'/edit/{part_id}')
    file = request.files['file']

    # then checks if user selected a file for upload
    if file.filename == '':
        flash('Please upload an image of your part!', 'component')
        is_valid = False
    elif not allowed_file(file.filename):
        flash('Please choose your image in jpg, jpeg, or png!', 'component')
        is_valdid = False
    
    if not is_valid:
        return redirect(f'/edit/{part_id}')

    # if user has uploaded a file and the file is in correct type
    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        print(file_name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    
    data = {
        **request.form,
        'id' : part_id,
        'img' : file_name,
        'owner_id' : session['uid']
    }
    # add the part to db
    Part.update_one(data)

    id = session['uid']
    return redirect(f'/personal/{id}')

#? ==================== DELETE ====================
@app.route('/delete/<int:part_id>')
def delete(part_id):
    if 'uid' not in session:
        return redirect('/login')

    Part.delete_one({'id' : part_id})

    id = session['uid']
    return redirect(f'/personal/{id}')