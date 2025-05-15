import io
import os
from datetime import datetime
from flask import (
    render_template, request, redirect, url_for, flash, 
    jsonify, send_file, abort, session
)
from app import app, db
from models import TestTemplate, TestVersion, QuestionTemplate, Question
from forms import TestTemplateForm, AnswerKeyAccessForm
from utils.pdf_generator import generate_test_pdf, generate_batch_test_pdf
from utils.qr_generator import generate_qr_code
from utils.math_generator import generate_question_templates, generate_test_version_questions

# Add now function for templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def index():
    """Home page with information about the application."""
    return render_template('index.html')

@app.route('/create-test', methods=['GET', 'POST'])
def create_test():
    """Create a new math test template and generate versions."""
    form = TestTemplateForm()
    
    if form.validate_on_submit():
        # Create a new test template
        test_template = TestTemplate()
        test_template.title = form.title.data
        test_template.description = form.description.data
        test_template.difficulty = form.difficulty.data
        # Handle the case where topics might be None
        if form.topics.data:
            test_template.topics = ','.join(form.topics.data)
        else:
            test_template.topics = ''
        test_template.num_questions = form.num_questions.data
        test_template.num_versions = form.num_versions.data
        
        # Set the password for answer key access
        test_template.set_password(form.password.data)
        
        # Save the test template
        db.session.add(test_template)
        db.session.flush()  # Flush to get template ID
        
        # Generate question templates
        question_template_data = generate_question_templates(
            topics=form.topics.data,
            difficulty=form.difficulty.data,
            num_questions=form.num_questions.data
        )
        
        # Create question templates
        for i, (topic, difficulty, order) in enumerate(question_template_data):
            question_template = QuestionTemplate()
            question_template.test_template_id = test_template.id
            question_template.question_type = topic
            question_template.difficulty = difficulty
            question_template.order = order
            db.session.add(question_template)
        
        # Commit to save question templates
        db.session.commit()
        
        # Reload question templates from the database to ensure they have IDs
        question_templates = QuestionTemplate.query.filter_by(
            test_template_id=test_template.id
        ).order_by(QuestionTemplate.order).all()
        
        # Generate each test version
        num_versions = form.num_versions.data
        if num_versions is None:
            num_versions = 1
        for version_number in range(1, num_versions + 1):
            # Create a version record
            test_version = TestVersion()
            test_version.test_template_id = test_template.id
            test_version.version_number = version_number
            db.session.add(test_version)
            db.session.flush()  # Flush to get version ID
            
            # Generate questions for this version
            questions_data = generate_test_version_questions(question_templates, version_number)
            
            # Add questions to the database
            for q_data in questions_data:
                question = Question()
                question.test_version_id = test_version.id
                question.question_template_id = q_data['question_template_id']
                question.question_text = q_data['question_text']
                question.answer = q_data['answer']
                question.solution_steps = q_data['solution_steps']
                question.order = q_data['order']
                db.session.add(question)
        
        # Final commit for all versions and questions
        db.session.commit()
        
        # Redirect to view the test template
        flash('Test created successfully with multiple versions!', 'success')
        return redirect(url_for('view_test_template', template_uuid=test_template.uuid))
    
    return render_template('create_test.html', form=form)

@app.route('/test-template/<template_uuid>')
def view_test_template(template_uuid):
    """View a test template and its versions."""
    template = TestTemplate.query.filter_by(uuid=template_uuid).first_or_404()
    
    # Get all versions of this test
    versions = TestVersion.query.filter_by(
        test_template_id=template.id
    ).order_by(TestVersion.version_number).all()
    
    return render_template('view_test_template.html', template=template, versions=versions)

@app.route('/test-template/<template_uuid>/pdf')
def download_batch_pdf(template_uuid):
    """Generate and download a PDF with all versions of the test."""
    template = TestTemplate.query.filter_by(uuid=template_uuid).first_or_404()
    
    # Get all versions of this test
    versions = TestVersion.query.filter_by(
        test_template_id=template.id
    ).order_by(TestVersion.version_number).all()
    
    if not versions:
        flash('No test versions found for this template.', 'error')
        return redirect(url_for('view_test_template', template_uuid=template.uuid))
    
    # Generate batch PDF
    pdf_buffer = generate_batch_test_pdf(template, versions)
    
    # Send the PDF as a downloadable file
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{template.title.replace(' ', '_')}_all_versions.pdf"
    )

