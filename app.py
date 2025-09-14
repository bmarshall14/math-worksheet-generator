# app.py
import streamlit as st
import os
import zipfile
import io
import random
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
import csv

class MathWorksheetGenerator:
    """Generate math worksheets with customizable problem counts and matching riddles"""
    
    def __init__(self):
        self.worksheet_count = 0
        self.answer_keys = []
        
        # Initialize problem banks for each standard
        self.integer_problems_bank = self._create_integer_bank()
        self.fraction_problems_bank = self._create_fraction_bank()
        self.decimal_problems_bank = self._create_decimal_bank()
        self.equation_problems_bank = self._create_equation_bank()
        self.percent_problems_bank = self._create_percent_bank()
        
        # Initialize riddle banks by answer length
        self.riddle_bank = self._create_riddle_bank()
        
    def _create_integer_bank(self):
        """Create a bank of integer addition/subtraction problems"""
        problems = []
        # Generate a large set of integer problems
        for _ in range(100):
            a = random.randint(-50, 50)
            b = random.randint(-50, 50)
            operation = random.choice(['+', '-'])
            
            if operation == '+':
                if b < 0:
                    problem = f"{a} + ({b})"
                else:
                    problem = f"{a} + {b}"
                answer = str(a + b)
            else:
                if b < 0:
                    problem = f"{a} - ({b})"
                else:
                    problem = f"{a} - {b}"
                answer = str(a - b)
            
            problems.append((problem, answer))
        
        # Add some specific curated problems
        problems.extend([
            ("-15 + 23", "8"),
            ("34 + (-42)", "-8"),
            ("-18 - (-13)", "-5"),
            ("27 - 38", "-11"),
            ("-9 + (-14)", "-23"),
            ("45 - (-7)", "52"),
            ("-31 + 19", "-12"),
            ("16 + (-16)", "0"),
        ])
        
        return problems
    
    def _create_fraction_bank(self):
        """Create a bank of fraction problems"""
        problems = [
            ("1/2 + 1/4", "3/4"),
            ("3/4 - 1/2", "1/4"),
            ("2/3 + 1/6", "5/6"),
            ("5/6 - 1/3", "1/2"),
            ("1/4 + 3/8", "5/8"),
            ("7/8 - 1/4", "5/8"),
            ("1/3 + 1/3", "2/3"),
            ("3/4 - 1/4", "1/2"),
            ("1/8 + 1/8", "1/4"),
            ("2/3 - 1/6", "1/2"),
            ("1/2 + 1/6", "2/3"),
            ("5/8 - 1/8", "1/2"),
            ("1/4 + 1/4", "1/2"),
            ("3/4 - 1/8", "5/8"),
            ("1/3 + 1/6", "1/2"),
            ("7/8 - 3/8", "1/2"),
            ("1/5 + 2/5", "3/5"),
            ("4/5 - 1/5", "3/5"),
            ("1/2 + 1/8", "5/8"),
            ("2/3 - 1/3", "1/3"),
            ("3/8 + 3/8", "3/4"),
            ("5/6 - 1/6", "2/3"),
            ("1/4 + 1/8", "3/8"),
            ("3/4 - 3/8", "3/8"),
            ("2/5 + 1/5", "3/5"),
            ("4/5 - 2/5", "2/5"),
            ("1/6 + 1/6", "1/3"),
            ("5/8 - 1/4", "3/8"),
            ("1/3 + 2/3", "1"),
            ("1 - 1/4", "3/4"),
        ]
        
        # Generate more fraction problems
        denominators = [2, 3, 4, 5, 6, 8, 10, 12]
        for _ in range(50):
            d1 = random.choice(denominators)
            d2 = random.choice(denominators)
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            
            # Simple same denominator problems
            if d1 == d2:
                if random.choice([True, False]):
                    result_n = n1 + n2
                    if result_n < d1:
                        problems.append((f"{n1}/{d1} + {n2}/{d2}", f"{result_n}/{d1}"))
                else:
                    if n1 > n2:
                        problems.append((f"{n1}/{d1} - {n2}/{d2}", f"{n1-n2}/{d1}"))
        
        return problems
    
    def _create_decimal_bank(self):
        """Create a bank of decimal problems"""
        problems = []
        
        # Generate decimal problems
        for _ in range(100):
            a = round(random.uniform(0, 20), 1)
            b = round(random.uniform(0, 20), 1)
            
            if random.choice([True, False]):
                answer = round(a + b, 1)
                problems.append((f"{a} + {b}", str(answer)))
            else:
                if a >= b:
                    answer = round(a - b, 1)
                    problems.append((f"{a} - {b}", str(answer)))
        
        return problems
    
    def _create_equation_bank(self):
        """Create a bank of one-step equation problems"""
        problems = []
        
        # Generate various equation types
        for _ in range(30):
            # Addition equations: x + a = b
            a = random.randint(1, 20)
            result = random.randint(5, 30)
            answer = result - a
            problems.append((f"x + {a} = {result}", str(answer)))
            
            # Subtraction equations: x - a = b
            a = random.randint(1, 15)
            result = random.randint(1, 20)
            answer = result + a
            problems.append((f"x - {a} = {result}", str(answer)))
            
            # Multiplication equations: ax = b
            a = random.randint(2, 12)
            answer = random.randint(1, 15)
            result = a * answer
            problems.append((f"{a}x = {result}", str(answer)))
            
            # Division equations: x/a = b
            a = random.randint(2, 10)
            result = random.randint(1, 15)
            answer = a * result
            problems.append((f"x/{a} = {result}", str(answer)))
        
        return problems
    
    def _create_percent_bank(self):
        """Create a bank of percent problems"""
        problems = []
        
        # Common percentages
        common_percents = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100]
        common_values = [20, 40, 50, 60, 80, 100, 120, 150, 200, 250, 300, 400, 500]
        
        for _ in range(100):
            percent = random.choice(common_percents)
            value = random.choice(common_values)
            answer = int(value * percent / 100)
            problems.append((f"{percent}% of {value}", str(answer)))
        
        return problems
    
    def _create_riddle_bank(self):
        """Create a comprehensive riddle bank organized by answer length"""
        riddle_bank = {}
        
        # Base riddles that can be extended with word combinations
        base_riddles = [
            # Nature & Weather
            ("What can run but never walks, has a mouth but never talks?", ["RIVER", "WATER"]),
            ("I fly without wings, I cry without eyes. What am I?", ["CLOUD", "STORM"]),
            ("What gets wet while drying?", ["TOWEL"]),
            ("I'm tall when young, short when old. What am I?", ["CANDLE"]),
            ("The more there is, the less you see. What is it?", ["DARKNESS", "FOG"]),
            
            # Objects & Tools
            ("What has keys but no locks, space but no room?", ["KEYBOARD"]),
            ("What has many teeth but cannot bite?", ["COMB", "SAW", "GEAR"]),
            ("What has a face and hands but no body?", ["CLOCK", "WATCH"]),
            ("What has an eye but cannot see?", ["NEEDLE", "STORM"]),
            ("What has a neck but no head?", ["BOTTLE"]),
            
            # Concepts & Abstract
            ("I disappear as soon as you say my name. What am I?", ["SILENCE"]),
            ("The more you take, the more you leave behind. What?", ["FOOTSTEPS", "STEPS"]),
            ("What breaks but never falls?", ["DAWN", "DAY"]),
            ("Forward I'm heavy, backward I'm not. What am I?", ["TON"]),
            ("What comes once in a minute, twice in a moment?", ["LETTER M", "M"]),
            
            # Places & Buildings
            ("What building has the most stories?", ["LIBRARY"]),
            ("I have cities but no houses, water but no fish. What am I?", ["MAP", "ATLAS"]),
            ("What room has no doors or windows?", ["MUSHROOM"]),
            
            # Food & Kitchen
            ("What begins with T, ends with T, and has T in it?", ["TEAPOT"]),
            ("I have branches but no fruit, trunk, or leaves. What am I?", ["BANK", "LIBRARY"]),
            
            # Actions & Movement
            ("What can travel around the world while staying in a corner?", ["STAMP"]),
            ("What can you catch but not throw?", ["COLD", "BREATH"]),
            ("What gets bigger the more you take away?", ["HOLE"]),
            ("What goes up but never comes down?", ["AGE", "TIME"]),
        ]
        
        # Generate riddles for different lengths (10-30)
        for length in range(10, 31):
            riddle_bank[length] = []
            
            # Method 1: Use exact length words/phrases
            for riddle_text, answers in base_riddles:
                for answer in answers:
                    if len(answer) == length:
                        riddle_bank[length].append((riddle_text, answer))
            
            # Method 2: Combine words to make longer answers
            if length >= 8:
                # Combine two related words
                combinations = [
                    ("What has keys but can't open locks, and space but no room?", "KEYBOARD", "COMPUTER"),
                    ("What gets wet while drying and hangs in your bathroom?", "BATH", "TOWEL"),
                    ("What flies without wings and cries without eyes?", "RAIN", "CLOUD"),
                    ("What building has stories and keeps knowledge?", "LIBRARY", "BOOKS"),
                    ("What can be cracked, made, told, and played?", "JOKE", "RIDDLE"),
                ]
                
                for riddle_text, word1, word2 in combinations:
                    combined = word1 + word2
                    if len(combined) == length:
                        riddle_bank[length].append((riddle_text, combined))
            
            # Method 3: Add descriptive phrases for longer answers
            if length >= 15:
                extended_riddles = [
                    (f"What has keys but no locks, space but no room, and you can enter but not go inside? (Think about what you're typing on)", "COMPUTER" + "KEYBOARD"[:length-8]),
                    (f"I have many pages but I'm not a book, I have many links but I'm not a chain. What am I?", "INTERNETWEBSITE"[:length]),
                    (f"I can be long or short, I can be grown or bought, I can be painted or left bare. What am I?", "FINGERNAILSHAND"[:length]),
                ]
                
                for riddle_text, answer in extended_riddles:
                    if len(answer) <= length:
                        # Pad with exclamation marks or repeated letters if needed
                        while len(answer) < length:
                            answer += "!"
                        riddle_bank[length].append((riddle_text, answer[:length]))
            
            # Method 4: Create number/letter pattern riddles for any length
            if len(riddle_bank[length]) == 0:
                # Fallback riddles that work for any length
                alphabet_riddle = f"What comes after {'A' * (length-1)}?", "A" * (length-1) + "B"
                counting_riddle = f"Count from 1 to {length}. What do you get?", "".join([str(i%10) for i in range(1, length+1)])
                pattern_riddle = f"Complete the pattern: {'AB' * (length//2)}", "AB" * (length//2) + ("A" if length % 2 else "")
                
                riddle_bank[length].extend([
                    (alphabet_riddle[0], alphabet_riddle[1]),
                    (counting_riddle[0], counting_riddle[1]),
                    (pattern_riddle[0], pattern_riddle[1]),
                ])
        
        return riddle_bank
    
    def _get_riddle_for_length(self, length):
        """Get or generate a riddle with an answer of specific length"""
        if length in self.riddle_bank and self.riddle_bank[length]:
            return random.choice(self.riddle_bank[length])
        else:
            # Generate a simple pattern riddle as fallback
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            answer = ""
            for i in range(length):
                answer += letters[i % 26]
            
            riddle = f"What word has {length} letters and follows the alphabet?"
            return (riddle, answer)
    
    def _assign_letters_to_problems(self, problems, riddle_answer):
        """Assign letters from the riddle answer to problems"""
        result = []
        # Remove special characters from riddle answer for letter assignment
        letters = [c for c in riddle_answer if c.isalpha() or c in "!?.,"]
        
        for i, (problem, answer) in enumerate(problems[:len(letters)]):
            result.append((problem, answer, letters[i]))
        
        return result
    
    def create_worksheet_from_bank(self, standard_type, num_problems, worksheet_num=1):
        """Create a worksheet with specified number of problems"""
        
        # Select problem bank and worksheet title based on standard
        if standard_type == "integers":
            problem_bank = self.integer_problems_bank.copy()
            title = "Adding & Subtracting Integers"
            filename = f"integer_operations_{worksheet_num}.pdf"
        elif standard_type == "fractions":
            problem_bank = self.fraction_problems_bank.copy()
            title = "Adding & Subtracting Fractions"
            filename = f"fractions_{worksheet_num}.pdf"
        elif standard_type == "decimals":
            problem_bank = self.decimal_problems_bank.copy()
            title = "Decimal Addition & Subtraction"
            filename = f"decimals_{worksheet_num}.pdf"
        elif standard_type == "equations":
            problem_bank = self.equation_problems_bank.copy()
            title = "Solving One-Step Equations"
            filename = f"equations_{worksheet_num}.pdf"
        elif standard_type == "percents":
            problem_bank = self.percent_problems_bank.copy()
            title = "Finding Percents"
            filename = f"percents_{worksheet_num}.pdf"
        else:
            return None
        
        # Randomly select problems
        random.shuffle(problem_bank)
        selected_problems = problem_bank[:num_problems]
        
        # Get a riddle with answer length matching number of problems
        riddle, riddle_answer = self._get_riddle_for_length(num_problems)
        
        # Assign letters to problems
        problems_with_letters = self._assign_letters_to_problems(selected_problems, riddle_answer)
        
        # Create the worksheet
        self._create_worksheet(filename, title, problems_with_letters, riddle, riddle_answer, num_problems)
        
        return filename
    
    def _create_worksheet(self, filename, title, problems, riddle, riddle_answer, num_problems):
        """Generic worksheet creator that handles variable number of problems"""
        print(f"Creating worksheet: {filename}")
        
        c = canvas.Canvas(filename, pagesize=pagesizes.letter)
        width, height = pagesizes.letter
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, f"MATH WORKSHEET - {title}")
        
        # Riddle
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 80, f"RIDDLE: {riddle}")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 100, "Solve each problem. Find your answer in the Answer Bank.")
        c.drawString(50, height - 115, "Write the corresponding letter. The letters spell the riddle answer!")
        
        # Calculate spacing based on number of problems
        if num_problems <= 15:
            problems_per_column = num_problems
            num_columns = 1
            y_spacing = 30
            start_y = height - 145
        elif num_problems <= 20:
            problems_per_column = num_problems
            num_columns = 1
            y_spacing = 25
            start_y = height - 145
        else:
            # For 21-30 problems, use two columns
            problems_per_column = (num_problems + 1) // 2
            num_columns = 2
            y_spacing = min(25, (height - 350) // problems_per_column)
            start_y = height - 145
        
        # Draw problems
        c.setFont("Helvetica", 10)
        
        for i, (problem, answer, letter) in enumerate(problems):
            if num_columns == 1:
                x_position = 50
                y_position = start_y - (i * y_spacing)
            else:
                # Two column layout
                column = i // problems_per_column
                row = i % problems_per_column
                x_position = 50 + (column * 280)
                y_position = start_y - (row * y_spacing)
            
            c.drawString(x_position, y_position, f"{i+1}.")
            c.drawString(x_position + 20, y_position, f"{problem} = _____")
            c.drawString(x_position + 180, y_position, "Letter: ___")
        
        # Answer Bank Position
        if num_problems <= 20:
            answer_bank_y = start_y - (num_problems * y_spacing) - 40
        else:
            answer_bank_y = start_y - (problems_per_column * y_spacing) - 40
        
        # Answer Bank Box
        c.setFont("Helvetica-Bold", 12)
        c.rect(40, answer_bank_y - 80, 530, 70)
        c.drawString(50, answer_bank_y - 15, "ANSWER BANK:")
        
        # Create answer bank with answers plus decoys
        c.setFont("Helvetica", 9)
        answer_bank = {}
        
        # Add real answers
        for problem, answer, letter in problems:
            answer_bank[answer] = letter
            
        # Add some decoy answers
        decoys = self._get_decoys(title)
        decoy_count = min(10, 30 - len(problems))  # Add fewer decoys for larger worksheets
        for decoy_answer, decoy_letter in list(decoys.items())[:decoy_count]:
            if decoy_answer not in answer_bank:
                answer_bank[decoy_answer] = decoy_letter
        
        # Shuffle and draw answer bank
        answer_items = list(answer_bank.items())
        random.shuffle(answer_items)
        
        y_position = answer_bank_y - 35
        x_position = 50
        count = 0
        items_per_row = 8 if len(answer_items) <= 16 else 10
        
        for answer, letter in answer_items:
            c.drawString(x_position, y_position, f"{answer}→{letter}")
            x_position += (520 // items_per_row)
            count += 1
            if count % items_per_row == 0:
                x_position = 50
                y_position -= 15
        
        # Riddle answer spaces
        c.setFont("Helvetica-Bold", 12)
        riddle_y = answer_bank_y - 110
        c.drawString(50, riddle_y, "RIDDLE ANSWER:")
        
        # Adjust spacing for answer blanks based on number of letters
        c.setFont("Helvetica", 14)
        if num_problems <= 15:
            spaces = "  ".join(["___"] * num_problems)
            c.drawString(160, riddle_y, spaces)
        else:
            # For longer answers, use two lines
            first_line = "  ".join(["___"] * 15)
            second_line = "  ".join(["___"] * (num_problems - 15))
            c.drawString(50, riddle_y - 20, first_line)
            c.drawString(50, riddle_y - 40, second_line)
        
        # Add footer
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 40, "Name: ________________________    Date: ____________    Period: _____")
        
        # Save
        c.save()
        print(f"✓ Created: {filename}")
        
        # Store for answer key
        self.answer_keys.append({
            'filename': filename,
            'title': title,
            'problems': problems,
            'riddle': riddle,
            'riddle_answer': riddle_answer
        })
        
        self.worksheet_count += 1
    
    def _get_decoys(self, title):
        """Get appropriate decoy answers based on worksheet type"""
        if "Integer" in title:
            decoys = {str(random.randint(-30, 30)): chr(65+i) for i in range(26)}
        elif "Fraction" in title:
            common_fractions = ["1/8", "3/8", "7/8", "1/5", "2/5", "3/5", "4/5", "1/10", "3/10", "7/10", "9/10", "1/12", "5/12", "7/12", "11/12"]
            decoys = {frac: chr(65+i) for i, frac in enumerate(common_fractions)}
        elif "Decimal" in title:
            decoys = {str(round(random.uniform(0, 20), 1)): chr(65+i) for i in range(26)}
        elif "Equation" in title:
            decoys = {str(random.randint(1, 30)): chr(65+i) for i in range(26)}
        elif "Percent" in title:
            decoys = {str(random.randint(5, 100)): chr(65+i) for i in range(26)}
        else:
            decoys = {str(i): chr(65+i) for i in range(26)}
        
        return decoys
    
    def create_answer_key(self, filename="answer_key_all.pdf"):
        """Create a comprehensive answer key PDF for all worksheets"""
        print(f"\nCreating comprehensive answer key: {filename}")
        
        c = canvas.Canvas(filename, pagesize=pagesizes.letter)
        width, height = pagesizes.letter
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "ANSWER KEY - ALL WORKSHEETS")
        
        y_position = height - 90
        
        for sheet in self.answer_keys:
            # Worksheet title
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, f"{sheet['title']} ({sheet['filename']})")
            y_position -= 20
            
            # Problems and answers - use smaller font for longer worksheets
            font_size = 10 if len(sheet['problems']) <= 20 else 9
            c.setFont("Helvetica", font_size)
            
            # For many problems, use two columns
            if len(sheet['problems']) > 15:
                problems_per_column = (len(sheet['problems']) + 1) // 2
                for i, (problem, answer, letter) in enumerate(sheet['problems']):
                    column = i // problems_per_column
                    row = i % problems_per_column
                    x = 70 + (column * 250)
                    y = y_position - (row * 15)
                    c.drawString(x, y, f"{i+1}. {problem} = {answer} ({letter})")
                y_position -= (problems_per_column * 15)
            else:
                for i, (problem, answer, letter) in enumerate(sheet['problems'], 1):
                    c.drawString(70, y_position, f"{i}. {problem} = {answer} (Letter: {letter})")
                    y_position -= 15
            
            # Check if we need a new page
            if y_position < 100:
                c.showPage()
                y_position = height - 50
                
            # Riddle answer
            c.setFont("Helvetica-Bold", 11)
            c.drawString(70, y_position - 10, f"RIDDLE ANSWER: {sheet['riddle_answer']}")
            y_position -= 30
            
            # Add separator
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.line(50, y_position, width - 50, y_position)
            y_position -= 20
            
            # Check if we need a new page
            if y_position < 150:
                c.showPage()
                y_position = height - 50
        
        c.save()
        print(f"✓ Answer key created: {filename}")

