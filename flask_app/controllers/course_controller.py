from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.course import Course
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user_id = session['user_id']
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    if 'refresh' in session:
        session['refresh'] += 1
    else:
        session['refresh'] = 1
    return render_template('dashboard.html', user=user, course=Course.get_all())

@app.route('/courses/new')
def create_course():
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('new_form.html')

@app.route('/course/new/process', methods=['POST'])
def process_course():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Course.validate_course(request.form):
        return redirect('/courses/new')

    data = {
        'user_id': session['user_id'],
        'score': request.form['score'],
        'golf_course': request.form['golf_course'],
        'notes': request.form['notes'],
    }
    Course.save(data)
    return redirect('/dashboard')

@app.route('/courses/<int:id>')
def view_course(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('view_form.html', course=Course.get_by_id({'id': id}))


@app.route('/courses/derby')
def all_course():
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('course.html',course=Course.get_all())

@app.route('/course/edit/<int:id>')
def edit_course(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('edit.html',course=Course.get_by_id({'id': id}))

@app.route('/course/edit/process/<int:id>', methods=['POST'])
def process_edit_course(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Course.validate_course(request.form):
        return redirect(f'/course/edit/{id}')

    data = {
        'id': id,
        'score': request.form['score'],
        'golf_course': request.form['golf_course'],
        'notes': request.form['notes'],
    }
    Course.update(data)
    return redirect('/dashboard')

@app.route('/courses/destroy/<int:id>')
def destroy_course(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    Course.destroy({'id':id})
    return redirect('/dashboard')