@app.route('/test-version/<test_uuid>')
def view_test_version(test_uuid):
    """View a specific test version."""
    test_version = TestVersion.query.filter_by(uuid=test_uuid).first_or_404()
    template = test_version.template
    
    # Get questions ordered by their order field
    questions = Question.query.filter_by(
        test_version_id=test_version.id
    ).order_by(Question.order).all()
    
    # Generate QR code for the answer key
    answer_key_url = url_for('answer_key', test_uuid=test_version.uuid, _external=True)
    qr_code_img = generate_qr_code(answer_key_url)
    
    return render_template(
        'view_test_version.html', 
        test_version=test_version, 
        template=template,
        questions=questions,
        qr_code=qr_code_img,
        access_code=test_version.get_access_code()
    )

@app.route('/test-version/<test_uuid>/pdf')
def download_test_version_pdf(test_uuid):
    """Generate and download a PDF of a specific test version."""
    test_version = TestVersion.query.filter_by(uuid=test_uuid).first_or_404()
    
    # Get questions ordered by their order field
    questions = Question.query.filter_by(
        test_version_id=test_version.id
    ).order_by(Question.order).all()
    
    # Create QR code for answer key
    answer_key_url = url_for('answer_key', test_uuid=test_version.uuid, _external=True)
    
    # Generate PDF
    pdf_buffer = generate_test_pdf(
        test_version, 
        questions, 
        answer_key_url,
        version_number=test_version.version_number
    )
    
    # Send the PDF as a downloadable file
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{test_version.template.title.replace(' ', '_')}_v{test_version.version_number}.pdf"
    )

@app.route('/answer-key/<test_uuid>', methods=['GET', 'POST'])
def answer_key(test_uuid):
    """Display the answer key for a test with password protection."""
    test_version = TestVersion.query.filter_by(uuid=test_uuid).first_or_404()
    template = test_version.template
    
    form = AnswerKeyAccessForm()
    
    # Check if user has already been authenticated for this answer key
    auth_key = f"auth_{test_uuid}"
    if session.get(auth_key):
        # User is authenticated, show the answer key
        questions = Question.query.filter_by(
            test_version_id=test_version.id
        ).order_by(Question.order).all()
        
        return render_template(
            'answer_key.html', 
            test_version=test_version, 
            template=template, 
            questions=questions
        )
    
    # User needs to authenticate
    if form.validate_on_submit():
        if template.check_password(form.password.data):
            # Store authentication in session
            session[auth_key] = True
            
            # Show the answer key
            questions = Question.query.filter_by(
                test_version_id=test_version.id
            ).order_by(Question.order).all()
            
            return render_template(
                'answer_key.html', 
                test_version=test_version, 
                template=template, 
                questions=questions
            )
        else:
            flash('Incorrect password. Please try again.', 'error')
    
    # Show password entry form
    return render_template(
        'answer_key_auth.html', 
        test_version=test_version, 
        template=template, 
        form=form,
        access_code=test_version.get_access_code()
    )

@app.route('/answer-key/<test_uuid>/pdf')
def download_answer_key_pdf(test_uuid):
    """Generate and download a PDF of the answer key."""
    test_version = TestVersion.query.filter_by(uuid=test_uuid).first_or_404()
    template = test_version.template
    
    # Check if user has already been authenticated for this answer key
    auth_key = f"auth_{test_uuid}"
    if not session.get(auth_key):
        flash('Please authenticate to access the answer key.', 'error')
        return redirect(url_for('answer_key', test_uuid=test_uuid))
    
    # Get questions ordered by their order field
    questions = Question.query.filter_by(
        test_version_id=test_version.id
    ).order_by(Question.order).all()
    
    # Generate PDF with answers
    pdf_buffer = generate_test_pdf(
        test_version, 
        questions, 
        version_number=test_version.version_number,
        include_answers=True
    )
    
    # Send the PDF as a downloadable file
    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{template.title.replace(' ', '_')}_v{test_version.version_number}_answers.pdf"
    )

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error_code=404, message='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html', error_code=500, message='Server error'), 500
