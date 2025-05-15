import random
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, solve, Eq

def generate_question_templates(topics, difficulty, num_questions):
    """
    Generate question templates based on the selected topics, difficulty, and number of questions.
    
    Args:
        topics (list): List of math topics to generate templates for
        difficulty (str): Difficulty level ('easy', 'medium', or 'hard')
        num_questions (int): Number of questions to generate
    
    Returns:
        list: List of question template tuples (question_type, difficulty, order)
    """
    templates = []
    
    # Ensure we have at least one topic
    if not topics or len(topics) == 0:
        # Default to addition if no topics selected (should not happen due to form validation)
        topics = ['addition']
    
    # Determine number of questions per topic
    questions_per_topic = {topic: 0 for topic in topics}
    remaining = num_questions
    
    # Distribute questions among topics
    while remaining > 0:
        for topic in topics:
            if remaining > 0:
                questions_per_topic[topic] += 1
                remaining -= 1
            else:
                break
    
    # Create template for each topic
    question_order = 1
    for topic in topics:
        num_topic_questions = questions_per_topic[topic]
        for _ in range(num_topic_questions):
            templates.append((topic, difficulty, question_order))
            question_order += 1
    
    return templates

def generate_question_from_template(question_type, difficulty, seed=None):
    """
    Generate a math question based on the template with optional seed for reproducibility.
    
    Args:
        question_type (str): Type of question to generate (e.g., 'addition', 'multiplication')
        difficulty (str): Difficulty level ('easy', 'medium', or 'hard')
        seed (int, optional): Random seed for reproducible question generation
    
    Returns:
        dict: Dictionary containing question, answer, and solution
    """
    # Set random seed if provided for reproducible question generation
    if seed is not None:
        random.seed(seed)
    
    # Generate question based on type
    if question_type == 'addition':
        q = generate_addition_question(difficulty)
    elif question_type == 'subtraction':
        q = generate_subtraction_question(difficulty)
    elif question_type == 'multiplication':
        q = generate_multiplication_question(difficulty)
    elif question_type == 'division':
        q = generate_division_question(difficulty)
    elif question_type == 'fractions':
        q = generate_fraction_question(difficulty)
    elif question_type == 'decimals':
        q = generate_decimal_question(difficulty)
    elif question_type == 'percentages':
        q = generate_percentage_question(difficulty)
    elif question_type == 'algebra':
        q = generate_algebra_question(difficulty)
    elif question_type == 'geometry':
        q = generate_geometry_question(difficulty)
    elif question_type == 'statistics':
        q = generate_statistics_question(difficulty)
    else:
        q = generate_addition_question(difficulty)  # Default fallback
    
    return q

def generate_test_version_questions(question_templates, version_number):
    """
    Generate a unique set of questions for a specific test version.
    
    Args:
        question_templates (list): List of QuestionTemplate objects
        version_number (int): The version number of the test
    
    Returns:
        list: List of dictionaries containing question, answer, and solution
    """
    questions = []
    
    # Generate a unique question for each template using template ID + version number as seed
    for template in question_templates:
        # Create a seed from template ID and version number for reproducibility
        seed_value = template.id * 1000 + version_number
        
        # Generate the question
        question_data = generate_question_from_template(
            template.question_type, 
            template.difficulty,
            seed=seed_value
        )
        
        questions.append({
            'question_template_id': template.id,
            'question_text': question_data['question'],
            'answer': question_data['answer'],
            'solution_steps': question_data.get('solution', ''),
            'order': template.order
        })
    
    return questions

def generate_math_questions(topics, difficulty, num_questions):
    """
    Legacy method to maintain compatibility with existing code.
    Generate math questions based on the selected topics, difficulty, and number of questions.
    
    Args:
        topics (list): List of math topics to generate questions for
        difficulty (str): Difficulty level ('easy', 'medium', or 'hard')
        num_questions (int): Number of questions to generate
    
    Returns:
        list: List of dictionaries containing question, answer, and solution
    """
    questions = []
    
    # Determine number of questions per topic
    questions_per_topic = {topic: 0 for topic in topics}
    remaining = num_questions
    
    # Distribute questions among topics
    while remaining > 0:
        for topic in topics:
            if remaining > 0:
                questions_per_topic[topic] += 1
                remaining -= 1
            else:
                break
    
    # Generate questions for each topic
    for topic in topics:
        num_topic_questions = questions_per_topic[topic]
        for _ in range(num_topic_questions):
            q = generate_question_from_template(topic, difficulty)
            questions.append(q)
    
    # Shuffle the questions to mix topics
    random.shuffle(questions)
    
    return questions

def generate_addition_question(difficulty):
    """Generate an addition problem based on the specified difficulty."""
    if difficulty == 'easy':
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        answer = a + b
        question = f"What is {a} + {b}?"
        solution = f"{a} + {b} = {answer}"
    elif difficulty == 'medium':
        a = random.randint(10, 100)
        b = random.randint(10, 100)
        answer = a + b
        question = f"Calculate {a} + {b}."
        solution = f"{a} + {b} = {answer}"
    else:  # hard
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        c = random.randint(10, 100)
        answer = a + b + c
        question = f"Find the sum of {a}, {b}, and {c}."
        solution = f"{a} + {b} + {c} = {answer}"
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }

def generate_subtraction_question(difficulty):
    """Generate a subtraction problem based on the specified difficulty."""
    if difficulty == 'easy':
        b = random.randint(1, 10)
        a = random.randint(b, 20)  # Ensure a > b to avoid negative answers
        answer = a - b
        question = f"What is {a} - {b}?"
        solution = f"{a} - {b} = {answer}"
    elif difficulty == 'medium':
        b = random.randint(10, 50)
        a = random.randint(b, 100)
        answer = a - b
        question = f"Calculate {a} - {b}."
        solution = f"{a} - {b} = {answer}"
    else:  # hard
        b = random.randint(100, 500)
        a = random.randint(b, 1000)
        answer = a - b
        question = f"Subtract {b} from {a}."
        solution = f"{a} - {b} = {answer}"
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }

def generate_multiplication_question(difficulty):
    """Generate a multiplication problem based on the specified difficulty."""
    if difficulty == 'easy':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        answer = a * b
        question = f"What is {a} × {b}?"
        solution = f"{a} × {b} = {answer}"
    elif difficulty == 'medium':
        a = random.randint(10, 20)
        b = random.randint(1, 10)
        answer = a * b
        question = f"Calculate {a} × {b}."
        solution = f"{a} × {b} = {answer}"
    else:  # hard
        a = random.randint(11, 30)
        b = random.randint(11, 20)
        answer = a * b
        question = f"Find the product of {a} and {b}."
        solution = f"{a} × {b} = {answer}"
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }

