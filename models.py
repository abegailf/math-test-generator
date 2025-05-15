import uuid
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class TestTemplate(db.Model):
    """Model representing a math test template."""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), nullable=False)  # 'easy', 'medium', 'hard'
    topics = db.Column(db.String(200), nullable=False)  # Comma-separated list of topics
    num_questions = db.Column(db.Integer, nullable=False)
    num_versions = db.Column(db.Integer, nullable=False, default=1)  # Number of unique test versions
    password_hash = db.Column(db.String(256), nullable=False)  # For secure answer key access
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    question_templates = db.relationship('QuestionTemplate', backref='test_template', lazy=True, cascade="all, delete-orphan")
    test_versions = db.relationship('TestVersion', backref='template', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f"<TestTemplate {self.title}>"

class QuestionTemplate(db.Model):
    """Model representing a template for generating question variations."""
    id = db.Column(db.Integer, primary_key=True)
    test_template_id = db.Column(db.Integer, db.ForeignKey('test_template.id'), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # Type of question (e.g., 'addition', 'multiplication')
    difficulty = db.Column(db.String(20), nullable=False)  # 'easy', 'medium', 'hard'
    order = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<QuestionTemplate {self.id} for TestTemplate {self.test_template_id}>"

class TestVersion(db.Model):
    """Model representing a specific version of a test."""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    test_template_id = db.Column(db.Integer, db.ForeignKey('test_template.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with questions
    questions = db.relationship('Question', backref='test_version', lazy=True, cascade="all, delete-orphan")
    
    def get_access_code(self):
        """Generate a unique access code for this test version's answer key."""
        unique_string = f"{self.uuid}-{self.test_template_id}-{self.version_number}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:8].upper()
    
    def __repr__(self):
        return f"<TestVersion {self.version_number} for TestTemplate {self.test_template_id}>"

class Question(db.Model):
    """Model representing a specific question instance."""
    id = db.Column(db.Integer, primary_key=True)
    test_version_id = db.Column(db.Integer, db.ForeignKey('test_version.id'), nullable=False)
    question_template_id = db.Column(db.Integer, db.ForeignKey('question_template.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    solution_steps = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False)
    
    # Relationship with question template
    question_template = db.relationship('QuestionTemplate')
    
    def __repr__(self):
        return f"<Question {self.id} for TestVersion {self.test_version_id}>"
