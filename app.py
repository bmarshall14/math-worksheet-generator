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
    """Generate math worksheets with randomized problems from a large bank"""
    
    def __init__(self):
        self.worksheet_count = 0
        self.answer_keys = []
        
        # Initialize problem banks for each standard
        self.integer_problems_bank = self._create_integer_bank()
        self.fraction_problems_bank = self._create_fraction_bank()
        self.decimal_problems_bank = self._create_decimal_bank()
        self.equation_problems_bank = self._create_equation_bank()
        self.percent_problems_bank = self._create_percent_bank()
        
        # Initialize riddle banks
        self.riddles_8_letter = self._create_8_letter_riddles()
        self.riddles_9_letter = self._create_9_letter_riddles()
        
    def _create_integer_bank(self):
        """Create a bank of integer addition/subtraction problems"""
        return [
            # Format: (problem, answer)
            ("-15 + 23", "8"),
            ("34 + (-42)", "-8"),
            ("-18 - (-13)", "-5"),
            ("27 - 38", "-11"),
            ("-9 + (-14)", "-23"),
            ("45 - (-7)", "52"),
            ("-31 + 19", "-12"),
            ("16 + (-16)", "0"),
            ("-25 + 15", "-10"),
            ("42 - 53", "-11"),
            ("-8 + (-12)", "-20"),
            ("35 - (-10)", "45"),
            ("-17 + 29", "12"),
            ("48 + (-48)", "0"),
            ("-22 - (-18)", "-4"),
            ("15 - 27", "-12"),
            ("-30 + 45", "15"),
            ("28 + (-35)", "-7"),
            ("-14 - 6", "-20"),
            ("50 - 65", "-15"),
            ("-7 + (-8)", "-15"),
            ("33 - (-12)", "45"),
            ("-19 + 11", "-8"),
            ("24 + (-31)", "-7"),
            ("-26 - (-26)", "0"),
            ("18 - 30", "-12"),
            ("-35 + 50", "15"),
            ("44 + (-52)", "-8"),
            ("-11 - 14", "-25"),
            ("37 - 48", "-11"),
            ("-28 + 28", "0"),
            ("22 - (-8)", "30"),
            ("-16 + 24", "8"),
            ("39 + (-47)", "-8"),
            ("-21 - (-16)", "-5"),
            ("29 - 40", "-11"),
            ("-13 + (-10)", "-23"),
            ("46 - (-6)", "52"),
            ("-32 + 20", "-12"),
            ("17 + (-17)", "0"),
        ]
    
    def _create_fraction_bank(self):
        """Create a bank of fraction problems"""
        return [
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
            ("1/2 + 1/3", "5/6"),
            ("3/4 - 1/3", "5/12"),
            ("2/5 + 3/10", "7/10"),
            ("3/4 - 2/3", "1/12"),
            ("1/6 + 1/4", "5/12"),
            ("5/6 - 1/4", "7/12"),
            ("3/8 + 1/4", "5/8"),
            ("2/3 - 1/4", "5/12"),
            ("1/5 + 3/10", "1/2"),
            ("7/8 - 1/2", "3/8"),
        ]
    
    def _create_decimal_bank(self):
        """Create a bank of decimal problems"""
        return [
            ("3.5 + 2.7", "6.2"),
            ("8.4 - 3.6", "4.8"),
            ("12.5 + 7.5", "20.0"),
            ("15.8 - 9.3", "6.5"),
            ("4.25 + 3.75", "8.0"),
            ("10.0 - 2.5", "7.5"),
            ("5.5 + 4.5", "10.0"),
            ("9.6 - 4.8", "4.8"),
            ("7.2 + 2.8", "10.0"),
            ("14.5 - 6.5", "8.0"),
            ("3.3 + 4.7", "8.0"),
            ("11.9 - 5.4", "6.5"),
            ("6.25 + 1.75", "8.0"),
            ("9.0 - 4.5", "4.5"),
            ("2.4 + 5.6", "8.0"),
            ("13.7 - 8.2", "5.5"),
            ("4.5 + 3.5", "8.0"),
            ("16.4 - 9.8", "6.6"),
            ("5.75 + 2.25", "8.0"),
            ("12.0 - 7.5", "4.5"),
            ("8.8 + 1.2", "10.0"),
            ("15.5 - 7.5", "8.0"),
            ("3.6 + 4.4", "8.0"),
            ("10.8 - 5.3", "5.5"),
            ("7.25 + 0.75", "8.0"),
            ("14.0 - 6.0", "8.0"),
            ("2.5 + 7.5", "10.0"),
            ("11.6 - 3.6", "8.0"),
            ("4.4 + 5.6", "10.0"),
            ("18.9 - 10.9", "8.0"),
            ("6.5 + 3.5", "10.0"),
            ("17.2 - 9.2", "8.0"),
            ("1.9 + 6.1", "8.0"),
            ("9.9 - 4.4", "5.5"),
            ("5.25 + 4.75", "10.0"),
            ("13.3 - 5.3", "8.0"),
            ("3.8 + 6.2", "10.0"),
            ("15.7 - 7.7", "8.0"),
            ("7.5 + 2.5", "10.0"),
            ("16.0 - 8.0", "8.0"),
        ]
    
    def _create_equation_bank(self):
        """Create a bank of one-step equation problems"""
        return [
            ("x + 5 = 12", "7"),
            ("x - 3 = 8", "11"),
            ("2x = 16", "8"),
            ("x/4 = 3", "12"),
            ("x + 9 = 15", "6"),
            ("3x = 27", "9"),
            ("x - 7 = -2", "5"),
            ("x/2 = 4", "8"),
            ("x + 8 = 20", "12"),
            ("x - 5 = 10", "15"),
            ("4x = 32", "8"),
            ("x/3 = 5", "15"),
            ("x + 11 = 18", "7"),
            ("x - 9 = 3", "12"),
            ("5x = 45", "9"),
            ("x/6 = 2", "12"),
            ("x + 7 = 13", "6"),
            ("x - 4 = 11", "15"),
            ("6x = 42", "7"),
            ("x/5 = 3", "15"),
            ("x + 10 = 25", "15"),
            ("x - 8 = 7", "15"),
            ("7x = 56", "8"),
            ("x/8 = 2", "16"),
            ("x + 13 = 20", "7"),
            ("x - 6 = 9", "15"),
            ("8x = 64", "8"),
            ("x/7 = 2", "14"),
            ("x + 4 = 10", "6"),
            ("x - 10 = 5", "15"),
            ("9x = 72", "8"),
            ("x/9 = 1", "9"),
            ("x + 15 = 30", "15"),
            ("x - 12 = 0", "12"),
            ("10x = 80", "8"),
            ("x/10 = 2", "20"),
            ("x + 3 = 18", "15"),
            ("x - 2 = 13", "15"),
            ("2x = 30", "15"),
            ("x/4 = 4", "16"),
        ]
    
    def _create_percent_bank(self):
        """Create a bank of percent problems"""
        return [
            ("50% of 80", "40"),
            ("25% of 120", "30"),
            ("10% of 350", "35"),
            ("75% of 40", "30"),
            ("20% of 150", "30"),
            ("100% of 45", "45"),
            ("30% of 200", "60"),
            ("5% of 100", "5"),
            ("50% of 60", "30"),
            ("25% of 80", "20"),
            ("10% of 200", "20"),
            ("75% of 60", "45"),
            ("20% of 100", "20"),
            ("100% of 75", "75"),
            ("30% of 100", "30"),
            ("5% of 200", "10"),
            ("50% of 100", "50"),
            ("25% of 160", "40"),
            ("10% of 450", "45"),
            ("75% of 80", "60"),
            ("20% of 200", "40"),
            ("100% of 35", "35"),
            ("30% of 150", "45"),
            ("5% of 300", "15"),
            ("50% of 90", "45"),
            ("25% of 200", "50"),
            ("10% of 300", "30"),
            ("75% of 100", "75"),
            ("20% of 250", "50"),
            ("100% of 60", "60"),
            ("40% of 100", "40"),
            ("60% of 50", "30"),
            ("15% of 200", "30"),
            ("80% of 50", "40"),
            ("90% of 100", "90"),
            ("35% of 100", "35"),
            ("45% of 100", "45"),
            ("55% of 100", "55"),
            ("65% of 100", "65"),
            ("85% of 100", "85"),
        ]
    
    def _create_8_letter_riddles(self):
        """Create riddles with 8-letter answers"""
        return [
            ("I have branches but no fruit, trunk, or leaves. What am I?", "LIBRARY!"),
            ("What gets wet while drying?", "TOWELING"),
            ("I have keys but no locks, space but no room. What am I?", "KEYBOARD"),
            ("I disappear as soon as you say my name. What am I?", "SILENCES"),
            ("What can run but never walks, has a mouth but never talks?", "RIVERBED"),
            ("What has a face and two hands but no arms or legs?", "CLOCKING"),
            ("I'm tall when I'm young, short when I'm old. What am I?", "CANDLES!"),
            ("What has many teeth but cannot bite?", "HAIRCOM"),
            ("What can travel around the world while staying in a corner?", "POSTAGES"),
            ("I have cities but no houses, water but no fish. What am I?", "ROADMAPS"),
            ("What breaks but never falls, and falls but never breaks?", "DAYNIGHT"),
            ("The more you take, the more you leave behind. What am I?", "FOOTSTEP"),
            ("What has a head, a tail, is brown, and has no legs?", "PENNIES!"),
            ("What comes once in a minute, twice in a moment, never in a thousand years?", "LETTER-M"),
            ("What has an eye but cannot see?", "NEEDLES!"),
            ("I'm light as a feather, yet the strongest can't hold me for long. What am I?", "BREATHES"),
            ("What can fill a room but takes up no space?", "LIGHTING"),
            ("Forward I'm heavy, backward I'm not. What am I?", "TONWEIGHT"),
            ("What begins with T, ends with T, and has T in it?", "TEAPOTS!"),
            ("What gets bigger the more you take away?", "HOLEDIGS"),
        ]
    
    def _create_9_letter_riddles(self):
        """Create riddles with 9-letter answers"""
        return [
            ("What has many rings but no fingers?", "TELEPHONE"),
            ("I speak without a mouth and hear without ears. What am I?", "ECHOSOUNG"),
            ("What building has the most stories?", "LIBRARIES"),
            ("I fly without wings, I cry without eyes. What am I?", "CLOUDRAIN"),
            ("What can you catch but not throw?", "COLDVIRUS"),
            ("I have no life, but I can die. What am I?", "BATTERIES"),
            ("What has words but never speaks?", "BOOKSHELF"),
            ("The more there is, the less you see. What is it?", "DARKNIGHT"),
            ("What has a neck but no head?", "BOTTLEJAR"),
            ("I'm always in front of you but can't be seen. What am I?", "TOMORROW!"),
        ]
    
    def _assign_letters_to_problems(self, problems, riddle_answer):
        """Assign letters from the riddle answer to problems"""
        result = []
        # Remove special characters from riddle answer for letter assignment
        letters = [c for c in riddle_answer if c.isalpha()]
        
        for i, (problem, answer) in enumerate(problems[:len(letters)]):
            result.append((problem, answer, letters[i]))
        
        return result
    
    def create_worksheet_from_bank(self, standard_type, worksheet_num=1):
        """Create a worksheet by randomly selecting from the problem bank"""
        
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
        
        # Randomly select a riddle (8 or 9 problems based on riddle length)
        if random.choice([True, False]):
            riddle, riddle_answer = random.choice(self.riddles_8_letter)
            selected_problems = problem_bank[:8]
        else:
            riddle, riddle_answer = random.choice(self.riddles_9_letter)
            selected_problems = problem_bank[:9]
        
        # Assign letters to problems
        problems_with_letters = self._assign_letters_to_problems(selected_problems, riddle_answer)
        
        # Create the worksheet
        self._create_worksheet(filename, title, problems_with_letters, riddle, riddle_answer)
        
        return filename
    
    def _create_worksheet(self, filename, title, problems, riddle, riddle_answer):
        """Generic worksheet creator"""
        print(f"Creating worksheet: {filename}")
        
        c = canvas.Canvas(filename, pagesize=pagesizes.letter)
        width, height = pagesizes.letter
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, f"MATH WORKSHEET - {title}")
        
        # Riddle
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 90, f"RIDDLE: {riddle}")
        
        c.setFont("Helvetica", 11)
        c.drawString(50, height - 110, "Solve each problem. Find your answer in the Answer Bank.")
        c.drawString(50, height - 125, "Write the corresponding letter. The letters spell the riddle answer!")
        
        # Draw problems
        c.setFont("Helvetica", 12)
        y_position = height - 160
        
        for i, (problem, answer, letter) in enumerate(problems, 1):
            c.drawString(50, y_position, f"{i}.")
            c.drawString(70, y_position, f"{problem} = __________")
            c.drawString(350, y_position, "Letter: _____")
            y_position -= 35
        
        # Answer Bank Box
        c.setFont("Helvetica-Bold", 14)
        c.rect(40, y_position - 120, 530, 100)
        c.drawString(50, y_position - 20, "ANSWER BANK:")
        
        # Create answer bank with answers plus decoys
        c.setFont("Helvetica", 11)
        answer_bank = {}
        
        # Add real answers
        for problem, answer, letter in problems:
            answer_bank[answer] = letter
            
        # Add some decoy answers
        decoys = self._get_decoys(title)
        for decoy_answer, decoy_letter in decoys.items():
            if decoy_answer not in answer_bank:
                answer_bank[decoy_answer] = decoy_letter
        
        # Shuffle answer bank for display
        answer_items = list(answer_bank.items())
        random.shuffle(answer_items)
        
        # Draw answer bank
        y_position -= 45
        x_position = 50
        count = 0
        
        for answer, letter in answer_items:
            c.drawString(x_position, y_position, f"{answer} → {letter}")
            x_position += 65
            count += 1
            if count % 8 == 0:
                x_position = 50
                y_position -= 20
        
        # Riddle answer spaces
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position - 50, "RIDDLE ANSWER:")
        c.setFont("Helvetica", 20)
        spaces = "  ".join(["___"] * len([c for c in riddle_answer if c.isalpha()]))
        c.drawString(180, y_position - 50, spaces)
        
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
            decoys = [str(random.randint(-30, 30)) for _ in range(8)]
            letters = ["M", "Q", "V", "W", "X", "Z", "J", "F"]
        elif "Fraction" in title:
            decoys = ["1/8", "3/8", "7/8", "1", "2/5", "3/5", "1/10", "9/10"]
            letters = ["X", "Y", "Z", "W", "Q", "V", "J", "F"]
        elif "Decimal" in title:
            decoys = ["3.5", "8.5", "12.0", "5.0", "15.5", "2.5", "9.5", "11.0"]
            letters = ["X", "Y", "Z", "W", "Q", "V", "J", "F"]
        elif "Equation" in title:
            decoys = ["10", "15", "4", "20", "3", "13", "18", "25"]
            letters = ["X", "Y", "Z", "W", "Q", "V", "J", "F"]
        elif "Percent" in title:
            decoys = ["25", "50", "75", "20", "10", "15", "55", "65"]
            letters = ["X", "Y", "Z", "W", "Q", "V", "J", "F"]
        else:
            decoys = ["1", "2", "3", "4", "5", "6", "7", "8"]
            letters = ["X", "Y", "Z", "W", "Q", "V", "J", "F"]
        
        return dict(zip(decoys, letters))
    
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
            
            # Problems and answers
            c.setFont("Helvetica", 10)
            for i, (problem, answer, letter) in enumerate(sheet['problems'], 1):
                c.drawString(70, y_position, f"{i}. {problem} = {answer} (Letter: {letter})")
                y_position -= 18
                
                # Check if we need a new page
                if y_position < 100:
                    c.showPage()
                    y_position = height - 50
                    
            # Riddle answer
            c.setFont("Helvetica-Bold", 11)
            c.drawString(70, y_position, f"RIDDLE ANSWER: {sheet['riddle_answer']}")
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
st.set_page_config(page_title="Math Worksheet Generator", page_icon="📐")