def generate_division_question(difficulty):
    """Generate a division problem based on the specified difficulty."""
    if difficulty == 'easy':
        b = random.randint(1, 10)
        a = b * random.randint(1, 10)  # Ensure clean division
        answer = a // b
        question = f"What is {a} ÷ {b}?"
        solution = f"{a} ÷ {b} = {answer}"
    elif difficulty == 'medium':
        b = random.randint(2, 12)
        a = b * random.randint(5, 15)
        answer = a // b
        question = f"Calculate {a} ÷ {b}."
        solution = f"{a} ÷ {b} = {answer}"
    else:  # hard
        b = random.randint(5, 20)
        a = b * random.randint(10, 30)
        answer = a // b
        question = f"Divide {a} by {b}."
        solution = f"{a} ÷ {b} = {answer}"
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }

def generate_fraction_question(difficulty):
    """Generate a fraction problem based on the specified difficulty."""
    if difficulty == 'easy':
        a = random.randint(1, 5)
        b = random.randint(a+1, 10)
        c = random.randint(1, 5)
        d = random.randint(c+1, 10)
        # Simple addition of fractions with the same denominator
        if random.choice([True, False]):
            question = f"Add the fractions: {a}/{b} + {c}/{b}"
            num = a + c
            denom = b
            # Simplify the fraction
            gcd = sp.gcd(num, denom)
            answer = f"{num//gcd}/{denom//gcd}" if gcd > 1 else f"{num}/{denom}"
            solution = f"{a}/{b} + {c}/{b} = {num}/{denom}"
            if gcd > 1:
                solution += f" = {num//gcd}/{denom//gcd}"
        else:
            question = f"What is the simplified form of {a*2}/{b*2}?"
            gcd = sp.gcd(a*2, b*2)
            answer = f"{(a*2)//gcd}/{(b*2)//gcd}"
            solution = f"{a*2}/{b*2} = {(a*2)//gcd}/{(b*2)//gcd}"
    
    elif difficulty == 'medium':
        a = random.randint(1, 5)
        b = random.randint(2, 10)
        c = random.randint(1, 5)
        d = random.randint(2, 10)
        operation = random.choice(['add', 'subtract', 'multiply'])
        
        if operation == 'add' or operation == 'subtract':
            # Make sure denominators are different
            while b == d:
                d = random.randint(2, 10)
            
            # Find the LCM
            lcm = (b * d) // sp.gcd(b, d)
            a_new = a * (lcm // b)
            c_new = c * (lcm // d)
            
            if operation == 'add':
                question = f"Add the fractions: {a}/{b} + {c}/{d}"
                result = a_new + c_new
                solution = f"{a}/{b} + {c}/{d} = {a_new}/{lcm} + {c_new}/{lcm} = {result}/{lcm}"
            else:
                question = f"Subtract the fractions: {a}/{b} - {c}/{d}"
                result = a_new - c_new
                solution = f"{a}/{b} - {c}/{d} = {a_new}/{lcm} - {c_new}/{lcm} = {result}/{lcm}"
            
            # Simplify the result
            gcd = sp.gcd(result, lcm)
            if gcd > 1:
                answer = f"{result//gcd}/{lcm//gcd}"
                solution += f" = {result//gcd}/{lcm//gcd}"
            else:
                answer = f"{result}/{lcm}"
        
        else:  # multiply
            question = f"Multiply the fractions: {a}/{b} × {c}/{d}"
            num = a * c
            denom = b * d
            # Simplify the fraction
            gcd = sp.gcd(num, denom)
            answer = f"{num//gcd}/{denom//gcd}" if gcd > 1 else f"{num}/{denom}"
            solution = f"{a}/{b} × {c}/{d} = {a*c}/{b*d}"
            if gcd > 1:
                solution += f" = {num//gcd}/{denom//gcd}"
    
    else:  # hard
        a = random.randint(1, 10)
        b = random.randint(2, 12)
        c = random.randint(1, 10)
        d = random.randint(2, 12)
        operation = random.choice(['add', 'subtract', 'multiply', 'divide'])
        
        if operation == 'add' or operation == 'subtract':
            # Find the LCM
            lcm = (b * d) // sp.gcd(b, d)
            a_new = a * (lcm // b)
            c_new = c * (lcm // d)
            
            if operation == 'add':
                question = f"Add the fractions: {a}/{b} + {c}/{d}"
                result = a_new + c_new
                solution = f"{a}/{b} + {c}/{d} = {a_new}/{lcm} + {c_new}/{lcm} = {result}/{lcm}"
            else:
                question = f"Subtract the fractions: {a}/{b} - {c}/{d}"
                result = a_new - c_new
                solution = f"{a}/{b} - {c}/{d} = {a_new}/{lcm} - {c_new}/{lcm} = {result}/{lcm}"
            
            # Simplify the result
            gcd = sp.gcd(result, lcm)
            if gcd > 1:
                answer = f"{result//gcd}/{lcm//gcd}"
                solution += f" = {result//gcd}/{lcm//gcd}"
            else:
                answer = f"{result}/{lcm}"
        
        elif operation == 'multiply':
            question = f"Multiply the fractions: {a}/{b} × {c}/{d}"
            num = a * c
            denom = b * d
            # Simplify the fraction
            gcd = sp.gcd(num, denom)
            answer = f"{num//gcd}/{denom//gcd}" if gcd > 1 else f"{num}/{denom}"
            solution = f"{a}/{b} × {c}/{d} = {a*c}/{b*d}"
            if gcd > 1:
                solution += f" = {num//gcd}/{denom//gcd}"
        
        else:  # divide
            question = f"Divide the fractions: {a}/{b} ÷ {c}/{d}"
            num = a * d
            denom = b * c
            # Simplify the fraction
            gcd = sp.gcd(num, denom)
            answer = f"{num//gcd}/{denom//gcd}" if gcd > 1 else f"{num}/{denom}"
            solution = f"{a}/{b} ÷ {c}/{d} = {a}/{b} × {d}/{c} = {a*d}/{b*c}"
            if gcd > 1:
                solution += f" = {num//gcd}/{denom//gcd}"
    
    return {
        'question': question,
        'answer': answer,
        'solution': solution
    }

def generate_decimal_question(difficulty):
    """Generate a decimal problem based on the specified difficulty."""
    if difficulty == 'easy':
        a = round(random.uniform(0.1, 10.0), 1)
        b = round(random.uniform(0.1, 10.0), 1)
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            answer = round(a + b, 1)
            question = f"What is {a} + {b}?"
            solution = f"{a} + {b} = {answer}"
        else:
            # Ensure a > b to avoid negative answers
            if a < b:
                a, b = b, a
            answer = round(a - b, 1)
            question = f"What is {a} - {b}?"
            solution = f"{a} - {b} = {answer}"
    
    elif difficulty == 'medium':
        a = round(random.uniform(0.1, 20.0), 2)
        b = round(random.uniform(0.1, 20.0), 2)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            answer = round(a + b, 2)
            question = f"Calculate {a} + {b}."
            solution = f"{a} + {b} = {answer}"
        elif operation == '-':
            # Ensure a > b to avoid negative answers
            if a < b:
                a, b = b, a
            answer = round(a - b, 2)
            question = f"Calculate {a} - {b}."
            solution = f"{a} - {b} = {answer}"
        else:  # multiplication
            # Use smaller numbers for multiplication
            a = round(random.uniform(0.1, 10.0), 1)
            b = round(random.uniform(0.1, 10.0), 1)
            answer = round(a * b, 2)
            question = f"Calculate {a} × {b}."
            solution = f"{a} × {b} = {answer}"
    
    else:  # hard
        operation = random.choice(['+', '-', '*', '/'])
        
        if operation in ['+', '-']:
            a = round(random.uniform(10.0, 100.0), 2)
            b = round(random.uniform(10.0, 100.0), 2)
            
            if operation == '+':
                answer = round(a + b, 2)
                question = f"Calculate {a} + {b}."
                solution = f"{a} + {b} = {answer}"
            else:
                # Ensure a > b to avoid negative answers
                if a < b:
                    a, b = b, a
                answer = round(a - b, 2)
                question = f"Calculate {a} - {b}."
                solution = f"{a} - {b} = {answer}"
        
        elif operation == '*':
            a = round(random.uniform(0.1, 10.0), 2)
            b = round(random.uniform(0.1, 10.0), 2)
            answer = round(a * b, 2)
            question = f"Calculate {a} × {b}."
            solution = f"{a} × {b} = {answer}"
        
        else:  # division
            b = round(random.uniform(0.5, 5.0), 1)
            # Create a divisible number to avoid long decimal answers
            a = round(b * round(random.uniform(1.0, 10.0), 1), 1)
            answer = round(a / b, 2)
            question = f"Calculate {a} ÷ {b}."
            solution = f"{a} ÷ {b} = {answer}"
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }

def generate_percentage_question(difficulty):
    """Generate a percentage problem based on the specified difficulty."""
    if difficulty == 'easy':
        # Find a percentage of a number
        percentage = random.choice([10, 20, 25, 50, 75])
        number = random.randint(10, 100) * 4  # Make it divisible by 4 for easier calculations
        answer = (percentage / 100) * number
        question = f"What is {percentage}% of {number}?"
        solution = f"{percentage}% of {number} = {percentage/100} × {number} = {answer}"
    
    elif difficulty == 'medium':
        question_type = random.choice(['find_percentage', 'find_number'])
        
        if question_type == 'find_percentage':
            # Find what percentage one number is of another
            b = random.randint(10, 100)
            percentage = random.choice([10, 20, 25, 40, 50, 60, 75])
            a = int(b * (percentage / 100))
            answer = percentage
            question = f"{a} is what percentage of {b}?"
            solution = f"{a} ÷ {b} × 100 = {a/b:.2f} × 100 = {percentage}%"
        
        else:  # find_number
            # Find the original number when given a percentage of it
            percentage = random.choice([10, 20, 25, 30, 40, 50, 60, 75])
            result = random.randint(10, 200)
            original = result * 100 / percentage
            answer = original
            question = f"If {percentage}% of a number is {result}, what is the original number?"
            solution = f"Let x be the original number.\n{percentage}% of x = {result}\n{percentage/100} × x = {result}\nx = {result} ÷ {percentage/100} = {result} × {100/percentage} = {original}"
    
    else:  # hard
        question_type = random.choice(['increase_decrease', 'complex'])
        
        if question_type == 'increase_decrease':
            # Percentage increase or decrease
            original = random.randint(50, 500)
            percentage = random.randint(5, 50)
            increase = random.choice([True, False])
            
            if increase:
                new_value = original * (1 + percentage/100)
                answer = new_value
                question = f"If {original} is increased by {percentage}%, what is the new value?"
                solution = f"New value = {original} × (1 + {percentage}/100) = {original} × {1 + percentage/100} = {new_value}"
            else:
                new_value = original * (1 - percentage/100)
                answer = new_value
                question = f"If {original} is decreased by {percentage}%, what is the new value?"
                solution = f"New value = {original} × (1 - {percentage}/100) = {original} × {1 - percentage/100} = {new_value}"
        
        else:  # complex
            # Multi-step percentage problem
            original = random.randint(100, 500)
            percent1 = random.randint(10, 30)
            percent2 = random.randint(10, 30)
            
            intermediate = original * (1 + percent1/100)
            final = intermediate * (1 - percent2/100)
            answer = final
            question = f"A value of {original} is increased by {percent1}% and then decreased by {percent2}%. What is the final value?"
            solution = f"First increase: {original} × (1 + {percent1}/100) = {original} × {1 + percent1/100} = {intermediate}\nThen decrease: {intermediate} × (1 - {percent2}/100) = {intermediate} × {1 - percent2/100} = {final}"
    
    return {
        'question': question,
        'answer': str(round(answer, 2)) if isinstance(answer, float) else str(answer),
        'solution': solution
    }

def generate_algebra_question(difficulty):
    """Generate an algebra problem based on the specified difficulty."""
    x = symbols('x')
    
    if difficulty == 'easy':
        # Simple linear equation: ax + b = c
        a = random.randint(1, 5)
        b = random.randint(1, 10)
        c = random.randint(1, 20)
        equation = f"{a}x + {b} = {c}"
        solution_value = (c - b) / a
        
        question = f"Solve for x: {equation}"
        solution = f"{equation}\n{a}x = {c} - {b}\n{a}x = {c-b}\nx = {solution_value}"
        
        if solution_value.is_integer():
            answer = str(int(solution_value))
        else:
            answer = str(solution_value)
    
    elif difficulty == 'medium':
        # More complex linear equations or simple quadratics
        equation_type = random.choice(['linear', 'quadratic'])
        
        if equation_type == 'linear':
            # Linear equation with variables on both sides: ax + b = cx + d
            a = random.randint(2, 8)
            b = random.randint(1, 15)
            c = random.randint(1, a-1)  # Ensure a > c for unique solution
            d = random.randint(1, 20)
            
            equation = f"{a}x + {b} = {c}x + {d}"
            solution_value = (d - b) / (a - c)
            
            question = f"Solve for x: {equation}"
            solution = f"{equation}\n{a}x - {c}x = {d} - {b}\n{a-c}x = {d-b}\nx = {solution_value}"
            
            if solution_value.is_integer():
                answer = str(int(solution_value))
            else:
                answer = str(solution_value)
        
        else:  # quadratic
            # Simple quadratic with integer solutions: x² - (a+b)x + ab = 0 with roots a, b
            a = random.randint(-5, 5)
            while a == 0:  # Avoid zero
                a = random.randint(-5, 5)
            
            b = random.randint(-5, 5)
            while b == 0 or b == a:  # Avoid zero and duplicate roots
                b = random.randint(-5, 5)
            
            equation = f"x² - {a+b}x + {a*b} = 0"
            
            question = f"Find the roots of the quadratic equation: {equation}"
            solution = f"{equation}\nUsing the quadratic formula or factoring:\n(x - {a})(x - {b}) = 0\nx = {a} or x = {b}"
            answer = f"{a}, {b}" if a < b else f"{b}, {a}"
    
    else:  # hard
        question_type = random.choice(['quadratic', 'system', 'word_problem'])
        
        if question_type == 'quadratic':
            # Quadratic with fractional or irrational roots
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            
            equation = f"{a}x² + {b}x + {c} = 0"
            
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                # If discriminant is negative, regenerate for real solutions
                return generate_algebra_question('hard')
            
            sol1 = (-b + sp.sqrt(discriminant)) / (2*a)
            sol2 = (-b - sp.sqrt(discriminant)) / (2*a)
            
            question = f"Solve the quadratic equation: {equation}"
            solution = f"{equation}\nUsing the quadratic formula:\nx = (-{b} ± √({b}² - 4 × {a} × {c})) / (2 × {a})\nx = ({-b} ± √{discriminant}) / {2*a}\nx₁ = {sol1}\nx₂ = {sol2}"
            
            # Format the answer nicely
            if sol1.is_integer() and sol2.is_integer():
                answer = f"{int(sol1)}, {int(sol2)}" if sol1 < sol2 else f"{int(sol2)}, {int(sol1)}"
            else:
                answer = f"{sol1}, {sol2}" if sol1 < sol2 else f"{sol2}, {sol1}"
        
        elif question_type == 'system':
            # System of two linear equations with integer solutions
            x, y = symbols('x y')
            
            # Create a system with integer solutions
            x_val = random.randint(-5, 5)
            y_val = random.randint(-5, 5)
            
            # Create two equations that have the solution (x_val, y_val)
            a1 = random.randint(1, 5)
            b1 = random.randint(1, 5)
            c1 = a1 * x_val + b1 * y_val
            
            a2 = random.randint(1, 5)
            while a2 == a1:  # Ensure different coefficients
                a2 = random.randint(1, 5)
            
            b2 = random.randint(1, 5)
            while (b2 * a1 == b1 * a2):  # Ensure independent equations
                b2 = random.randint(1, 5)
            
            c2 = a2 * x_val + b2 * y_val
            
            question = f"Solve the system of equations:\n{a1}x + {b1}y = {c1}\n{a2}x + {b2}y = {c2}"
            solution = f"Using substitution or elimination:\nFrom the first equation: {a1}x + {b1}y = {c1}\nFrom the second equation: {a2}x + {b2}y = {c2}\nSolving the system gives x = {x_val}, y = {y_val}"
            answer = f"x = {x_val}, y = {y_val}"
        
        else:  # word_problem
            # Age problem: current sum is a, in b years sum will be c
            current_age1 = random.randint(20, 40)
            current_age2 = random.randint(5, 15)
            years_later = random.randint(5, 10)
            
            sum_now = current_age1 + current_age2
            sum_later = sum_now + 2 * years_later
            ratio_later = (current_age1 + years_later) / (current_age2 + years_later)
            ratio_later = round(ratio_later, 1)
            
            question = f"A person is {sum_now - current_age2} years older than another person. The sum of their ages is {sum_now}. In {years_later} years, the ratio of their ages will be {ratio_later}. Find their current ages."
            solution = f"Let x be the age of the older person and y be the age of the younger person.\nWe know x - y = {sum_now - current_age2} and x + y = {sum_now}.\nFrom the first equation: x = y + {sum_now - current_age2}\nSubstituting into the second equation: (y + {sum_now - current_age2}) + y = {sum_now}\n2y + {sum_now - current_age2} = {sum_now}\n2y = {current_age2}\ny = {current_age2}\nTherefore, x = {current_age1} and y = {current_age2}"
            answer = f"{current_age1}, {current_age2}"
    
    return {
        'question': question,
        'answer': answer,
        'solution': solution
    }

def generate_geometry_question(difficulty):
    """Generate a geometry problem based on the specified difficulty."""
    if difficulty == 'easy':
        # Simple area or perimeter problems
        shape = random.choice(['rectangle', 'square', 'triangle'])
        
        if shape == 'rectangle':
            length = random.randint(3, 15)
            width = random.randint(2, 10)
            
            calc_type = random.choice(['area', 'perimeter'])
            if calc_type == 'area':
                answer = length * width
                question = f"What is the area of a rectangle with length {length} units and width {width} units?"
                solution = f"Area of a rectangle = length × width = {length} × {width} = {answer} square units"
            else:
                answer = 2 * (length + width)
                question = f"What is the perimeter of a rectangle with length {length} units and width {width} units?"
                solution = f"Perimeter of a rectangle = 2 × (length + width) = 2 × ({length} + {width}) = 2 × {length + width} = {answer} units"
        
        elif shape == 'square':
            side = random.randint(2, 15)
            
            calc_type = random.choice(['area', 'perimeter'])
            if calc_type == 'area':
                answer = side ** 2
                question = f"What is the area of a square with side length {side} units?"
                solution = f"Area of a square = side² = {side}² = {answer} square units"
            else:
                answer = 4 * side
                question = f"What is the perimeter of a square with side length {side} units?"
                solution = f"Perimeter of a square = 4 × side = 4 × {side} = {answer} units"
        
        else:  # triangle
            base = random.randint(3, 15)
            height = random.randint(2, 10)
            
            answer = (base * height) / 2
            question = f"What is the area of a triangle with base {base} units and height {height} units?"
            solution = f"Area of a triangle = ½ × base × height = ½ × {base} × {height} = {answer} square units"
    
    elif difficulty == 'medium':
        # More complex shapes or Pythagorean theorem
        shape = random.choice(['circle', 'trapezoid', 'right_triangle'])
        
        if shape == 'circle':
            radius = random.randint(2, 12)
            
            calc_type = random.choice(['area', 'circumference'])
            if calc_type == 'area':
                answer = round(3.14159 * (radius ** 2), 2)
                question = f"What is the area of a circle with radius {radius} units? (Use π ≈ 3.14159)"
                solution = f"Area of a circle = πr² = 3.14159 × {radius}² = 3.14159 × {radius**2} = {answer} square units"
            else:
                answer = round(2 * 3.14159 * radius, 2)
                question = f"What is the circumference of a circle with radius {radius} units? (Use π ≈ 3.14159)"
                solution = f"Circumference of a circle = 2πr = 2 × 3.14159 × {radius} = {answer} units"
        
        elif shape == 'trapezoid':
            base1 = random.randint(5, 15)
            base2 = random.randint(5, 15)
            height = random.randint(3, 10)
            
            answer = (base1 + base2) * height / 2
            question = f"What is the area of a trapezoid with parallel sides of lengths {base1} units and {base2} units, and height {height} units?"
            solution = f"Area of a trapezoid = ½ × (sum of parallel sides) × height = ½ × ({base1} + {base2}) × {height} = ½ × {base1 + base2} × {height} = {answer} square units"
        
        else:  # right_triangle (Pythagorean theorem)
            # Use Pythagorean triples for clean answers
            triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
            a, b, c = random.choice(triples)
            
            # Scale the triple for variety
            scale = random.randint(1, 3)
            a, b, c = a * scale, b * scale, c * scale
            
            # Randomly choose which side to solve for
            unknown = random.choice(['a', 'b', 'c'])
            
            if unknown == 'a':
                answer = a
                question = f"In a right triangle, if one leg is {b} units and the hypotenuse is {c} units, what is the length of the other leg?"
                solution = f"Using the Pythagorean theorem: a² + b² = c²\na² + {b}² = {c}²\na² + {b**2} = {c**2}\na² = {c**2} - {b**2}\na² = {c**2 - b**2}\na = √{c**2 - b**2} = {answer} units"
            
            elif unknown == 'b':
                answer = b
                question = f"In a right triangle, if one leg is {a} units and the hypotenuse is {c} units, what is the length of the other leg?"
                solution = f"Using the Pythagorean theorem: a² + b² = c²\n{a}² + b² = {c}²\n{a**2} + b² = {c**2}\nb² = {c**2} - {a**2}\nb² = {c**2 - a**2}\nb = √{c**2 - a**2} = {answer} units"
            
            else:  # unknown == 'c'
                answer = c
                question = f"In a right triangle with legs of lengths {a} units and {b} units, what is the length of the hypotenuse?"
                solution = f"Using the Pythagorean theorem: a² + b² = c²\n{a}² + {b}² = c²\n{a**2} + {b**2} = c²\nc² = {a**2 + b**2}\nc = √{a**2 + b**2} = {answer} units"
    
    else:  # hard
        # Advanced geometric concepts
        problem_type = random.choice(['3d_volume', 'similar_triangles', 'coordinate_geometry'])
        
        if problem_type == '3d_volume':
            shape = random.choice(['cube', 'cylinder', 'sphere'])
            
            if shape == 'cube':
                side = random.randint(3, 10)
                answer = side ** 3
                question = f"What is the volume of a cube with side length {side} units?"
                solution = f"Volume of a cube = side³ = {side}³ = {answer} cubic units"
            
            elif shape == 'cylinder':
                radius = random.randint(2, 8)
                height = random.randint(3, 10)
                answer = round(3.14159 * (radius ** 2) * height, 2)
                question = f"What is the volume of a cylinder with radius {radius} units and height {height} units? (Use π ≈ 3.14159)"
                solution = f"Volume of a cylinder = πr²h = 3.14159 × {radius}² × {height} = 3.14159 × {radius**2} × {height} = {answer} cubic units"
            
            else:  # sphere
                radius = random.randint(2, 10)
                answer = round((4/3) * 3.14159 * (radius ** 3), 2)
                question = f"What is the volume of a sphere with radius {radius} units? (Use π ≈ 3.14159)"
                solution = f"Volume of a sphere = (4/3)πr³ = (4/3) × 3.14159 × {radius}³ = (4/3) × 3.14159 × {radius**3} = {answer} cubic units"
        
        elif problem_type == 'similar_triangles':
            # Similar triangles problem
            scale = random.randint(2, 5)
            side1 = random.randint(3, 10)
            side2 = side1 * scale
            
            # Create a related length to find
            unknown_side_small = random.randint(4, 12)
            unknown_side_large = unknown_side_small * scale
            
            question = f"Two triangles are similar. In the smaller triangle, one side is {side1} units and another side is {unknown_side_small} units. In the larger triangle, the corresponding side to the {side1}-unit side is {side2} units. What is the length of the corresponding side to the {unknown_side_small}-unit side in the larger triangle?"
            solution = f"For similar triangles, the ratio of corresponding sides is constant.\nRatio = {side2}/{side1} = {scale}\nSo, the unknown side = {unknown_side_small} × {scale} = {unknown_side_large} units"
            answer = unknown_side_large
        
        else:  # coordinate_geometry
            # Distance between two points or midpoint
            calc_type = random.choice(['distance', 'midpoint'])
            
            # Generate points with integer coordinates for simplicity
            x1 = random.randint(-10, 10)
            y1 = random.randint(-10, 10)
            x2 = random.randint(-10, 10)
            y2 = random.randint(-10, 10)
            
            if calc_type == 'distance':
                answer = round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)
                question = f"What is the distance between the points ({x1}, {y1}) and ({x2}, {y2})?"
                solution = f"Distance = √[(x₂ - x₁)² + (y₂ - y₁)²] = √[({x2} - {x1})² + ({y2} - {y1})²] = √[{(x2-x1)**2} + {(y2-y1)**2}] = √{(x2-x1)**2 + (y2-y1)**2} = {answer} units"
            
            else:  # midpoint
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Format the answer nicely
                if mid_x.is_integer():
                    mid_x = int(mid_x)
                if mid_y.is_integer():
                    mid_y = int(mid_y)
                
                question = f"What is the midpoint of the line segment connecting the points ({x1}, {y1}) and ({x2}, {y2})?"
                solution = f"Midpoint = ((x₁ + x₂)/2, (y₁ + y₂)/2) = (({x1} + {x2})/2, ({y1} + {y2})/2) = ({mid_x}, {mid_y})"
                answer = f"({mid_x}, {mid_y})"
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }

def generate_statistics_question(difficulty):
    """Generate a statistics problem based on the specified difficulty."""
    if difficulty == 'easy':
        # Mean, median, mode of a small dataset
        stat_type = random.choice(['mean', 'median', 'mode'])
        
        # Generate a small dataset with integer values
        data_size = random.randint(5, 8)
        
        if stat_type == 'mean':
            # Create data where the mean is an integer for simplicity
            mean = random.randint(5, 15)
            data = [random.randint(mean-5, mean+5) for _ in range(data_size-1)]
            # Make sure the last number makes the mean exact
            sum_so_far = sum(data)
            last_value = mean * data_size - sum_so_far
            data.append(last_value)
            random.shuffle(data)
            
            data_str = ", ".join(map(str, data))
            question = f"What is the mean (average) of the following numbers: {data_str}?"
            solution = f"Mean = (sum of all values) ÷ (number of values) = ({sum(data)}) ÷ {len(data)} = {mean}"
            answer = mean
        
        elif stat_type == 'median':
            # Create data where finding the median is straightforward
            base = random.randint(5, 20)
            spread = random.randint(1, 10)
            data = [base + random.randint(-spread, spread) for _ in range(data_size)]
            data.sort()  # Sort for easier verification
            
            # Find the median
            if len(data) % 2 == 0:  # Even number of elements
                median = (data[len(data)//2 - 1] + data[len(data)//2]) / 2
            else:  # Odd number of elements
                median = data[len(data)//2]
            
            # Shuffle for presentation
            random.shuffle(data)
            
            data_str = ", ".join(map(str, data))
            question = f"What is the median of the following numbers: {data_str}?"
            
            sorted_data_str = ", ".join(map(str, sorted(data)))
            if len(data) % 2 == 0:  # Even number of elements
                middle1 = len(data)//2 - 1
                middle2 = len(data)//2
                solution = f"First, arrange the numbers in ascending order: {sorted_data_str}\nFor an even number of values, the median is the average of the two middle values.\nMedian = ({sorted(data)[middle1]} + {sorted(data)[middle2]}) ÷ 2 = {median}"
            else:  # Odd number of elements
                middle = len(data)//2
                solution = f"First, arrange the numbers in ascending order: {sorted_data_str}\nFor an odd number of values, the median is the middle value.\nMedian = {sorted(data)[middle]}"
            
            answer = median
        
        else:  # mode
            # Create data with a clear mode
            base_values = [random.randint(1, 20) for _ in range(data_size-2)]
            mode_value = random.randint(1, 20)
            while mode_value in base_values:
                mode_value = random.randint(1, 20)
            
            # Add the mode value twice to ensure it's the most frequent
            data = base_values + [mode_value, mode_value]
            random.shuffle(data)
            
            data_str = ", ".join(map(str, data))
            question = f"What is the mode of the following numbers: {data_str}?"
            
            # Count frequencies
            freq = {}
            for value in data:
                if value in freq:
                    freq[value] += 1
                else:
                    freq[value] = 1
            
            mode_count = freq[mode_value]
            solution = f"The mode is the value that appears most frequently.\nCounting the frequencies:\n"
            for value, count in freq.items():
                solution += f"{value} appears {count} time(s)\n"
            solution += f"Therefore, {mode_value} is the mode with {mode_count} occurrences."
            
            answer = mode_value
    
    elif difficulty == 'medium':
        # Range, variance, or probability
        stat_type = random.choice(['range', 'variance', 'probability'])
        
        if stat_type == 'range':
            # Generate data for range calculation
            data_size = random.randint(6, 10)
            min_val = random.randint(1, 20)
            max_val = min_val + random.randint(15, 30)
            
            data = [random.randint(min_val+1, max_val-1) for _ in range(data_size-2)]
            data += [min_val, max_val]  # Add the min and max values
            random.shuffle(data)
            
            range_val = max_val - min_val
            
            data_str = ", ".join(map(str, data))
            question = f"What is the range of the following dataset: {data_str}?"
            solution = f"Range = maximum value - minimum value = {max_val} - {min_val} = {range_val}"
            answer = range_val
        
        elif stat_type == 'variance':
            # Generate data for simple variance calculation
            data_size = random.randint(4, 6)  # Keep it small for simpler calculations
            mean = random.randint(5, 15)
            
            # Create data with integer deviations for easier calculations
            deviations = [random.randint(-5, 5) for _ in range(data_size)]
            while sum(deviations) != 0:  # Ensure the deviations sum to zero to maintain the chosen mean
                deviations[-1] = -sum(deviations[:-1])
            
            data = [mean + d for d in deviations]
            
            # Calculate variance manually
            squared_deviations = [(x - mean) ** 2 for x in data]
            variance = sum(squared_deviations) / len(data)
            
            data_str = ", ".join(map(str, data))
            question = f"What is the variance of the following dataset: {data_str}? (Round to two decimal places)"
            
            solution = f"Step 1: Find the mean: ({' + '.join(map(str, data))}) ÷ {len(data)} = {mean}\n\n"
            solution += "Step 2: Find the squared deviations from the mean:\n"
            
            for i, x in enumerate(data):
                solution += f"(x₍{i+1}₎ - mean)² = ({x} - {mean})² = {x-mean}² = {(x-mean)**2}\n"
            
            solution += f"\nStep 3: Find the average of the squared deviations:\nVariance = ({' + '.join(map(str, squared_deviations))}) ÷ {len(data)} = {sum(squared_deviations)} ÷ {len(data)} = {variance:.2f}"
            
            answer = round(variance, 2)
        
        else:  # probability
            # Simple probability problems
            prob_type = random.choice(['dice', 'cards', 'marbles'])
            
            if prob_type == 'dice':
                # Probability with dice
                dice_count = random.randint(1, 2)
                
                if dice_count == 1:
                    # Single die problems
                    target = random.choice(['even', 'odd', 'specific', 'range'])
                    
                    if target == 'even':
                        favorable = 3  # 2, 4, 6
                        question = "What is the probability of rolling an even number on a standard six-sided die?"
                        solution = "Favorable outcomes: 2, 4, 6 (3 outcomes)\nTotal possible outcomes: 1, 2, 3, 4, 5, 6 (6 outcomes)\nProbability = 3/6 = 1/2"
                        answer = "1/2"
                    
                    elif target == 'odd':
                        favorable = 3  # 1, 3, 5
                        question = "What is the probability of rolling an odd number on a standard six-sided die?"
                        solution = "Favorable outcomes: 1, 3, 5 (3 outcomes)\nTotal possible outcomes: 1, 2, 3, 4, 5, 6 (6 outcomes)\nProbability = 3/6 = 1/2"
                        answer = "1/2"
                    
                    elif target == 'specific':
                        value = random.randint(1, 6)
                        favorable = 1
                        question = f"What is the probability of rolling a {value} on a standard six-sided die?"
                        solution = f"Favorable outcomes: {value} (1 outcome)\nTotal possible outcomes: 1, 2, 3, 4, 5, 6 (6 outcomes)\nProbability = 1/6"
                        answer = "1/6"
                    
                    else:  # range
                        lower = random.randint(1, 3)
                        upper = random.randint(lower+1, 6)
                        favorable = upper - lower + 1
                        
                        question = f"What is the probability of rolling a number between {lower} and {upper} (inclusive) on a standard six-sided die?"
                        solution = f"Favorable outcomes: {', '.join(map(str, range(lower, upper+1)))} ({favorable} outcomes)\nTotal possible outcomes: 1, 2, 3, 4, 5, 6 (6 outcomes)\nProbability = {favorable}/6"
                        
                        # Simplify the fraction if possible
                        gcd = sp.gcd(favorable, 6)
                        if gcd > 1:
                            answer = f"{favorable//gcd}/{6//gcd}"
                        else:
                            answer = f"{favorable}/6"
                
                else:  # two dice
                    # Sum of two dice
                    target_sum = random.randint(2, 12)
                    
                    # Calculate favorable outcomes
                    favorable = 0
                    for i in range(1, 7):
                        for j in range(1, 7):
                            if i + j == target_sum:
                                favorable += 1
                    
                    question = f"What is the probability of rolling a sum of {target_sum} when rolling two standard six-sided dice?"
                    
                    solution = f"When rolling two dice, there are 6 × 6 = 36 possible outcomes.\nFavorable outcomes (sum = {target_sum}):\n"
                    
                    for i in range(1, 7):
                        for j in range(1, 7):
                            if i + j == target_sum:
                                solution += f"({i}, {j}) "
                    
                    solution += f"\nTotal favorable outcomes: {favorable}\nProbability = {favorable}/36"
                    
                    # Simplify the fraction if possible
                    gcd = sp.gcd(favorable, 36)
                    if gcd > 1:
                        answer = f"{favorable//gcd}/{36//gcd}"
                    else:
                        answer = f"{favorable}/36"
            
            elif prob_type == 'cards':
                # Probability with a standard deck of cards
                card_type = random.choice(['suit', 'face_card', 'value'])
                
                if card_type == 'suit':
                    suit = random.choice(['hearts', 'diamonds', 'clubs', 'spades'])
                    question = f"What is the probability of drawing a {suit} from a standard deck of 52 cards?"
                    solution = f"A standard deck has 13 {suit}.\nTotal number of cards = 52\nProbability = 13/52 = 1/4"
                    answer = "1/4"
                
                elif card_type == 'face_card':
                    question = "What is the probability of drawing a face card (jack, queen, or king) from a standard deck of 52 cards?"
                    solution = "There are 4 jacks, 4 queens, and 4 kings in a standard deck, for a total of 12 face cards.\nTotal number of cards = 52\nProbability = 12/52 = 3/13"
                    answer = "3/13"
                
                else:  # value
                    value = random.choice(['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
                    question = f"What is the probability of drawing a {value} from a standard deck of 52 cards?"
                    solution = f"There are 4 {value}s in a standard deck.\nTotal number of cards = 52\nProbability = 4/52 = 1/13"
                    answer = "1/13"
            
            else:  # marbles
                # Probability with marbles in a bag
                red = random.randint(2, 8)
                blue = random.randint(2, 8)
                green = random.randint(2, 8)
                total = red + blue + green
                
                color = random.choice(['red', 'blue', 'green'])
                if color == 'red':
                    favorable = red
                elif color == 'blue':
                    favorable = blue
                else:
                    favorable = green
                
                question = f"A bag contains {red} red marbles, {blue} blue marbles, and {green} green marbles. If you draw one marble at random, what is the probability of drawing a {color} marble?"
                solution = f"Number of {color} marbles = {favorable}\nTotal number of marbles = {red} + {blue} + {green} = {total}\nProbability = {favorable}/{total}"
                
                # Simplify the fraction if possible
                gcd = sp.gcd(favorable, total)
                if gcd > 1:
                    answer = f"{favorable//gcd}/{total//gcd}"
                else:
                    answer = f"{favorable}/{total}"
    
    else:  # hard
        # Standard deviation, normal distribution, or complex probability
        stat_type = random.choice(['std_dev', 'normal_dist', 'conditional_prob'])
        
        if stat_type == 'std_dev':
            # Generate data for standard deviation calculation
            data_size = random.randint(5, 7)  # Keep it manageable
            mean = random.randint(10, 20)
            
            # Create data with integer deviations for easier calculations
            deviations = [random.randint(-6, 6) for _ in range(data_size)]
            while sum(deviations) != 0:  # Ensure the deviations sum to zero to maintain the chosen mean
                deviations[-1] = -sum(deviations[:-1])
            
            data = [mean + d for d in deviations]
            
            # Calculate variance and standard deviation
            squared_deviations = [(x - mean) ** 2 for x in data]
            variance = sum(squared_deviations) / len(data)
            std_dev = variance ** 0.5
            
            data_str = ", ".join(map(str, data))
            question = f"What is the standard deviation of the following dataset: {data_str}? (Round to two decimal places)"
            
            solution = f"Step 1: Find the mean: ({' + '.join(map(str, data))}) ÷ {len(data)} = {mean}\n\n"
            solution += "Step 2: Find the squared deviations from the mean:\n"
            
            for i, x in enumerate(data):
                solution += f"(x₍{i+1}₎ - mean)² = ({x} - {mean})² = {x-mean}² = {(x-mean)**2}\n"
            
            solution += f"\nStep 3: Find the average of the squared deviations (variance):\nVariance = ({' + '.join(map(str, squared_deviations))}) ÷ {len(data)} = {sum(squared_deviations)} ÷ {len(data)} = {variance:.4f}\n\n"
            solution += f"Step 4: Take the square root of the variance to find the standard deviation:\nStandard deviation = √{variance:.4f} = {std_dev:.2f}"
            
            answer = round(std_dev, 2)
        
        elif stat_type == 'normal_dist':
            # Problem involving normal distribution
            # Use Z-score for standard normal distribution
            
            mean = random.randint(60, 80)
            std_dev = random.randint(5, 15)
            
            value = mean + random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2]) * std_dev
            
            z_score = (value - mean) / std_dev
            
            # Common Z-score probabilities
            z_table = {
                -2.0: 0.0228,
                -1.5: 0.0668,
                -1.0: 0.1587,
                -0.5: 0.3085,
                0.0: 0.5000,
                0.5: 0.6915,
                1.0: 0.8413,
                1.5: 0.9332,
                2.0: 0.9772
            }
            
            operation = random.choice(['above', 'below'])
            
            if operation == 'above':
                probability = 1 - z_table[z_score]
                question = f"In a normal distribution with mean {mean} and standard deviation {std_dev}, what is the probability of a value being greater than {value}? (Round to four decimal places)"
                solution = f"Step 1: Find the Z-score:\nZ = (x - μ) ÷ σ = ({value} - {mean}) ÷ {std_dev} = {z_score}\n\nStep 2: Find the probability using the standard normal table:\nP(Z > {z_score}) = 1 - P(Z < {z_score}) = 1 - {z_table[z_score]} = {probability:.4f}"
            else:
                probability = z_table[z_score]
                question = f"In a normal distribution with mean {mean} and standard deviation {std_dev}, what is the probability of a value being less than {value}? (Round to four decimal places)"
                solution = f"Step 1: Find the Z-score:\nZ = (x - μ) ÷ σ = ({value} - {mean}) ÷ {std_dev} = {z_score}\n\nStep 2: Find the probability using the standard normal table:\nP(Z < {z_score}) = {probability:.4f}"
            
            answer = round(probability, 4)
        
        else:  # conditional_prob
            # Conditional probability problems
            
            # Create a problem about drawing cards without replacement
            card_problem = random.choice([True, False])
            
            if card_problem:
                # Drawing two cards from a deck without replacement
                first_condition = random.choice(['heart', 'face_card', 'red'])
                second_condition = random.choice(['heart', 'face_card', 'red'])
                
                # Calculate initial counts
                if first_condition == 'heart':
                    first_favorable = 13
                    first_desc = "a heart"
                elif first_condition == 'face_card':
                    first_favorable = 12  # J, Q, K
                    first_desc = "a face card (jack, queen, or king)"
                else:  # red
                    first_favorable = 26  # hearts and diamonds
                    first_desc = "a red card"
                
                # Calculate conditional counts
                if first_condition == second_condition:
                    # Drawing the same type twice
                    if first_condition == 'heart':
                        second_favorable = 12  # One less heart
                        second_desc = "another heart"
                    elif first_condition == 'face_card':
                        second_favorable = 11  # One less face card
                        second_desc = "another face card"
                    else:  # red
                        second_favorable = 25  # One less red card
                        second_desc = "another red card"
                    
                    total_remain = 51  # After drawing one card
                    
                    joint_prob_num = first_favorable * second_favorable
                    joint_prob_den = 52 * 51
                    
                elif second_condition == 'heart':
                    # If first condition is not heart
                    if first_condition == 'face_card':
                        # Face cards that are hearts: K, Q, J of hearts = 3
                        # Remaining hearts after drawing a face card: 10
                        second_favorable = 10 if first_favorable == 3 else 13
                        second_desc = "a heart"
                    else:  # red
                        # Hearts are a subset of red cards
                        # Remaining hearts after drawing a red card: 12
                        second_favorable = 12
                        second_desc = "a heart"
                
                elif second_condition == 'face_card':
                    # If first condition is not face card
                    if first_condition == 'heart':
                        # Face cards that are hearts: K, Q, J of hearts = 3
                        # Remaining face cards after drawing a heart: 9
                        second_favorable = 9 if first_favorable == 3 else 12
                        second_desc = "a face card"
                    else:  # red
                        # Face cards that are red: K, Q, J of hearts and diamonds = 6
                        # Remaining face cards after drawing a red card: 6
                        second_favorable = 6
                        second_desc = "a face card"
                
                else:  # second_condition == 'red'
                    # If first condition is not red
                    if first_condition == 'heart':
                        # Hearts are a subset of red cards
                        # Remaining red cards after drawing a heart: 25
                        second_favorable = 25
                        second_desc = "a red card"
                    else:  # face_card
                        # Face cards that are red: K, Q, J of hearts and diamonds = 6
                        # Remaining red cards after drawing a face card: 20
                        second_favorable = 20 if first_favorable == 6 else 26
                        second_desc = "a red card"
                
                total_remain = 51  # Total cards remaining after first draw
                
                # Calculate the conditional probability
                cond_prob = second_favorable / total_remain
                
                question = f"You draw two cards from a standard deck of 52 cards without replacement. If the first card is {first_desc}, what is the probability that the second card is {second_desc}?"
                solution = f"After drawing {first_desc}, there are {total_remain} cards left in the deck.\nOf these, {second_favorable} are {second_desc}.\nProbability = {second_favorable}/{total_remain}"
                
                # Simplify the fraction if possible
                gcd = sp.gcd(second_favorable, total_remain)
                if gcd > 1:
                    answer = f"{second_favorable//gcd}/{total_remain//gcd}"
                else:
                    answer = f"{second_favorable}/{total_remain}"
            
            else:
                # Disease testing problem (sensitivity and specificity)
                disease_prevalence = random.randint(1, 10) / 100  # 1% to 10%
                test_sensitivity = random.randint(85, 99) / 100    # 85% to 99%
                test_specificity = random.randint(90, 99) / 100    # 90% to 99%
                
                # Calculate probabilities
                p_disease = disease_prevalence
                p_no_disease = 1 - disease_prevalence
                p_positive_given_disease = test_sensitivity
                p_negative_given_no_disease = test_specificity
                p_positive_given_no_disease = 1 - test_specificity
                
                # Calculate positive predictive value (probability of disease given positive test)
                p_positive = p_positive_given_disease * p_disease + p_positive_given_no_disease * p_no_disease
                p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
                
                question = f"A disease affects {disease_prevalence*100:.1f}% of the population. A test for this disease has a sensitivity of {test_sensitivity*100:.1f}% (probability of a positive test if the person has the disease) and a specificity of {test_specificity*100:.1f}% (probability of a negative test if the person does not have the disease). If a person tests positive, what is the probability that they actually have the disease? (Round to four decimal places)"
                
                solution = "Using Bayes' theorem:\n"
                solution += "P(Disease|Positive) = [P(Positive|Disease) × P(Disease)] ÷ P(Positive)\n\n"
                solution += f"P(Disease) = {disease_prevalence:.4f}\n"
                solution += f"P(No Disease) = 1 - {disease_prevalence:.4f} = {p_no_disease:.4f}\n"
                solution += f"P(Positive|Disease) = {test_sensitivity:.4f} (sensitivity)\n"
                solution += f"P(Positive|No Disease) = 1 - {test_specificity:.4f} = {p_positive_given_no_disease:.4f} (1 - specificity)\n\n"
                solution += f"P(Positive) = P(Positive|Disease) × P(Disease) + P(Positive|No Disease) × P(No Disease)\n"
                solution += f"P(Positive) = {test_sensitivity:.4f} × {disease_prevalence:.4f} + {p_positive_given_no_disease:.4f} × {p_no_disease:.4f} = {p_positive:.4f}\n\n"
                solution += f"P(Disease|Positive) = ({test_sensitivity:.4f} × {disease_prevalence:.4f}) ÷ {p_positive:.4f} = {p_disease_given_positive:.4f}"
                
                answer = round(p_disease_given_positive, 4)
    
    return {
        'question': question,
        'answer': str(answer),
        'solution': solution
    }
