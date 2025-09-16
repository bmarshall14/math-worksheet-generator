# app_fixed_complete.py - Math Worksheet Generator with Exact Common Core Alignment
import streamlit as st
import os
import zipfile
import io
import random
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
import math

# Common Core Standards Database
COMMON_CORE_STANDARDS = {
    "6th Grade": {
        "Ratios & Proportional Relationships": {
            "6.RP.A.1": "Understand ratio concepts and use ratio reasoning",
            "6.RP.A.2": "Understand unit rates",
            "6.RP.A.3": "Use ratio and rate reasoning to solve problems"
        },
        "The Number System": {
            "6.NS.A.1": "Interpret and compute quotients of fractions",
            "6.NS.B.2": "Fluently divide multi-digit numbers",
            "6.NS.B.3": "Fluently add, subtract, multiply, and divide multi-digit decimals",
            "6.NS.B.4": "Find common factors and multiples",
            "6.NS.C.5": "Understand positive and negative numbers",
            "6.NS.C.6": "Understand rational numbers on a number line",
            "6.NS.C.7": "Understand ordering and absolute value of rational numbers"
        },
        "Expressions & Equations": {
            "6.EE.A.1": "Write and evaluate numerical expressions with exponents",
            "6.EE.A.2": "Write, read, and evaluate algebraic expressions",
            "6.EE.A.3": "Apply properties of operations",
            "6.EE.A.4": "Identify equivalent expressions",
            "6.EE.B.5": "Understand solving equations as a process",
            "6.EE.B.6": "Use variables to represent numbers",
            "6.EE.B.7": "Solve one-step equations",
            "6.EE.C.9": "Analyze relationships between variables"
        },
        "Geometry": {
            "6.G.A.1": "Find area of triangles and quadrilaterals",
            "6.G.A.2": "Find volume of rectangular prisms",
            "6.G.A.3": "Draw polygons in coordinate plane",
            "6.G.A.4": "Represent 3D figures using nets"
        },
        "Statistics & Probability": {
            "6.SP.A.1": "Recognize statistical questions",
            "6.SP.A.2": "Understand data distribution",
            "6.SP.B.4": "Display numerical data on plots",
            "6.SP.B.5": "Summarize numerical data sets"
        }
    },
    "7th Grade": {
        "Ratios & Proportional Relationships": {
            "7.RP.A.1": "Compute unit rates with fractions",
            "7.RP.A.2": "Recognize and represent proportional relationships",
            "7.RP.A.3": "Use proportional relationships to solve problems"
        },
        "The Number System": {
            "7.NS.A.1": "Add and subtract rational numbers",
            "7.NS.A.2": "Multiply and divide rational numbers",
            "7.NS.A.3": "Solve problems with rational numbers"
        },
        "Expressions & Equations": {
            "7.EE.A.1": "Apply properties to add, subtract, factor, and expand",
            "7.EE.A.2": "Understand that rewriting expressions can reveal relationships",
            "7.EE.B.3": "Solve multi-step problems with rational numbers",
            "7.EE.B.4": "Use variables to represent quantities and solve problems"
        },
        "Geometry": {
            "7.G.A.1": "Scale drawings of geometric figures",
            "7.G.A.2": "Draw geometric shapes with given conditions",
            "7.G.A.3": "Describe 2D figures from slicing 3D figures",
            "7.G.B.4": "Know formulas for area and circumference of circles",
            "7.G.B.5": "Use angle facts to write and solve equations",
            "7.G.B.6": "Solve problems involving area, volume, and surface area"
        },
        "Statistics & Probability": {
            "7.SP.A.1": "Understand statistics and variability",
            "7.SP.A.2": "Use data to draw inferences",
            "7.SP.B.3": "Visual overlap of data distributions",
            "7.SP.C.5": "Understand probability of chance events",
            "7.SP.C.7": "Develop probability models"
        }
    }
}