# Streamlit Interface
st.set_page_config(page_title="Math Worksheet Generator", page_icon="📐", layout="wide")

st.title("📐 Advanced Math Worksheet Generator")
st.markdown("Generate customizable math worksheets with riddles - choose your own problem count!")

# Main configuration in columns
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.markdown("### Select Standards")
    integers = st.checkbox("Integer Operations", value=True)
    fractions = st.checkbox("Fractions")
    decimals = st.checkbox("Decimals")
    equations = st.checkbox("One-Step Equations")
    percents = st.checkbox("Percents")

with col2:
    st.markdown("### Worksheet Configuration")
    
    # Number of problems per worksheet
    num_problems = st.slider(
        "Problems per worksheet",
        min_value=10,
        max_value=30,
        value=15,
        step=1,
        help="The riddle answer will have the same number of letters as problems!"
    )
    
    # Number of versions
    num_versions = st.number_input(
        "Versions per standard",
        min_value=1,
        max_value=10,
        value=3,
        help="Each version will have different problems and riddles"
    )

with col3:
    st.markdown("### Options")
    generate_answer_key = st.checkbox("Generate Answer Key", value=True)
    
    st.markdown("### Info")
    total_worksheets = sum([integers, fractions, decimals, equations, percents]) * num_versions
    st.info(f"Will generate: **{total_worksheets}** worksheets")