st.title("📐 Math Worksheet Generator")
st.markdown("Generate unique math worksheets with randomized problems and riddles!")

# Worksheet selection
st.subheader("Generate Worksheets")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Select Standards")
    integers = st.checkbox("Integer Operations", value=True)
    fractions = st.checkbox("Fractions")
    decimals = st.checkbox("Decimals")
    equations = st.checkbox("One-Step Equations")
    percents = st.checkbox("Percents")

with col2:
    st.markdown("### Number of Versions")
    st.info("Generate multiple unique versions of each worksheet!")
    num_versions = st.number_input(
        "Versions per standard",
        min_value=1,
        max_value=10,
        value=3,
        help="Each version will have different problems and riddles"
    )

# Options
st.subheader("Additional Options")
generate_answer_key = st.checkbox("Generate Answer Key PDF", value=True)

# Show preview of available content
with st.expander("📚 See Available Content"):
    st.markdown("""
    **Problem Banks:**
    - Integer Operations: 40 unique problems
    - Fractions: 40 unique problems
    - Decimals: 40 unique problems
    - Equations: 40 unique problems
    - Percents: 40 unique problems
    
    **Riddle Bank:**
    - 20 riddles with 8-letter answers
    - 10 riddles with 9-letter answers
    
    Each worksheet randomly selects 8-9 problems and a riddle, 
    making every generated worksheet unique!
    """)