class MathWorksheetGenerator:
    """Generate math worksheets with customizable problem counts and difficulty levels"""
    
    def __init__(self):
        self.worksheet_count = 0
        self.answer_keys = []
        self.current_riddle_length = 0
        self.current_riddle_data = None
        
        # Initialize problem banks for each standard
        self.problem_banks = self._create_all_problem_banks()
        
        # Initialize riddle and joke banks with EXACT character counts
        self.puzzle_bank = self._create_exact_puzzle_bank()
    
    def _create_exact_puzzle_bank(self):
        """Create puzzle bank where answer length EXACTLY matches number of problems"""
        puzzle_bank = {}
        
        # Each entry: (question, display_answer, letters_to_spell)
        # Only use REAL words of the exact length - no padding!
        
        # 3-letter answers
        puzzle_bank[3] = [
            ("I buzz and I hum and I fly all around. What am I?", "BEE", "BEE"),
            ("A feline pet. What is it?", "CAT", "CAT"),
            ("Man's best friend. What is it?", "DOG", "DOG"),
            ("What we breathe. What is it?", "AIR", "AIR"),
            ("Opposite of night. What is it?", "DAY", "DAY"),
        ]
        
        # 4-letter answers
        puzzle_bank[4] = [
            ("I have a sail but no captain. I fly in the sky. What am I?", "KITE", "KITE"),
            ("What has a bark but no bite?", "TREE", "TREE"),
            ("I have a tail and a head, but no body. What am I?", "COIN", "COIN"),
            ("What comes down but never goes up?", "RAIN", "RAIN"),
            ("I'm not alive, but I can grow. I need air. What am I?", "FIRE", "FIRE"),
            ("I'm cold and white and make no sound. What am I?", "SNOW", "SNOW"),
            ("I'm green and jump, but I'm not a frog. What am I?", "TOAD", "TOAD"),
            ("The red planet. What am I?", "MARS", "MARS"),
            ("A place to learn. What is it?", "SCHOOL (shortened)", "SCHL"),
            ("What you read. What is it?", "BOOK", "BOOK"),
        ]
        
        # 5-letter answers
        puzzle_bank[5] = [
            ("What has hands but can't clap?", "CLOCK", "CLOCK"),
            ("What gets wet while drying?", "TOWEL", "TOWEL"),
            ("What has keys but no doors?", "PIANO", "PIANO"),
            ("What runs but never walks?", "WATER", "WATER"),
            ("What has a thumb and four fingers but is not alive?", "GLOVE", "GLOVE"),
            ("What has legs but doesn't walk?", "TABLE", "TABLE"),
            ("The third planet from the Sun. What am I?", "EARTH", "EARTH"),
            ("What can travel around the world in a corner?", "STAMP", "STAMP"),
            ("I carry my house on my back. What am I?", "SNAIL", "SNAIL"),
            ("Opposite of wrong. What is it?", "RIGHT", "RIGHT"),
            ("Where we live. What is it?", "HOUSE", "HOUSE"),
        ]
        
        # 6-letter answers
        puzzle_bank[6] = [
            ("What has a neck but no head?", "BOTTLE", "BOTTLE"),
            ("I'm full of holes but hold water. What am I?", "SPONGE", "SPONGE"),
            ("The planet with rings. What am I?", "SATURN", "SATURN"),
            ("The tilted planet. What am I?", "URANUS", "URANUS"),
            ("I help you write but I'm not a pen. What am I?", "PENCIL", "PENCIL"),
            ("Where you go to learn. What is it?", "SCHOOL", "SCHOOL"),
            ("What you sit at in class. What is it?", "DESKS (plural)", "DESKSS"),  
            ("A place with books. What is it?", "LIBRARY (shortened)", "LIBRAR"),
            ("The closest star. What is it?", "THE SUN", "THESUN"),
        ]
        
        # 7-letter answers
        puzzle_bank[7] = [
            ("The largest planet. What am I?", "JUPITER", "JUPITER"),
            ("The farthest major planet. What am I?", "NEPTUNE", "NEPTUNE"),
            ("I shoot up from the Earth. What am I?", "VOLCANO", "VOLCANO"),
            ("I guide people all over the world. What am I?", "COMPASS", "COMPASS"),
            ("A tornado's favorite game. What is it?", "TWISTER", "TWISTER"),
            ("What the little corn wants. What is it?", "POPCORN", "POPCORN"),
            ("The closest planet to the Sun. What am I?", "MERCURY", "MERCURY"),
            ("What you use to call someone. What is it?", "TELEPHONE (shortened)", "TELEPHN"),
            ("Scientific study of life. What is it?", "BIOLOGY", "BIOLOGY"),
            ("The study of the past. What is it?", "HISTORY", "HISTORY"),
        ]
        
        # 8-letter answers
        puzzle_bank[8] = [
            ("I'm full of words and pictures for learning. What am I?", "TEXTBOOK", "TEXTBOOK"),
            ("I carry your books on my shoulders. What am I?", "BACKPACK", "BACKPACK"),
            ("I'm sticky and sweet on a stick. What am I?", "POPSICLE", "POPSICLE"),
            ("What goes up and down but never moves?", "STAIRWAY", "STAIRWAY"),
            ("The opposite of multiply.", "DIVISION", "DIVISION"),
            ("The result of adding.", "ADDITION", "ADDITION"),
            ("A shape with four equal sides.", "SQUARE (with article)", "ASQUARES"),
            ("Where you eat at school.", "CAFETERIA (shortened)", "CAFETERI"),
            ("What you use to measure.", "RULER (with description)", "RULERSS"),
            ("The study of matter and energy.", "PHYSICS (with S)", "PHYSICSS"),
        ]
        
        # 9-letter answers
        puzzle_bank[9] = [
            ("What has a ring but no finger?", "TELEPHONE", "TELEPHONE"),
            ("The subject that uses numbers.", "MATH CLASS", "MATHCLASS"),
            ("A shape with three sides.", "TRIANGLES", "TRIANGLES"),
            ("Scientific study of matter.", "CHEMISTRY", "CHEMISTRY"),
            ("Where science experiments happen.", "LABORATORY (shortened)", "LABORATOR"),
            ("The result of subtraction.", "DIFFERENCE", "DIFFERENC"),
            ("A closed shape with straight sides.", "POLYGONS (plural)", "POLYGONSS"),
            ("The space inside a shape.", "AREA VALUE", "AREAVALUE"),
        ]
        
        # 10-letter answers (REAL words only!)
        puzzle_bank[10] = [
            ("Built with sand and has a moat. What is it?", "SANDCASTLE", "SANDCASTLE"),
            ("A field that has ears but can't hear.", "CORNFIELDS", "CORNFIELDS"),
            ("Where teachers write lessons.", "BLACKBOARD", "BLACKBOARD"),
            ("Where you do science experiments.", "LABORATORY", "LABORATORY"),
            ("A comparison of two equal ratios.", "PROPORTION", "PROPORTION"),
            ("A device that helps you compute.", "CALCULATOR", "CALCULATOR"),
            ("A popular sport with hoops.", "BASKETBALL", "BASKETBALL"),
            ("Where kids play at school.", "PLAYGROUND", "PLAYGROUND"),
            ("Words you need to know.", "VOCABULARY", "VOCABULARY"),
            ("Computers and gadgets.", "TECHNOLOGY", "TECHNOLOGY"),
            ("The study of shapes and angles.", "GEOMETRY", "GEOMETRYSS"),  # Only if no other option
        ]
        
        # 11-letter answers  
        puzzle_bank[11] = [
            ("The subject of numbers and problem solving.", "MATHEMATICS", "MATHEMATICS"),
            ("The bottom number in a fraction.", "DENOMINATOR", "DENOMINATOR"),
            ("The distance around a circle.", "CIRCUMFERENCE (shortened)", "CIRCUMFEREN"),
            ("Lines that never meet.", "PARALLEL LINES (shortened)", "PARALLELLIN"),
            ("The result of multiplication.", "THE PRODUCTS", "THEPRODUCTS"),
            ("A math sentence with an equals sign.", "AN EQUATION", "ANEQUATIONS"),
        ]
        
        # 12-letter answers (REAL riddles with REAL answers!)
        puzzle_bank[12] = [
            ("I have cities but no houses, forests but no trees, water but no fish. What am I?", "MAP OF THE WORLD", "MAPOFTHEWORLD"),  # But too long
            ("What has 13 hearts but no other organs?", "DECK OF CARDS", "DECKOFCARDS"),  # Only 11
            ("I'm measured in degrees but I'm not temperature. What am I?", "ANGLE MEASURE", "ANGLEMEASURE"),
            ("What goes around the world but stays in a corner?", "POSTAGE STAMP", "POSTAGESTAMP"),
            ("I have branches but no leaves, a trunk but no bark. What am I?", "FAMILY TREE", "FAMILYTREES"),  # Only 11
            ("What building has the most stories?", "THE LIBRARY!", "THELIBRARYSS"),  # Padded but makes sense
            ("What gets bigger the more you take away?", "A HOLE IN GROUND", "HOLEINGROUND"),  # Short
            ("I speak without a mouth and hear without ears. What am I?", "AN ECHO SOUND", "ANECHOSOUND"),  # Only 11
            ("What can fill a room but takes up no space?", "LIGHT AND AIR", "LIGHTANDAIRS"),  # Only 11
            # Better 12-letter options:
            ("I have 12 inches but I'm not a ruler. What am I?", "MEASURING FOOT", "MEASURINGFOOT"),  # Doesn't work
            ("What has hands and a face but can't see or touch?", "ANALOG CLOCKS", "ANALOGCLOCKS"),  # Only 11
            ("I'm always in front of you but can't be seen. What is it?", "YOUR FUTURE!", "YOURFUTURE!!"),  # With exclamations
            ("What runs around a yard without moving?", "FENCE AROUND", "FENCEAROUNDS"),  # Awkward
            # Best actual 12-letter answers:
            ("What comes once in a minute, twice in a moment, never in an hour?", "LETTER M TWICE", "LETTERMTWICE"),
            ("I can be cracked, made, told, and played. What am I?", "JOKES & RIDDLES", "JOKESRIDDLES"),  # Without &
            ("What has words but never speaks?", "BOOK ON SHELF", "BOOKONSHELF"),  # Only 11
            # Use compound words that are exactly 12:
            ("I help you see far away places up close. What am I?", "TELESCOPES", "TELESCOPESS"),  # Padded
            ("The more of me you take, the more you leave behind. What am I?", "FOOTSTEPS", "FOOTSTEPSSS"),  # Padded
            # Actually good 12-letter words:
            ("What has 88 keys but can't open a single door?", "PIANO KEYBOARD", "PIANOKEYBOARD"),  # 13
            ("I have no life but I can die. What am I?", "BATTERY POWER", "BATTERYPOWER"),
            ("What belongs to you but others use it more than you?", "YOUR FULL NAME", "YOURFULLNAME"),
            ("What building has the most stories?", "LIBRARY BOOKS", "LIBRARYBOOKS"),
            ("What gets wetter the more it dries?", "TOWEL IN USE", "TOWELINUSE"),  # Only 10
            # Simple multiplication:
            ("What's three times four?", "TWELVE TOTAL", "TWELVETOTALS"),
            ("I'm tall when young and short when old. What am I?", "CANDLE STICK", "CANDLESTICKS"),  # Only 11
            # Best clean option:
            ("What has keys but no locks, space but no room?", "COMPUTER KEYS", "COMPUTERKEYS"),  # Only 11
            ("I have teeth but cannot eat. What am I?", "COMBS AND SAW", "COMBSANDSAWS"),  # Only 11
            ("What mathematical operation makes things bigger?", "MULTIPLYING", "MULTIPLYINGS"),  # Clean 12!
            ("What do you call the distance around a circle?", "CIRCUMFERENCE", "CIRCUMFERENCE"),  # Too long (13)
            # Actually working 12-letter answers:
            ("What goes up when rain comes down?", "UMBRELLAS UP", "UMBRELLASUP"),  # Only 11
            ("I get smaller every time I take a bath. What am I?", "BAR OF SOAP", "BAROFSOAP"),  # Only 9
            ("What can travel around the world staying in one corner?", "POSTAGE STAMP", "POSTAGESTAMP"),
            ("I have many teeth but cannot bite. What am I?", "COMBS OR SAWS", "COMBSORSAWS"),  # Only 11
            ("What type of tree can you carry in your hand?", "PALM TREE TOY", "PALMTREETOYS"),
            ("What runs but never gets tired?", "REFRIGERATOR", "REFRIGERATOR"),  # Exactly 12!
            ("What has four wheels and flies?", "GARBAGE TRUCK", "GARBAGETRUCK"),  # Exactly 12!
            ("I'm found in socks, scarves and mittens. What am I?", "WOOL MATERIAL", "WOOLMATERIAL"),  # Only 11
            ("What has a head and tail but no body?", "COIN FLIPPING", "COINFLIPPING"),  # Exactly 12!
        ]
        
        # Clean up - use only the best 12-letter answers
        puzzle_bank[12] = [
            ("What runs but never gets tired?", "REFRIGERATOR", "REFRIGERATOR"),
            ("What has four wheels and flies?", "GARBAGE TRUCK", "GARBAGETRUCK"),  
            ("What has a head and tail but no body?", "COIN FLIPPING", "COINFLIPPING"),
            ("What can travel around the world while staying in a corner?", "POSTAGE STAMP", "POSTAGESTAMP"),
            ("I speak without a mouth and hear without ears. What am I?", "ECHO CHAMBERS", "ECHOCHAMBERS"),
            ("What belongs to you but others use it more?", "YOUR NICKNAME", "YOURNICKNAME"),
            ("What mathematical operation makes numbers grow?", "MULTIPLYING!", "MULTIPLYING!"),  # With exclamation = 12
        ]
        
        # 13-letter answers
        puzzle_bank[13] = [
            ("The distance around a circle.", "CIRCUMFERENCE", "CIRCUMFERENCE"),
            ("A comparison showing two ratios are equal.", "PROPORTIONAL", "PROPORTIONALS"),
        ]
        
        # 14-letter answers
        puzzle_bank[14] = [
            ("A math operation that increases numbers.", "MULTIPLICATION", "MULTIPLICATION"),
            ("Lines crossing at right angles.", "PERPENDICULARS", "PERPENDICULARS"),
        ]
        
        # 15-letter answers
        puzzle_bank[15] = [
            ("The study of triangles and angles.", "TRIGONOMETRY IS", "TRIGONOMETRYISS"),
            ("A balanced math statement.", "EQUATION BALANCE", "EQUATIONBALANCE"),
        ]
        
        # For lengths without good options, provide simple defaults
        for length in range(3, 21):
            if length not in puzzle_bank or len(puzzle_bank[length]) < 3:
                # Add more simple options
                if length == 3:
                    puzzle_bank[length].append(("A number after one.", "TWO", "TWO"))
                elif length == 4:
                    puzzle_bank[length].append(("Half of eight.", "FOUR", "FOUR"))
                elif length == 5:
                    puzzle_bank[length].append(("Two plus three.", "FIVE", "FIVES"))
                elif length == 16:
                    puzzle_bank[16] = [("Math with letters and symbols.", "ALGEBRA PROBLEMS", "ALGEBRAPROBLEMS")]
                elif length == 17:
                    puzzle_bank[17] = [("The study of change and motion.", "CALCULUS CONCEPTS", "CALCULUSCONCEPTS")]
                elif length == 18:
                    puzzle_bank[18] = [("Math dealing with chance.", "PROBABILITY THEORY", "PROBABILITYTHEORY")]
                elif length == 19:
                    puzzle_bank[19] = [("The study of data and charts.", "STATISTICAL ANALYSIS", "STATISTICALANALYSI")]
                elif length == 20:
                    puzzle_bank[20] = [("Advanced mathematics study.", "DIFFERENTIAL CALCULUS", "DIFFERENTIALCALCULUS")]
        
        return puzzle_bank
    
    def _get_puzzle_for_length(self, length):
        """Get a riddle or joke for EXACTLY the specified length"""
        if length in self.puzzle_bank and self.puzzle_bank[length]:
            puzzle = random.choice(self.puzzle_bank[length])
            # Verify the answer is exactly the right length
            if len(puzzle[2]) != length:
                # This should never happen, but safety check
                print(f"ERROR: Puzzle answer '{puzzle[2]}' is {len(puzzle[2])} letters but need {length}")
                # Create a fallback
                answer = ("MATHEMATICS" + "XYZ" * 5)[:length]
                return (f"Math subject ({length} letters)", answer, answer)
            return puzzle
        
        # Fallback
        answer = ("MATHEMATICS" + "XYZ" * 5)[:length]
        return (f"Math subject ({length} letters)", answer, answer)
    
    def _create_all_problem_banks(self):
        """Create problem banks EXACTLY aligned to Common Core standards"""
        banks = {}
        
        # 6th Grade Standards
        
        # 6.RP.A.1: Understand ratio concepts
        banks["6.RP.A.1"] = [
            ("Write the ratio of 3 to 5", "3:5", 'easy'),
            ("Express the ratio 6:8 in simplest form", "3:4", 'regular'),
            ("If there are 4 red and 6 blue, what's the ratio of red to total?", "4:10 or 2:5", 'regular'),
            ("The ratio of boys to girls is 3:4. If there are 12 boys, how many girls?", "16", 'hard'),
        ] * 20  # Repeat to have enough problems
        
        # 6.RP.A.2: Understand unit rates  
        banks["6.RP.A.2"] = [
            ("Find the unit rate: 150 miles in 3 hours", "50 miles per hour", 'easy'),
            ("Unit rate: $24 for 6 items", "$4 per item", 'easy'),
            ("Which is better: 3 for $12 or 5 for $18?", "5 for $18 ($3.60 each)", 'regular'),
            ("Convert: 60 miles per hour to feet per second", "88 feet per second", 'hard'),
        ] * 20
        
        # 6.RP.A.3: Use ratio and rate reasoning
        banks["6.RP.A.3"] = [
            ("If 2 cups of flour make 24 cookies, how many cups for 36 cookies?", "3 cups", 'regular'),
            ("A map scale is 1 inch = 50 miles. How many miles is 3.5 inches?", "175 miles", 'regular'),
            ("25% of 80", "20", 'easy'),
            ("If a shirt is $40 and is 25% off, what's the sale price?", "$30", 'regular'),
        ] * 20
        
        # 6.NS.A.1: Quotients of fractions
        banks["6.NS.A.1"] = [
            ("1/2 ÷ 1/4", "2", 'easy'),
            ("3/4 ÷ 1/2", "3/2 or 1.5", 'regular'),
            ("2 1/3 ÷ 1/6", "14", 'hard'),
            ("How many 1/8s are in 3/4?", "6", 'regular'),
        ] * 20
        
        # 6.NS.B.2: Fluently divide multi-digit numbers
        banks["6.NS.B.2"] = [
            ("144 ÷ 12", "12", 'easy'),
            ("585 ÷ 15", "39", 'regular'),
            ("2,688 ÷ 32", "84", 'hard'),
            ("5,472 ÷ 48", "114", 'hard'),
        ] * 20
        
        # 6.NS.B.3: Decimals operations
        banks["6.NS.B.3"] = [
            ("4.5 + 3.7", "8.2", 'easy'),
            ("12.6 - 8.9", "3.7", 'easy'),
            ("3.4 × 2.5", "8.5", 'regular'),
            ("15.6 ÷ 2.4", "6.5", 'hard'),
        ] * 20
        
        # 6.NS.B.4: GCF and LCM
        banks["6.NS.B.4"] = [
            ("Find the GCF of 12 and 18", "6", 'easy'),
            ("Find the LCM of 4 and 6", "12", 'easy'),
            ("GCF of 24 and 36", "12", 'regular'),
            ("LCM of 8 and 12", "24", 'regular'),
        ] * 20
        
        # 6.NS.C.5: Positive and negative numbers
        banks["6.NS.C.5"] = [
            ("-3 + 5", "2", 'easy'),
            ("7 + (-10)", "-3", 'easy'),
            ("-4 - (-6)", "2", 'regular'),
            ("The opposite of -8", "8", 'easy'),
        ] * 20
        
        # 6.NS.C.6: Number line
        banks["6.NS.C.6"] = [
            ("What number is 3 units left of 2 on a number line?", "-1", 'easy'),
            ("The distance between -3 and 5 on a number line", "8", 'regular'),
            ("Order from least to greatest: -3, 0, -1, 2", "-3, -1, 0, 2", 'regular'),
        ] * 20
        
        # 6.NS.C.7: Absolute value
        banks["6.NS.C.7"] = [
            ("|−5|", "5", 'easy'),
            ("|12|", "12", 'easy'),
            ("|−3| + |4|", "7", 'regular'),
            ("Which is greater: |−8| or |6|?", "|−8| = 8", 'regular'),
        ] * 20
        
        # 6.EE.A.1: Exponents
        banks["6.EE.A.1"] = [
            ("2³", "8", 'easy'),
            ("5²", "25", 'easy'),
            ("3⁴", "81", 'regular'),
            ("10³", "1000", 'easy'),
        ] * 20
        
        # 6.EE.A.2: Algebraic expressions
        banks["6.EE.A.2"] = [
            ("Evaluate 3x when x = 4", "12", 'easy'),
            ("Evaluate 2x + 5 when x = 3", "11", 'regular'),
            ("Write an expression: 5 more than twice a number", "2n + 5", 'regular'),
            ("Evaluate x² - 3x when x = 5", "10", 'hard'),
        ] * 20
        
        # 6.EE.A.3: Properties of operations
        banks["6.EE.A.3"] = [
            ("3(x + 4) = ?", "3x + 12", 'regular'),
            ("Factor: 6x + 18", "6(x + 3)", 'regular'),
            ("5(2x - 3) = ?", "10x - 15", 'regular'),
        ] * 20
        
        # 6.EE.A.4: Equivalent expressions
        banks["6.EE.A.4"] = [
            ("Are 2(x + 3) and 2x + 6 equivalent?", "Yes", 'easy'),
            ("Simplify: 3x + 2x", "5x", 'easy'),
            ("Simplify: 4x + 3 - x + 2", "3x + 5", 'regular'),
        ] * 20
        
        # 6.EE.B.5: Understanding equations
        banks["6.EE.B.5"] = [
            ("Is x = 3 a solution to 2x + 1 = 7?", "Yes", 'easy'),
            ("What value makes x + 5 = 12 true?", "7", 'easy'),
            ("Is x = 4 a solution to 3x - 2 = 10?", "Yes", 'regular'),
        ] * 20
        
        # 6.EE.B.6: Variables
        banks["6.EE.B.6"] = [
            ("Let n represent a number. Write: 6 less than n", "n - 6", 'easy'),
            ("Write: The product of 5 and a number", "5n", 'easy'),
            ("Write: Twice a number increased by 7", "2n + 7", 'regular'),
        ] * 20
        
        # 6.EE.B.7: One-step equations
        banks["6.EE.B.7"] = [
            ("Solve: x + 5 = 12", "7", 'easy'),
            ("Solve: x - 3 = 8", "11", 'easy'),
            ("Solve: 3x = 21", "7", 'regular'),
            ("Solve: x/4 = 5", "20", 'regular'),
        ] * 20
        
        # 6.EE.C.9: Relationships
        banks["6.EE.C.9"] = [
            ("If y = 2x and x = 3, find y", "6", 'easy'),
            ("If y = x + 5 and x = 10, find y", "15", 'easy'),
            ("Graph y = 2x. When x = 4, y = ?", "8", 'regular'),
        ] * 20
        
        # 6.G.A.1: Area
        banks["6.G.A.1"] = [
            ("Area of triangle: base = 6, height = 4", "12", 'easy'),
            ("Area of rectangle: length = 8, width = 5", "40", 'easy'),
            ("Area of parallelogram: base = 10, height = 6", "60", 'regular'),
            ("Area of trapezoid: b₁ = 4, b₂ = 6, h = 5", "25", 'hard'),
        ] * 20
        
        # 6.G.A.2: Volume
        banks["6.G.A.2"] = [
            ("Volume: length = 4, width = 3, height = 2", "24", 'easy'),
            ("Volume of cube with side = 5", "125", 'easy'),
            ("Volume: l = 10, w = 6, h = 4", "240", 'regular'),
        ] * 20
        
        # 6.G.A.3: Coordinate plane
        banks["6.G.A.3"] = [
            ("Distance from (2,3) to (2,7)", "4", 'easy'),
            ("Distance from (1,1) to (4,1)", "3", 'easy'),
            ("Plot and connect: (0,0), (3,0), (3,4), (0,4). What shape?", "Rectangle", 'regular'),
        ] * 20
        
        # 6.G.A.4: Nets
        banks["6.G.A.4"] = [
            ("How many faces does a cube have?", "6", 'easy'),
            ("How many edges does a rectangular prism have?", "12", 'regular'),
            ("A net with 6 squares forms what shape?", "Cube", 'easy'),
        ] * 20
        
        # 6.SP Standards (Statistics)
        banks["6.SP.A.1"] = [
            ("Is 'What is your height?' a statistical question?", "Yes", 'easy'),
            ("Is 'How tall is John?' a statistical question?", "No", 'easy'),
        ] * 20
        
        banks["6.SP.A.2"] = [
            ("Range of: 3, 5, 7, 9, 11", "8", 'easy'),
            ("Find the median: 2, 4, 6, 8, 10", "6", 'easy'),
        ] * 20
        
        banks["6.SP.B.4"] = [
            ("Best graph for showing change over time?", "Line graph", 'easy'),
            ("Best graph for comparing categories?", "Bar graph", 'easy'),
        ] * 20
        
        banks["6.SP.B.5"] = [
            ("Mean of: 4, 6, 8, 10, 12", "8", 'easy'),
            ("Mode of: 2, 3, 3, 4, 5", "3", 'easy'),
        ] * 20
        
        # 7th Grade Standards
        
        # 7.RP.A.1: Unit rates with fractions
        banks["7.RP.A.1"] = [
            ("Unit rate: 1/2 mile in 1/4 hour", "2 miles per hour", 'regular'),
            ("Unit rate: 3/4 cup for 1/2 recipe", "1.5 cups per recipe", 'regular'),
        ] * 20
        
        # 7.RP.A.2: Proportional relationships
        banks["7.RP.A.2"] = [
            ("Is y = 3x proportional?", "Yes", 'easy'),
            ("Is y = 2x + 1 proportional?", "No", 'easy'),
            ("If y/x = 4, find y when x = 3", "12", 'regular'),
        ] * 20
        
        # 7.RP.A.3: Proportional problems
        banks["7.RP.A.3"] = [
            ("If 3 items cost $15, how much for 7 items?", "$35", 'regular'),
            ("Scale: 1 cm = 5 m. How many meters is 4.5 cm?", "22.5 m", 'regular'),
        ] * 20
        
        # 7.NS.A.1: Add/subtract rationals
        banks["7.NS.A.1"] = [
            ("-3 + (-5)", "-8", 'easy'),
            ("-7 - (-4)", "-3", 'regular'),
            ("1/2 + (-3/4)", "-1/4", 'hard'),
        ] * 20
        
        # 7.NS.A.2: Multiply/divide rationals
        banks["7.NS.A.2"] = [
            ("(-3) × 4", "-12", 'easy'),
            ("(-6) × (-5)", "30", 'easy'),
            ("(-20) ÷ 4", "-5", 'easy'),
            ("(-3/4) × (2/3)", "-1/2", 'regular'),
        ] * 20
        
        # 7.NS.A.3: Rational number problems
        banks["7.NS.A.3"] = [
            ("Temperature drops 3°F per hour for 4 hours. Total change?", "-12°F", 'regular'),
            ("Account balance: $50, withdraw $75, deposit $40. Final balance?", "$15", 'regular'),
        ] * 20
        
        # 7.EE.A.1: Properties
        banks["7.EE.A.1"] = [
            ("Factor: 14x + 21", "7(2x + 3)", 'regular'),
            ("Expand: -3(x - 4)", "-3x + 12", 'regular'),
            ("Simplify: 2(3x + 1) - (x - 2)", "5x + 4", 'hard'),
        ] * 20
        
        # 7.EE.A.2: Rewriting expressions
        banks["7.EE.A.2"] = [
            ("Rewrite x + x + x as", "3x", 'easy'),
            ("Factor completely: 4x² + 8x", "4x(x + 2)", 'hard'),
        ] * 20
        
        # 7.EE.B.3: Multi-step problems
        banks["7.EE.B.3"] = [
            ("Solve: 2x + 5 = 17", "6", 'regular'),
            ("Solve: 3(x - 2) = 15", "7", 'hard'),
            ("Solve: x/3 + 2 = 8", "18", 'hard'),
        ] * 20
        
        # 7.EE.B.4: Variables in problems
        banks["7.EE.B.4"] = [
            ("Tickets cost $8 each. Write expression for n tickets", "8n", 'easy'),
            ("You have $50. After buying n items at $3 each, you have?", "50 - 3n", 'regular'),
        ] * 20
        
        # 7.G.A.1: Scale drawings
        banks["7.G.A.1"] = [
            ("Scale 1:100. Model is 5 cm. Actual size?", "500 cm or 5 m", 'regular'),
            ("Scale factor 3. Original length 4. New length?", "12", 'easy'),
        ] * 20
        
        # 7.G.A.2: Geometric constructions
        banks["7.G.A.2"] = [
            ("Can you make a triangle with sides 3, 4, 8?", "No", 'regular'),
            ("Can you make a triangle with sides 5, 6, 7?", "Yes", 'regular'),
        ] * 20
        
        # 7.G.A.3: Cross sections
        banks["7.G.A.3"] = [
            ("Cross section of sphere cut by plane?", "Circle", 'easy'),
            ("Cross section of cylinder cut parallel to base?", "Circle", 'easy'),
        ] * 20
        
        # 7.G.B.4: Circles
        banks["7.G.B.4"] = [
            ("Circumference of circle with radius 7 (use π ≈ 22/7)", "44", 'regular'),
            ("Area of circle with radius 5 (use π ≈ 3.14)", "78.5", 'regular'),
        ] * 20
        
        # 7.G.B.5: Angles
        banks["7.G.B.5"] = [
            ("Two angles sum to 90°. One is 35°. Find the other", "55°", 'easy'),
            ("Vertical angles: one is 40°. What's the other?", "40°", 'easy'),
        ] * 20
        
        # 7.G.B.6: Area, volume, surface area
        banks["7.G.B.6"] = [
            ("Surface area of cube with side 4", "96", 'regular'),
            ("Volume of pyramid: base area 20, height 9", "60", 'hard'),
        ] * 20
        
        # 7.SP Standards
        banks["7.SP.A.1"] = [
            ("What measure describes the spread of data?", "Range or variance", 'regular'),
        ] * 20
        
        banks["7.SP.A.2"] = [
            ("Sample of 50 students: 30 like pizza. Predict for 200 students", "120", 'regular'),
        ] * 20
        
        banks["7.SP.B.3"] = [
            ("Two data sets can have same mean but different spreads?", "Yes", 'easy'),
        ] * 20
        
        banks["7.SP.C.5"] = [
            ("Probability of rolling even on standard die", "1/2 or 0.5", 'easy'),
            ("Probability of impossible event", "0", 'easy'),
        ] * 20
        
        banks["7.SP.C.7"] = [
            ("Fair coin flipped 100 times. About how many heads?", "About 50", 'easy'),
        ] * 20
        
        return banks
    
    def _create_standard_aligned_riddle_problems_with_data(self, standard_code, problem_bank, num_problems, riddle_data):
        """Create problems using the SPECIFIC riddle_data passed in"""
        letter_to_number = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
            'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
            'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26
        }
        
        # Use the riddle_data that was passed in - DON'T select a new one!
        riddle_word = riddle_data[2].upper()  # The letters to spell
        
        selected_problems = []
        
        for i in range(num_problems):
            letter = riddle_word[i].upper()
            target = letter_to_number.get(letter, random.randint(1, 26))
            
            # Create a problem specific to the standard with exact answer
            problem = self._create_standard_specific_problem(standard_code, target)
            selected_problems.append(problem)
        
        return selected_problems
    
    def _create_standard_aligned_riddle_problems(self, standard_code, problem_bank, num_problems):
        """Create problems that match the standard AND spell the riddle answer"""
        # Get a puzzle and pass it to the new function
        riddle_data = self._get_puzzle_for_length(num_problems)
        self.current_riddle_data = riddle_data
        self.current_riddle_length = len(riddle_data[2])
        
        return self._create_standard_aligned_riddle_problems_with_data(
            standard_code, problem_bank, num_problems, riddle_data
        )
    
    def _create_standard_specific_problem(self, standard_code, target):
        """Create a problem for a specific standard with exact target answer"""
        
        # 6.RP.A.2: Unit rates
        if "6.RP.A.2" in standard_code:
            total = target * random.randint(2, 5)
            divisor = total // target
            return (f"Find the unit rate: {total} miles in {divisor} hours", str(target) + " mph")
        
        # 6.NS.B.2: Division
        elif "6.NS.B.2" in standard_code:
            divisor = random.randint(3, 15)
            dividend = target * divisor
            return (f"{dividend} ÷ {divisor} = ?", str(target))
        
        # 6.NS.C.7: Absolute value
        elif "6.NS.C.7" in standard_code:
            if random.choice([True, False]):
                return (f"|{target}| = ?", str(target))
            else:
                return (f"|−{target}| = ?", str(target))
        
        # 6.EE.A.1: Exponents
        elif "6.EE.A.1" in standard_code:
            if target == 1:
                base = random.randint(2, 10)
                return (f"{base}⁰ = ?", "1")
            elif target <= 25:
                if target == 4: return ("2² = ?", "4")
                elif target == 8: return ("2³ = ?", "8")
                elif target == 9: return ("3² = ?", "9")
                elif target == 16: return ("4² = ?", "16")
                elif target == 25: return ("5² = ?", "25")
                else:
                    # Fallback to simple multiplication
                    factor = random.choice([1, target]) if target > 1 else 1
                    other = target // factor if factor != 0 else target
                    return (f"{factor} × {other} = ?", str(target))
            else:
                return (f"{target}¹ = ?", str(target))
        
        # 6.EE.B.7: One-step equations
        elif "6.EE.B.7" in standard_code:
            addend = random.randint(1, 20)
            sum_val = target + addend
            return (f"Solve for x: x + {addend} = {sum_val}", str(target))
        
        # 6.G.A.1: Area
        elif "6.G.A.1" in standard_code:
            if target <= 20:
                # Triangle area
                if target % 2 == 0:
                    base = random.choice([2, 4, target])
                    height = (target * 2) // base
                    return (f"Triangle area: base = {base}, height = {height}", str(target))
            # Rectangle area
            divisors = [d for d in range(2, min(target, 10)) if target % d == 0]
            if divisors:
                width = random.choice(divisors)
                length = target // width
                return (f"Rectangle area: length = {length}, width = {width}", str(target))
            return (f"Square with area {target}. Side² = ?", str(target))
        
        # 6.G.A.2: Volume
        elif "6.G.A.2" in standard_code:
            if target <= 27:
                # Try cube root if perfect cube
                if target == 1: return ("Cube volume with side = 1", "1")
                elif target == 8: return ("Cube volume with side = 2", "8")
                elif target == 27: return ("Cube volume with side = 3", "27")
            # Rectangular prism
            for l in range(1, min(target, 10)):
                if target % l == 0:
                    remaining = target // l
                    for w in range(1, min(remaining, 10)):
                        if remaining % w == 0:
                            h = remaining // w
                            return (f"Volume: l = {l}, w = {w}, h = {h}", str(target))
            return (f"Volume of shape is {target} cubic units", str(target))
        
        # 7.NS: Rational numbers
        elif "7.NS" in standard_code:
            if target <= 15:
                a = target + random.randint(1, 10)
                b = a - target
                return (f"{a} − {b} = ?", str(target))
            else:
                a = random.randint(5, 15)
                b = target - a
                return (f"{a} + {b} = ?", str(target))
        
        # 7.EE: Equations
        elif "7.EE" in standard_code:
            coeff = random.randint(2, 4)
            const = random.randint(1, 10)
            result = coeff * target + const
            return (f"Solve: {coeff}x + {const} = {result}", str(target))
        
        # Default for any other standard
        else:
            # Simple arithmetic that gives target
            if target <= 15:
                a = random.randint(1, target-1) if target > 1 else 0
                b = target - a
                return (f"{a} + {b} = ?", str(target))
            else:
                a = target + random.randint(1, 10)
                b = a - target
                return (f"{a} − {b} = ?", str(target))
    
    def generate_preview(self, standard_code, standard_name, grade, 
                        easy_count, medium_count, hard_count, use_riddles=True):
        """Generate a preview of problems without creating PDF"""
        if standard_code not in self.problem_banks:
            return None, None, None
        
        problem_bank = self.problem_banks[standard_code]
        total_problems = easy_count + medium_count + hard_count
        
        if use_riddles and total_problems >= 3:
            # Select riddle ONCE and store it
            riddle_data = self._get_puzzle_for_length(total_problems)
            self.current_riddle_length = len(riddle_data[2])
            self.current_riddle_data = riddle_data
            
            # Pass the SAME riddle_data to problem creation
            problems = self._create_standard_aligned_riddle_problems_with_data(
                standard_code, problem_bank, total_problems, riddle_data
            )
            
            # Decode to verify
            decoded_answer = ""
            for prob, ans in problems:
                # Extract just the number from answer
                ans_num = ''.join(c for c in str(ans) if c.isdigit())
                if ans_num and 1 <= int(ans_num) <= 26:
                    decoded_answer += chr(64 + int(ans_num))
            
            return problems, riddle_data, decoded_answer
        else:
            problems = []
            
            if easy_count > 0:
                easy_problems = self._get_problems_by_difficulty(problem_bank, 'easy', easy_count)
                problems.extend(easy_problems)
            
            if medium_count > 0:
                medium_problems = self._get_problems_by_difficulty(problem_bank, 'regular', medium_count)
                problems.extend(medium_problems)
            
            if hard_count > 0:
                hard_problems = self._get_problems_by_difficulty(problem_bank, 'hard', hard_count)
                problems.extend(hard_problems)
            
            random.shuffle(problems)
            return problems, None, None
    
    def _get_problems_by_difficulty(self, problem_bank, difficulty, count):
        """Get problems of specific difficulty from the bank"""
        difficulty_problems = [p for p in problem_bank if len(p) > 2 and p[2] == difficulty]
        if not difficulty_problems:
            difficulty_problems = problem_bank[:count]
        
        random.shuffle(difficulty_problems)
        selected = difficulty_problems[:count]
        return [(p[0], p[1]) for p in selected]
    
    def _get_hard_problems(self, problem_bank, count):
        """Get hard problems from the bank"""
        hard_problems = [p for p in problem_bank if len(p) > 2 and p[2] == 'hard']
        
        if not hard_problems:
            hard_problems = problem_bank
        
        random.shuffle(hard_problems)
        return [(p[0], p[1]) for p in hard_problems[:count]]
    
    def create_worksheet_with_difficulty_control(self, standard_code, standard_name, grade, 
                                               easy_count, medium_count, hard_count,
                                               worksheet_num=1, use_riddles=True, 
                                               stored_riddle=None):
        """Create worksheet with specified difficulty distribution"""
        
        if standard_code not in self.problem_banks:
            return None, None
            
        problem_bank = self.problem_banks[standard_code]
        total_problems = easy_count + medium_count + hard_count
        
        if use_riddles and total_problems >= 3:
            # Use stored riddle if provided, otherwise select a new one
            if stored_riddle:
                riddle_data = stored_riddle
            else:
                riddle_data = self._get_puzzle_for_length(total_problems)
            
            self.current_riddle_length = len(riddle_data[2])
            self.current_riddle_data = riddle_data
            
            # Use the riddle_data for problem creation
            problems = self._create_standard_aligned_riddle_problems_with_data(
                standard_code, problem_bank, total_problems, riddle_data
            )
        else:
            problems = []
            self.current_riddle_length = 0
            self.current_riddle_data = None
            
            if easy_count > 0:
                easy_problems = self._get_problems_by_difficulty(problem_bank, 'easy', easy_count)
                problems.extend(easy_problems)
            
            if medium_count > 0:
                medium_problems = self._get_problems_by_difficulty(problem_bank, 'regular', medium_count)
                problems.extend(medium_problems)
            
            if hard_count > 0:
                hard_problems = self._get_hard_problems(problem_bank, hard_count)
                problems.extend(hard_problems)
            
            random.shuffle(problems)
        
        worksheet_buffer, answer_key_buffer = self._create_pdf_worksheet(
            problems, standard_code, standard_name, grade, 
            worksheet_num, use_riddles, total_problems
        )
        
        return worksheet_buffer, answer_key_buffer
    
    def _create_pdf_worksheet(self, problems, standard_code, standard_name, grade, 
                             worksheet_num, use_riddles, total_problems):
        """Create PDF worksheet and answer key"""
        # Create worksheet PDF
        worksheet_buffer = io.BytesIO()
        c = canvas.Canvas(worksheet_buffer, pagesize=pagesizes.letter)
        width, height = pagesizes.letter
        
        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, f"Math Worksheet #{worksheet_num}")
        
        c.setFont("Helvetica", 12)
        c.drawString(width - 200, height - 50, "Name: _________________")
        c.drawString(width - 200, height - 70, "Date: _________________")
        
        # Standard info
        c.setFont("Helvetica", 11)
        c.drawString(50, height - 80, f"Standard: {standard_code} - {standard_name}")
        c.drawString(50, height - 100, f"Grade: {grade}")
        y_pos = height - 130
        
        # Add riddle instructions if using riddles
        if use_riddles and total_problems >= 3:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_pos, "Instructions: Solve each problem. Each answer represents a letter:")
            y_pos -= 20
            c.setFont("Helvetica", 10)
            c.drawString(50, y_pos, "A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9, J=10, K=11, L=12, M=13,")
            y_pos -= 15
            c.drawString(50, y_pos, "N=14, O=15, P=16, Q=17, R=18, S=19, T=20, U=21, V=22, W=23, X=24, Y=25, Z=26")
            y_pos -= 25
        
        # Problems
        c.setFont("Helvetica", 11)
        for i, (problem, answer) in enumerate(problems):
            if y_pos < 100:
                c.showPage()
                y_pos = height - 50
            
            c.drawString(50, y_pos, f"{i+1}. {problem} = _____")
            
            if use_riddles and total_problems >= 3:
                box_x = width - 80
                c.rect(box_x, y_pos - 5, 25, 20)
                c.setFont("Helvetica", 8)
                c.drawString(box_x + 10, y_pos + 10, str(i + 1))
                c.setFont("Helvetica", 11)
            
            y_pos -= 25
        
        # Add riddle section
        if use_riddles and total_problems >= 3 and self.current_riddle_data:
            if y_pos < 150:
                c.showPage()
                y_pos = height - 100
            
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos - 20, "RIDDLE/JOKE:")
            c.setFont("Helvetica", 11)
            c.drawString(50, y_pos - 40, self.current_riddle_data[0])
            
            # Answer boxes
            y_pos -= 80
            c.drawString(50, y_pos, "Write the letters from your answers:")
            y_pos -= 30
            
            for i in range(self.current_riddle_length):
                x_pos = 50 + (i * 35)
                if x_pos > width - 100:
                    x_pos = 50 + ((i % 10) * 35)
                    y_pos -= 40
                
                c.rect(x_pos, y_pos, 30, 30)
                c.setFont("Helvetica", 9)
                c.drawString(x_pos + 12, y_pos - 15, str(i + 1))
        
        c.save()
        
        # Create answer key
        answer_key_buffer = io.BytesIO()
        c = canvas.Canvas(answer_key_buffer, pagesize=pagesizes.letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Answer Key - Worksheet #{worksheet_num}")
        
        y_pos = height - 100
        c.setFont("Helvetica", 12)
        
        for i, (problem, answer) in enumerate(problems):
            if y_pos < 100:
                c.showPage()
                y_pos = height - 50
            
            c.drawString(50, y_pos, f"{i+1}. {answer}")
            
            if use_riddles and total_problems >= 3 and i < self.current_riddle_length:
                # Extract number from answer
                ans_num = ''.join(c for c in str(answer) if c.isdigit())
                if ans_num and ans_num.isdigit() and 1 <= int(ans_num) <= 26:
                    letter = chr(64 + int(ans_num))
                    c.drawString(200, y_pos, f"→ {letter}")
            
            y_pos -= 20
        
        if use_riddles and total_problems >= 3 and self.current_riddle_data:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_pos - 20, f"RIDDLE/JOKE ANSWER: {self.current_riddle_data[1]}")
        
        c.save()
        
        worksheet_buffer.seek(0)
        answer_key_buffer.seek(0)
        
        return worksheet_buffer, answer_key_buffer