# Show preview of what will be generated
with st.expander("📚 Preview Your Configuration"):
    st.markdown(f"""
    **Your Settings:**
    - **{num_problems} problems** per worksheet
    - **{num_versions} unique versions** of each selected standard
    - Riddle answers will be **{num_problems} characters long**
    
    **Selected Standards:**
    {('- Integer Operations' if integers else '')}
    {('- Fractions' if fractions else '')}
    {('- Decimals' if decimals else '')}
    {('- One-Step Equations' if equations else '')}
    {('- Percents' if percents else '')}
    
    **What makes each worksheet unique:**
    - Randomly selected problems from large problem banks
    - Different riddle with {num_problems}-letter answer
    - Randomized answer bank arrangement
    """)

# Generate button
if st.button(f"🎲 Generate {total_worksheets} Worksheets", type="primary", disabled=(total_worksheets == 0)):
    if total_worksheets == 0:
        st.error("Please select at least one standard!")
    else:
        with st.spinner(f"Generating {total_worksheets} unique worksheets with {num_problems}-letter riddles..."):
            # Create generator
            generator = MathWorksheetGenerator()
            
            # Track generated files
            generated_files = []
            
            # Generate selected worksheets
            standards_to_generate = []
            if integers:
                standards_to_generate.append("integers")
            if fractions:
                standards_to_generate.append("fractions")
            if decimals:
                standards_to_generate.append("decimals")
            if equations:
                standards_to_generate.append("equations")
            if percents:
                standards_to_generate.append("percents")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Generate multiple versions of each selected standard
            total_generated = 0
            for standard in standards_to_generate:
                for version in range(1, num_versions + 1):
                    status_text.text(f"Generating {standard} worksheet {version}...")
                    filename = generator.create_worksheet_from_bank(standard, num_problems, version)
                    if filename:
                        generated_files.append(filename)
                    total_generated += 1
                    progress_bar.progress(total_generated / total_worksheets)
            
            # Generate answer key
            if generate_answer_key:
                status_text.text("Creating answer key...")
                generator.create_answer_key()
                generated_files.append("answer_key_all.pdf")
            
            progress_bar.progress(1.0)
            status_text.text("Creating ZIP file...")
            
            # Create zip file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for file in generated_files:
                    if os.path.exists(file):
                        zip_file.write(file)
                        os.remove(file)  # Clean up after adding to zip
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Show success message with details
            st.success(f"""
            ✅ Successfully generated {total_worksheets} unique worksheets!
            
            Each worksheet contains:
            - **{num_problems} problems** randomly selected from the bank
            - A riddle with a **{num_problems}-letter answer**
            - Unique problem combinations
            - Customized answer bank
            """)
            
            # Offer download
            st.download_button(
                label=f"📥 Download All Files ({len(generated_files)} files)",
                data=zip_buffer.getvalue(),
                file_name=f"math_worksheets_{num_problems}problems_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )

# Instructions and tips
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📖 How to Use
    1. **Select standards** you want to practice
    2. **Choose problem count** (10-30 per worksheet)
    3. **Set versions** (for differentiation)
    4. **Generate** and download your custom worksheets
    
    ### 🎯 Problem Count Guidelines
    - **10-12 problems**: Quick assessment, exit tickets
    - **15-18 problems**: Standard homework/classwork
    - **20-25 problems**: Comprehensive practice
    - **26-30 problems**: Challenge worksheets, tests
    """)

with col2:
    st.markdown("""
    ### ✨ Features
    - **Flexible Length**: 10-30 problems per worksheet
    - **Smart Riddles**: Answer length matches problem count
    - **Huge Problem Banks**: 100+ problems per standard
    - **True Randomization**: Every worksheet is unique
    - **Professional Layout**: Auto-adjusts for problem count
    
    ### 💡 Tips
    - Different problem counts prevent copying
    - Longer worksheets work great for group work
    - Use 10-problem sheets for quick warm-ups
    - 30-problem sheets for test preparation
    """)

st.caption("Each worksheet is dynamically generated with riddles that match your chosen problem count!")