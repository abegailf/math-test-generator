import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, 
    TableStyle, Image, PageBreak, FrameBreak, Frame
)
from reportlab.lib.units import inch
from utils.qr_generator import generate_qr_code

def generate_test_pdf(test_version, questions, answer_key_url=None, version_number=None, include_answers=False):
    """
    Generate a PDF for a math test.
    
    Args:
        test_version: The TestVersion model object (or Test model for legacy support)
        questions: List of Question model objects
        answer_key_url: URL to the answer key (for QR code generation)
        version_number: Optional version number to display
        include_answers: Whether to include answers in the PDF
    
    Returns:
        io.BytesIO: A buffer containing the generated PDF
    """
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Create a custom style for questions
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=normal_style,
        fontSize=12,
        spaceAfter=10
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=normal_style,
        fontSize=12,
        textColor=colors.blue
    )
    
    # Get template/test information
    # Support both TestVersion and legacy Test models
    if hasattr(test_version, 'template'):
        # This is a TestVersion
        test_template = test_version.template
        title = test_template.title
        difficulty = test_template.difficulty
        topics = test_template.topics
        description = test_template.description
    else:
        # This is a legacy Test model
        title = test_version.title
        difficulty = test_version.difficulty
        topics = test_version.topics
        description = test_version.description
    
    # Start building the PDF content
    content = []
    
    # Add the test title and version
    if version_number is not None:
        content.append(Paragraph(f"{title} - Version {version_number}", title_style))
    else:
        content.append(Paragraph(title, title_style))
    
    content.append(Spacer(1, 0.2*inch))
    
    # Add test information
    content.append(Paragraph(f"Difficulty: {difficulty.capitalize()}", normal_style))
    
    # Format topics list for display
    topics_list = topics.split(',')
    topics_str = ', '.join([t.capitalize() for t in topics_list])
    content.append(Paragraph(f"Topics: {topics_str}", normal_style))
    
    # Add description if available
    if description:
        content.append(Spacer(1, 0.1*inch))
        content.append(Paragraph("Description:", heading_style))
        content.append(Paragraph(description, normal_style))
    
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Questions:", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    # Add each question
    for i, question in enumerate(questions):
        # Format the question
        question_text = f"{i+1}. {question.question_text}"
        content.append(Paragraph(question_text, question_style))
        
        # Create an answer space or show the answer
        if include_answers:
            answer_text = f"Answer: {question.answer}"
            content.append(Paragraph(answer_text, answer_style))
            
            # Add solution steps if available
            if question.solution_steps:
                solution_text = f"Solution: {question.solution_steps}"
                content.append(Paragraph(solution_text, answer_style))
        else:
            # Add blank space for the answer
            content.append(Paragraph("Answer: _______________________________", normal_style))
            content.append(Spacer(1, 0.3*inch))
    
    # Add QR code to the test (only if not including answers and a URL is provided)
    if not include_answers and answer_key_url:
        content.append(PageBreak())
        content.append(Paragraph("Secure Answer Key Access", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        # Generate QR code
        qr_img = generate_qr_code(answer_key_url, as_image=True)
        qr_width = 2 * inch
        
        # Add the QR code image
        content.append(Image(qr_img, width=qr_width, height=qr_width))
        
        # Add instructions
        content.append(Spacer(1, 0.1*inch))
        content.append(Paragraph("Scan the QR code above with a smartphone to access the answer key. A password is required for access.", normal_style))
        
        # If this is a TestVersion, include its access code if available
        if hasattr(test_version, 'get_access_code'):
            access_code = test_version.get_access_code()
            content.append(Spacer(1, 0.2*inch))
            content.append(Paragraph(f"Test Version ID: {access_code}", ParagraphStyle(
                'AccessCode',
                parent=normal_style,
                fontSize=10,
                alignment=1  # Center alignment
            )))
    
    # Build the PDF
    doc.build(content)
    
    return buffer

def generate_batch_test_pdf(test_template, test_versions):
    """
    Generate a PDF containing all test versions in a batch.
    
    Args:
        test_template: The TestTemplate model object
        test_versions: List of TestVersion model objects
    
    Returns:
        io.BytesIO: A buffer containing the generated PDF
    """
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    subheading_style = styles['Heading3']
    normal_style = styles['Normal']
    
    # Start building the PDF content
    content = []
    
    # Add cover page
    content.append(Paragraph(test_template.title, title_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph(f"Test Batch Summary", heading_style))
    content.append(Spacer(1, 0.1*inch))
    
    # Add test information
    content.append(Paragraph(f"Difficulty: {test_template.difficulty.capitalize()}", normal_style))
    
    # Format topics list for display
    topics = test_template.topics.split(',')
    topics_str = ', '.join([t.capitalize() for t in topics])
    content.append(Paragraph(f"Topics: {topics_str}", normal_style))
    
    # Add description if available
    if test_template.description:
        content.append(Spacer(1, 0.1*inch))
        content.append(Paragraph("Description:", subheading_style))
        content.append(Paragraph(test_template.description, normal_style))
    
    # Add test versions summary
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph(f"Number of Test Versions: {len(test_versions)}", normal_style))
    content.append(Paragraph(f"Questions per Test: {test_template.num_questions}", normal_style))
    
    # Add instruction for teachers
    content.append(Spacer(1, 0.3*inch))
    content.append(Paragraph("Instructions for Teachers:", heading_style))
    content.append(Paragraph("This PDF contains all versions of the test. Each test has a unique QR code that links to its specific answer key. The answer key is password-protected using the password you provided when creating the tests.", normal_style))
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph("Version Index:", subheading_style))
    
    # Create a table for the version index
    data = [["Version #", "Test ID", "Pages"]]
    for i, version in enumerate(test_versions):
        data.append([
            str(version.version_number), 
            version.get_access_code(),
            str(i*2 + 2) + "-" + str(i*2 + 3)  # Pages (2 pages per test)
        ])
    
    # Create the table
    version_table = Table(data, colWidths=[1*inch, 1.5*inch, 1*inch])
    version_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    content.append(version_table)
    content.append(PageBreak())
    
    # Add each test version
    for i, version in enumerate(test_versions):
        # Get questions for this version
        questions = version.questions
        
        # Get answer key URL
        answer_key_url = f"/answer-key/{version.uuid}"
        
        # Add the test
        content.append(Paragraph(f"{test_template.title} - Version {version.version_number}", title_style))
        content.append(Spacer(1, 0.2*inch))
        
        # Add test information
        content.append(Paragraph(f"Test ID: {version.get_access_code()}", normal_style))
        content.append(Paragraph(f"Difficulty: {test_template.difficulty.capitalize()}", normal_style))
        content.append(Paragraph(f"Topics: {topics_str}", normal_style))
        
        content.append(Spacer(1, 0.2*inch))
        content.append(Paragraph("Questions:", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        # Sort questions by order
        sorted_questions = sorted(questions, key=lambda q: q.order)
        
        # Add each question
        for j, question in enumerate(sorted_questions):
            # Format the question
            question_text = f"{j+1}. {question.question_text}"
            content.append(Paragraph(question_text, normal_style))
            
            # Add blank space for the answer
            content.append(Paragraph("Answer: _______________________________", normal_style))
            content.append(Spacer(1, 0.2*inch))
        
        # Add QR code
        content.append(PageBreak())
        content.append(Paragraph("Secure Answer Key Access", heading_style))
        content.append(Spacer(1, 0.1*inch))
        
        # Generate QR code
        qr_img = generate_qr_code(answer_key_url, as_image=True)
        qr_width = 2 * inch
        
        # Add the QR code image
        content.append(Image(qr_img, width=qr_width, height=qr_width))
        
        # Add instructions
        content.append(Spacer(1, 0.1*inch))
        content.append(Paragraph("Scan the QR code above with a smartphone to access the answer key. A password is required for access.", normal_style))
        content.append(Spacer(1, 0.2*inch))
        content.append(Paragraph(f"Test Version ID: {version.get_access_code()}", ParagraphStyle(
            'AccessCode',
            parent=normal_style,
            fontSize=10,
            alignment=1  # Center alignment
        )))
        
        # Add page break between test versions (except for the last one)
        if i < len(test_versions) - 1:
            content.append(PageBreak())
    
    # Build the PDF
    doc.build(content)
    
    return buffer