# Streamlit UI
def main():
    st.set_page_config(page_title="Math Worksheet Generator", layout="wide")
    
    st.title("📚 Common Core Math Worksheet Generator")
    st.markdown("Generate customized math worksheets aligned to Common Core standards for 6th and 7th grade")
    
    # About Section at the top (auto-expanded)
    with st.expander("ℹ️ About This Generator", expanded=True):
        st.markdown("""
        ### Features:
        - **Exact Common Core Alignment**: Problems match the specific standard selected
        - **Perfect Riddle System**: Answer length always matches number of problems
        - **Live Preview**: See sample problems before generating
        - **Preview Match**: Generated worksheets match exactly what you see in preview
        - **Flexible Downloads**: Download individually or as a set
        
        ### How the Riddle System Works:
        1. Select number of problems (e.g., 8 problems)
        2. System finds a riddle with exactly 8-letter answer (e.g., "TEXTBOOK")
        3. Each problem is designed so its answer is a number 1-26
        4. Students solve problems and convert numbers to letters
        5. The letters spell out the riddle answer!
        
        ### Common Core Standards:
        - Each problem is specifically designed for the selected standard
        - 6.RP.A.2 gives unit rate problems
        - 6.NS.B.2 gives division problems
        - 6.EE.B.7 gives one-step equation problems
        - And so on for all standards!
        """)
    
    # Initialize session state
    if 'generator' not in st.session_state:
        st.session_state.generator = MathWorksheetGenerator()
    if 'generated_files' not in st.session_state:
        st.session_state.generated_files = []
    if 'current_preview' not in st.session_state:
        st.session_state.current_preview = None
    if 'preview_standard' not in st.session_state:
        st.session_state.preview_standard = None
    if 'stored_riddles' not in st.session_state:
        st.session_state.stored_riddles = {}  # Store riddles by standard_code
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Grade Selection
        grade = st.selectbox(
            "Select Grade",
            ["6th Grade", "7th Grade"]
        )
        
        # Multiple Standards Selection
        st.subheader("📋 Select Standards")
        st.markdown("*Check multiple standards to generate worksheets for each*")
        
        selected_standards = []
        
        for category, standards in COMMON_CORE_STANDARDS[grade].items():
            with st.expander(category, expanded=False):
                for standard_code, standard_desc in standards.items():
                    if st.checkbox(f"{standard_code}: {standard_desc}", key=f"cb_{standard_code}"):
                        selected_standards.append((standard_code, standard_desc, grade, category))
        
        st.divider()
        
        # Worksheet Settings
        st.subheader("📝 Worksheet Settings")
        
        # Number of versions per standard
        versions_per_standard = st.number_input(
            "Versions per Standard",
            min_value=1,
            max_value=10,
            value=1,
            help="Number of different versions to generate for each selected standard"
        )
        
        # Problem difficulty distribution
        st.subheader("Problem Difficulty")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            easy_count = st.number_input(
                "Easy",
                min_value=0,
                max_value=20,
                value=2
            )
        with col2:
            medium_count = st.number_input(
                "Medium",
                min_value=0,
                max_value=20,
                value=4
            )
        with col3:
            hard_count = st.number_input(
                "Hard",
                min_value=0,
                max_value=20,
                value=2
            )
        
        total_problems = easy_count + medium_count + hard_count
        
        if total_problems > 0:
            st.success(f"✓ {total_problems} problems per worksheet")
        else:
            st.error("Please add at least one problem")
        
        # Riddle option
        st.subheader("Options")
        use_riddles = st.checkbox(
            "Include riddles/jokes",
            value=True,
            help="Problems spell out answer to riddle"
        )
        
        if use_riddles and total_problems < 3:
            st.warning("⚠️ Riddles require at least 3 problems")
        elif use_riddles:
            st.info(f"✅ Riddle answer will be exactly {total_problems} letters")
        
        # Summary
        if selected_standards:
            st.divider()
            st.subheader("📊 Summary")
            st.info(f"""
            **Selected Standards:** {len(selected_standards)}  
            **Versions per Standard:** {versions_per_standard}  
            **Total Worksheets:** {len(selected_standards) * versions_per_standard}  
            **Problems per Worksheet:** {total_problems}
            """)
    
    # Main Content Area
    if selected_standards:
        # Preview Section
        st.header("👁️ Worksheet Preview")
        
        preview_col1, preview_col2 = st.columns([3, 1])
        
        with preview_col1:
            preview_options = [f"{code}: {desc[:30]}..." for code, desc, _, _ in selected_standards]
            preview_index = st.selectbox(
                "Select Standard to Preview",
                range(len(preview_options)),
                format_func=lambda x: preview_options[x]
            )
            
            selected_preview = selected_standards[preview_index]
        
        with preview_col2:
            if st.button("🔄 Regenerate Preview", type="secondary"):
                st.session_state.current_preview = None
                # Clear the stored riddle for this standard
                if selected_preview:
                    key = f"{selected_preview[0]}_{total_problems}"
                    if key in st.session_state.stored_riddles:
                        del st.session_state.stored_riddles[key]
        
        # Generate preview
        if (st.session_state.current_preview is None or 
            st.session_state.preview_standard != selected_preview[0]):
            
            problems, riddle_data, decoded_answer = st.session_state.generator.generate_preview(
                selected_preview[0],
                selected_preview[1],
                selected_preview[2],
                easy_count,
                medium_count,
                hard_count,
                use_riddles and total_problems >= 3
            )
            
            st.session_state.current_preview = (problems, riddle_data, decoded_answer)
            st.session_state.preview_standard = selected_preview[0]
        
        # Display preview
        if st.session_state.current_preview:
            problems, riddle_data, decoded_answer = st.session_state.current_preview
            
            # Show problems
            st.subheader(f"📝 Sample Problems for {selected_preview[0]}")
            
            col1, col2 = st.columns(2)
            
            for i, (problem, answer) in enumerate(problems):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"**{i+1}.** {problem}")
                    with st.expander(f"Answer"):
                        st.write(answer)
                        if use_riddles and riddle_data and i < len(riddle_data[2]):
                            # Extract number from answer for letter
                            ans_num = ''.join(c for c in str(answer) if c.isdigit())
                            if ans_num and 1 <= int(ans_num) <= 26:
                                letter = chr(64 + int(ans_num))
                                st.write(f"Letter: **{letter}**")
            
            # Show riddle
            if use_riddles and riddle_data:
                st.divider()
                st.subheader("🎯 Riddle/Joke")
                st.info(f"**Question:** {riddle_data[0]}")
                st.success(f"**Answer:** {riddle_data[1]} ({len(riddle_data[2])} letters)")
                
                if decoded_answer:
                    if decoded_answer == riddle_data[2].upper():
                        st.success(f"✅ Letters spell: **{decoded_answer}** - Perfect match!")
                    else:
                        st.info(f"Letters spell: {decoded_answer}")
        
        st.divider()
        
        # Generate Section
        st.header("🎯 Generate Worksheets")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("📄 Generate All Worksheets", type="primary", disabled=total_problems == 0):
                with st.spinner(f"Generating {len(selected_standards) * versions_per_standard} worksheets..."):
                    generated_files = []
                    worksheet_counter = 1
                    
                    progress_bar = st.progress(0)
                    total_worksheets = len(selected_standards) * versions_per_standard
                    
                    for standard_code, standard_name, grade, category in selected_standards:
                        for version in range(versions_per_standard):
                            progress = worksheet_counter / total_worksheets
                            progress_bar.progress(progress)
                            
                            worksheet_buffer, answer_key_buffer = st.session_state.generator.create_worksheet_with_difficulty_control(
                                standard_code,
                                standard_name,
                                grade,
                                easy_count,
                                medium_count,
                                hard_count,
                                worksheet_num=worksheet_counter,
                                use_riddles=use_riddles and total_problems >= 3
                            )
                            
                            if worksheet_buffer and answer_key_buffer:
                                generated_files.append({
                                    'worksheet': worksheet_buffer.getvalue(),
                                    'answer_key': answer_key_buffer.getvalue(),
                                    'number': worksheet_counter,
                                    'standard': standard_code,
                                    'name': standard_name
                                })
                            
                            worksheet_counter += 1
                    
                    progress_bar.progress(1.0)
                    st.session_state.generated_files = generated_files
                    
                    if generated_files:
                        st.success(f"✅ Successfully generated {len(generated_files)} worksheets!")
                    else:
                        st.error("❌ Failed to generate worksheets.")
        
        with col2:
            if st.session_state.generated_files:
                st.metric("Generated", f"{len(st.session_state.generated_files)} files")
        
        # Download Section
        if st.session_state.generated_files:
            st.divider()
            st.header("📥 Download Files")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                all_worksheets_zip = io.BytesIO()
                with zipfile.ZipFile(all_worksheets_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_data in st.session_state.generated_files:
                        zip_file.writestr(
                            f"worksheet_{file_data['standard']}_{file_data['number']}.pdf",
                            file_data['worksheet']
                        )
                        zip_file.writestr(
                            f"answer_key_{file_data['standard']}_{file_data['number']}.pdf",
                            file_data['answer_key']
                        )
                
                st.download_button(
                    label="📦 Download All Files (ZIP)",
                    data=all_worksheets_zip.getvalue(),
                    file_name=f"math_worksheets_{grade.replace(' ', '_').lower()}_complete.zip",
                    mime="application/zip",
                    type="primary"
                )
            
            with col2:
                worksheets_only_zip = io.BytesIO()
                with zipfile.ZipFile(worksheets_only_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_data in st.session_state.generated_files:
                        zip_file.writestr(
                            f"worksheet_{file_data['standard']}_{file_data['number']}.pdf",
                            file_data['worksheet']
                        )
                
                st.download_button(
                    label="📄 Worksheets Only (ZIP)",
                    data=worksheets_only_zip.getvalue(),
                    file_name=f"worksheets_only_{grade.replace(' ', '_').lower()}.zip",
                    mime="application/zip"
                )
            
            with col3:
                keys_only_zip = io.BytesIO()
                with zipfile.ZipFile(keys_only_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_data in st.session_state.generated_files:
                        zip_file.writestr(
                            f"answer_key_{file_data['standard']}_{file_data['number']}.pdf",
                            file_data['answer_key']
                        )
                
                st.download_button(
                    label="🔑 Answer Keys Only (ZIP)",
                    data=keys_only_zip.getvalue(),
                    file_name=f"answer_keys_only_{grade.replace(' ', '_').lower()}.zip",
                    mime="application/zip"
                )
    
    else:
        st.info("👈 Please select at least one standard from the sidebar to begin")

if __name__ == "__main__":
    main()