# Generate button
if st.button("🎲 Generate Random Worksheets", type="primary"):
    with st.spinner("Generating unique worksheets..."):
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
        
        # Generate multiple versions of each selected standard
        for standard in standards_to_generate:
            for version in range(1, num_versions + 1):
                filename = generator.create_worksheet_from_bank(standard, version)
                if filename:
                    generated_files.append(filename)
        
        # Generate answer key
        if generate_answer_key:
            generator.create_answer_key()
            generated_files.append("answer_key_all.pdf")
        
        # Create zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for file in generated_files:
                if os.path.exists(file):
                    zip_file.write(file)
        
        # Show success message with details
        st.success(f"""
        ✅ Successfully generated {len(generated_files)-1 if generate_answer_key else len(generated_files)} unique worksheets!
        
        Each worksheet contains:
        - Randomly selected problems from the bank
        - A random riddle to solve
        - Unique problem combinations
        """)
        
        # Offer download
        st.download_button(
            label=f"📥 Download All Files ({len(generated_files)} files)",
            data=zip_buffer.getvalue(),
            file_name=f"math_worksheets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip"
        )

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    ### Features:
    - **Randomized Problems**: Each worksheet pulls from a bank of 40+ problems per standard
    - **Random Riddles**: 30+ different riddles that students solve using their answers
    - **Multiple Versions**: Generate up to 10 unique versions of each worksheet type
    - **Answer Keys**: Comprehensive answer key includes all generated worksheets
    
    ### Steps:
    1. **Select standards** you want to generate worksheets for
    2. **Choose number of versions** (each will be unique!)
    3. **Click Generate** to create your randomized worksheets
    4. **Download the ZIP** file containing all materials
    
    ### Perfect for:
    - Differentiated instruction (different worksheet for each student)
    - Make-up tests and retakes
    - Extra practice with variety
    - Preventing copying between students
    """)

st.markdown("---")
st.caption("Each time you generate worksheets, you'll get completely different problem combinations and riddles!")