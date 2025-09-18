# app.py - Math Worksheet Generator with Complete Fixes
import streamlit as st
import os
import zipfile
import io
import random
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
import math
from math import gcd
import csv

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
        "Statistics & Probability": {
            "7.SP.A.1": "Understand statistics and variability",
            "7.SP.A.2": "Use data to draw inferences",
            "7.SP.B.3": "Visual overlap of data distributions",
            "7.SP.C.5": "Understand probability of chance events",
            "7.SP.C.7": "Develop probability models"
        }
    }
}

# Standards that support riddles (numerical answers only)
RIDDLE_COMPATIBLE_STANDARDS = {
    # 6th Grade
    "6.RP.A.1", "6.RP.A.2", "6.RP.A.3",
    "6.NS.A.1", "6.NS.B.2", "6.NS.B.3", "6.NS.B.4", "6.NS.C.5", "6.NS.C.6", "6.NS.C.7",
    "6.EE.A.1", "6.EE.A.2", "6.EE.B.7", "6.EE.C.9",
    "6.G.A.1", "6.G.A.2", "6.G.A.3", "6.G.A.4",
    "6.SP.B.5",  # Only mean/median/mode calculations
    # 7th Grade
    "7.RP.A.1", "7.RP.A.2", "7.RP.A.3",
    "7.NS.A.1", "7.NS.A.2", "7.NS.A.3",
    "7.EE.B.3", "7.EE.B.4",
    "7.SP.C.5"  # Only numerical probability
}

class MathWorksheetGenerator:
    def __init__(self):
        self.worksheet_count = 0
        self.current_riddle = None
        self.current_letter_mapping = {}
        self.preview_state = None
        self.used_problems = []
        self.riddle_bank = self._create_enhanced_riddle_bank()
        self.problem_banks = self._create_problem_banks()
    
    def _create_enhanced_riddle_bank(self):
        """Create comprehensive riddle bank with exact letter counts"""
        riddle_bank = {}
        
        # 3-letter riddles
        riddle_bank[3] = [
            ("I buzz and make honey. What am I?", "BEE", "BEE"),
            ("A feline pet. What is it?", "CAT", "CAT"),
            ("Man's best friend. What is it?", "DOG", "DOG"),
            ("What we breathe. What is it?", "AIR", "AIR"),
            ("Opposite of night. What is it?", "DAY", "DAY"),
        ]
        
        # 4-letter riddles
        riddle_bank[4] = [
            ("What has bark but no bite?", "TREE", "TREE"),
            ("What comes down but never goes up?", "RAIN", "RAIN"),
            ("I'm red all over. What planet am I?", "MARS", "MARS"),
            ("What has teeth but can't bite?", "COMB", "COMB"),
            ("I have a tail and head but no body. What am I?", "COIN", "COIN"),
        ]
        
        # 5-letter riddles
        riddle_bank[5] = [
            ("What has hands but can't clap?", "CLOCK", "CLOCK"),
            ("What gets wet while drying?", "TOWEL", "TOWEL"),
            ("What runs but never walks?", "WATER", "WATER"),
            ("I'm your home, third from the Sun. What am I?", "EARTH", "EARTH"),
            ("What has keys but can't open locks?", "PIANO", "PIANO"),
            ("What did the buffalo say to her son on the first day of school?", "BISON", "BISON"),
            ("What has a tongue but cannot talk?", "ASHOE", "ASHOE"),
        ]
        
        # 6-letter riddles
        riddle_bank[6] = [
            ("What has a neck but no head?", "BOTTLE", "BOTTLE"),
            ("I'm full of holes but hold water. What am I?", "SPONGE", "SPONGE"),
            ("Where you go to learn. What is it?", "SCHOOL", "SCHOOL"),
            ("Planet with the most bling. What am I?", "SATURN", "SATURN"),
            ("I help you write but I'm not a pen. What am I?", "PENCIL", "PENCIL"),
        ]
        
        # 7-letter riddles
        riddle_bank[7] = [
            ("I'm the biggest gas giant. What am I?", "JUPITER", "JUPITER"),
            ("I shoot up from Earth, hot and bright. What am I?", "VOLCANO", "VOLCANO"),
            ("What is a tornado's favorite game?", "TWISTER", "TWISTER"),
            ("I'm closest to the Sun. What am I?", "MERCURY", "MERCURY"),
            ("I guide people but only point. What am I?", "COMPASS", "COMPASS"),
            ("I can travel up to 100 miles an hour but never leave the room. What am I?", "ASNEEZE", "ASNEEZE"),
        ]
        
        # 8-letter riddles
        riddle_bank[8] = [
            ("I'm full of words and pictures. What am I?", "TEXTBOOK", "TEXTBOOK"),
            ("I carry knowledge on my back. What am I?", "BACKPACK", "BACKPACK"),
            ("I go up and down but never move. What am I?", "STAIRWAY", "STAIRWAY"),
            ("I'm sweet and sticky on a stick. What am I?", "POPSICLE", "POPSICLE"),
            ("What has 13 hearts but no organs?", "DECKCARD", "DECKCARD"),
            ("It belonds to you, but your friends use it more.", "YOURNAME", "YOURNAME"),
            ("What did one volcano say to the other?", "ILAVAYOU", "ILAVAYOU"),
            ("What kind of tree fits in your hand?", "PALMTREE", "PALM TREE"),
            ("What word has 26 letters but only three syllables?", "ALPHABET", "ALPHABET"),
            ("I can run even though I have no legs. What am I?", "YOURNOSE", "YOURNOSE"),
        ]
        
        # 9-letter riddles
        riddle_bank[9] = [
            ("What has a ring but no finger?", "TELEPHONE", "TELEPHONE"),
            ("What has ears but cannot hear?", "CORNFIELD", "CORNFIELD"),
            ("What happens when a vampire goes in snow?", "FROSTBITE", "FROSTBITE"),
            ("What kind of music do mummies love?", "WRAPMUSIC", "WRAPMUSIC"),
            ("What do you call a rabbit with fleas?", "BUGSBUNNY", "BUGSBUNNY"),
            ("What do you call a fake noodle?", "ANIMPASTA", "ANIMPASTA"),
            ("What do horses do when it's time for bed?", "HITTHEHAY", "HITTHEHAY"),
            ("What do you call a cold puppy?", "ACHILIDOG", "ACHILIDOG"),
            ("What kind of fish knows how to do an appendectomy?", "ASTURGEON", "ASTURGEON"),
            ("I am always in front of you and never behind you. What am I?", "THEFUTURE", "THEFUTURE"),
        ]
        
        # 10-letter riddles
        riddle_bank[10] = [
            ("I'm made of sand and might have a moat. Build me near water, but I'm not a boat.", "SANDCASTLE", "SANDCASTLE"),
            ("What do you call two witches living together?", "BROOMMATES", "BROOMMATES"),
            ("I ring when it's time to start or end. I'm not a phone, but I'm every students friend.", "SCHOOLBELL", "SCHOOLBELL"),
            ("What do you give a vampire when they're sick?", "COFFINDROPS", "COFFINDROPS"),
            ("Which side of the turkey has the most feathers?", "THEOUTSIDE", "THEOUTSIDE"),
            ("How do astronomers organize a party?", "THEYPLANIT", "THEYPLANIT"),
            ("What's the easiest building to lift?", "LIGHTHOUSE", "LIGHTHOUSE"),
            ("What do you call it when a cow grows facial hair?", "AMOOSTACHE", "AMOOSTACHE"),
            ("What do you call an anxious fly?", "AJITTERBUG", "AJITTERBUG"),
            ("The more you take, the more you leave behind. What am I?", "FOOTPRINTS", "FOOTPRINTS"),
            ("What do you find at the end of the rainbow?", "THELETTERW", "THELETTERW"),
            ("Solve the problems below to uncover a phrase!", "YOUGOTTHIS", "YOUGOTTHIS"),
            
        ]
        
        # 11-letter riddles
        riddle_bank[11] = [
            ("What do you call a sleeping bull?", "BULLDOZER", "BULLDOZER"),
            ("What do you call two birds in love?", "TWEETHEARTS", "TWEETHEARTS"),
            ("What are ten things you can always count on?", "YOURFINGERS", "YOURFINGERS"),
            ("What is a rabbit's favorite dance??", "THEBUNNYHOP", "THEBUNNYHOP"),
            ("What kind of milk comes from a pampered cow?", "SPOILEDMILK", "SPOILEDMILK"),
            ("What's a sea monster's favorite lunch?", "FISHANDSHIPS", "FISHANDSHIPS"),
            ("What kind of bagel can travel?", "APLAINBAGEL", "APLAINBAGEL"),
            ("What kind of band can’t play music?", "ARUBBERBAND", "ARUBBERBAND"),
            ("Where is the ocean the deepest?", "ONTHEBOTTOM", "ONTHEBOTTOM"),
        ]

        # 12-letter riddles
        riddle_bank[12] = [
            ("What has wheels and flies but is not an airplane?", "GARBAGETRUCK", "GARBAGETRUCK"),
            ("What does a clam do on it's birthday?", "SHELLEBRATES", "SHELLEBRATES"),
            ("What kind of candy do you eat on a playground ?", "RECESSPIECES", "RECESSPIECES"),
            ("Where do math teachers go on vacation?", "NUMBERVILLE", "NUMBERVILLE"),
            ("What's a vampire's favorite fruit?", "BLOODORANGES", "BLOODORANGES"),
            ("What kind of car does a sheep like to drive?", "ALAMBORGHINI", "ALAMBORGHINI"),
            ("Where do penguins go to vote?", "THENORTHPOLL", "THENORTHPOLL"),
        ]

        # 13-letter riddles
        riddle_bank[13] = [
            ("What do you say to a kangaroo on its birthday?", "HOPPYBIRTHDAY", "HOPPYBIRTHDAY"),
            ("I help you see the stars at night. What am I?", "TELESCOPESYS", "TELESCOPESYS"),
            ("What's a math teacher's favorite season?", "MULTIPLYSPRING", "MULTIPLYSPRING"),
            ("What rock group has four men who can't sing?", "MOUNTRUSHMORE", "MOUNTRUSHMORE"),
            ("What do you call a funny mountain?", "HILARIOUSHILL", "HILARIOUSHILL"),
            ("What do cats eat for breakfast?", "MICEKRISPIRES", "MICEKRISPIRES"),
            ("What do you get when you cross a fish with an elephant?", "SWIMMINGTRUNKS", "SWIMMINGTRUNKS"),
            ("How do you find a cheetah in the dark?", "USEASPOTLIGHT", "USEASPOTLIGHT"),
            ("What do you call a happy cowboy?", "AJOLLYRANCHER", "AJOLLYRANCHER"),
        ]

        # 14-letter riddles
        riddle_bank[14] = [
            ("What are two things you can never have for breakfast?", "LUNCHANDDINNER", "LUNCHANDDINNER"),
            ("What did the little corn say to the mama corn?", "WHEREISPOPCORN", "WHEREISPOPCORN"),
            ("What do you call an alligator in a vest?", "ANINVESTIGATOR", "ANINVESTIGATOR"),
            ("Where do surfers go for an education?", "BOARDINGSCHOOL", "BOARDINGSCHOOL"),
            ("What do you call someone who raises hens?", "ACHICKENTENDER", "ACHICKENTENDER"),
            ("What is the best place to grow a garden in school?", "INKINDERGARTEN", "INKINDERGARTEN"),
            ("A king, a queen, and two twins are in a room. How are there no adults?", "THEYAREALLBEDS", "THEYAREALLBEDS"),
            ("What has a lot of needles but can’t sew?", "ACHRISTMASTREE", "ACHRISTMASTREE"),
        ]

        # 15-letter riddles
        riddle_bank[15] = [
            ("How do fish pay for groceries", "WITHSANDDOLLARS", "WITHSANDDOLLARS"),
            ("What do you call a dog magician?", "LABRACADABRADOR", "LABRACADABRADOR"),
            ("Solve the problems below to uncover a word!", "ACCOMPLISHMENTS", "ACCOMPLISHMENTS"),
            ("Solve the problems below to uncover a word!", "EXTRAORDINARILY", "EXTRAORDINARILY"),
            ("Solve the problems below to uncover a word!", "RESOURCEFULLNESS", "RESOURCEFULLNESS"),
            ("Solve the problems below to uncover a word!", "KINDHEARTEDNESS", "KINDHEARTEDNESS"),
        ]

        
        return riddle_bank
    
    def _create_problem_banks(self):
        """Create comprehensive problem banks for each standard"""
        banks = {}
        
        # 6th Grade Standards
        banks["6.RP.A.1"] = [
            lambda: self._ratio_problem(12, 18),
            lambda: self._ratio_problem(15, 25),
            lambda: self._ratio_problem(21, 28),
            lambda: self._ratio_problem(16, 20),
            lambda: self._ratio_problem(14, 21),
            lambda: ("Recipe uses 2 cups flour to 3 cups sugar. Ratio?", "2:3"),
            lambda: ("Class has 12 boys and 18 girls. Simplest ratio?", "2:3"),
            lambda: ("Team won 15 games, lost 10. Win to loss ratio?", "3:2"),
            lambda: ("Ratio of 8 red to 12 blue marbles?", "2:3"),
            lambda: ("24 cars to 16 trucks. Simplest form?", "3:2"),
            lambda: self._ratio_problem(9, 12),
            lambda: self._ratio_problem(10, 15),
            lambda: self._ratio_problem(18, 24),
            lambda: self._ratio_problem(20, 25),
            lambda: self._ratio_problem(27, 36),
            lambda: ("Ratio of 6 apples to 9 oranges?", "2:3"),
            lambda: ("15 minutes to 1 hour. Simplest ratio?", "1:4"),
            lambda: ("$12 to $18. Simplest ratio?", "2:3"),
            lambda: ("Ratio of 14 wins to 7 losses?", "2:1"),
            lambda: ("30 students: 18 passed, 12 failed. Pass:fail?", "3:2"),
            lambda: ("Ratio of 35 miles to 25 miles?", "7:5"),
            lambda: ("Mix uses 4 cups water to 6 cups juice. Ratio?", "2:3"),
        ]
        
        banks["6.RP.A.2"] = [
            lambda: ("Car travels 150 miles in 3 hours. Speed?", "50"),
            lambda: ("If 6 items cost $24, cost per item?", "4"),
            lambda: ("Read 45 pages in 15 minutes. Pages per minute?", "3"),
            lambda: ("240 miles in 4 hours. Miles per hour?", "60"),
            lambda: ("$35 for 7 items. Unit price?", "5"),
            lambda: ("Type 200 words in 5 minutes. Words per minute?", "40"),
            lambda: ("Factory makes 300 items in 6 hours. Rate?", "50"),
            lambda: ("Walk 18 blocks in 9 minutes. Blocks per minute?", "2"),
            lambda: ("360 miles in 6 hours. Speed?", "60"),
            lambda: ("$48 for 8 items. Cost per item?", "6"),
            lambda: ("Read 100 pages in 25 minutes. Pages per minute?", "4"),
            lambda: ("Bike 30 miles in 2 hours. Miles per hour?", "15"),
            lambda: ("$63 for 9 items. Unit price?", "7"),
            lambda: ("Type 300 words in 10 minutes. Words per minute?", "30"),
            lambda: ("Machine produces 400 items in 8 hours. Rate?", "50"),
            lambda: ("Run 12 miles in 2 hours. Speed?", "6"),
            lambda: ("$72 for 12 items. Cost each?", "6"),
            lambda: ("Complete 20 problems in 10 minutes. Problems per minute?", "2"),
            lambda: ("Travel 180 miles in 3 hours. Speed?", "60"),
            lambda: ("$100 for 20 items. Unit price?", "5"),
            lambda: ("Paint 120 sq ft in 4 hours. Sq ft per hour?", "30"),
            lambda: ("Earn $96 in 8 hours. Hourly rate?", "12"),
        ]
        
        banks["6.RP.A.3"] = [
            lambda: ("Find 25% of 80", "20"),
            lambda: ("Find 30% of 90", "27"),
            lambda: ("Find 50% of 84", "42"),
            lambda: ("Item costs $80. With 25% off, price?", "60"),
            lambda: ("$100 item, 30% discount. Sale price?", "70"),
            lambda: ("15 is what percent of 60?", "25"),
            lambda: ("20% tip on $45 bill?", "9"),
            lambda: ("Tax is 8% on $50. Total cost?", "54"),
            lambda: ("Find 10% of 120", "12"),
            lambda: ("Find 75% of 40", "30"),
            lambda: ("Find 20% of 150", "30"),
            lambda: ("Find 40% of 75", "30"),
            lambda: ("$60 item, 20% off. Sale price?", "48"),
            lambda: ("18 is what percent of 72?", "25"),
            lambda: ("15% tip on $40 bill?", "6"),
            lambda: ("Tax is 6% on $100. Total?", "106"),
            lambda: ("Find 60% of 50", "30"),
            lambda: ("Find 5% of 200", "10"),
            lambda: ("24 is what percent of 80?", "30"),
            lambda: ("$90 item, 10% off. Final price?", "81"),
            lambda: ("Find 35% of 60", "21"),
            lambda: ("Commission: 15% of $200 sale?", "30"),
            lambda: ("Markup: 25% on $40 item. Selling price?", "50"),
            lambda: ("Interest: 5% on $600. Amount?", "30"),
        ]

        banks["6.NS.A.1"] = [
            lambda: ("1/2 ÷ 1/4", "2"),
            lambda: ("3/4 ÷ 1/4", "3"),
            lambda: ("2/3 ÷ 1/3", "2"),
            lambda: ("How many quarters in 3?", "12"),
            lambda: ("How many halves in 4?", "8"),
            lambda: ("6 ÷ 1/2", "12"),
            lambda: ("3/5 ÷ 1/5", "3"),
            lambda: ("4/7 ÷ 2/7", "2"),
            lambda: ("8 ÷ 1/4", "32"),
            lambda: ("5/6 ÷ 1/6", "5"),
            lambda: ("3/8 ÷ 1/8", "3"),
            lambda: ("How many thirds in 5?", "15"),
            lambda: ("9 ÷ 1/3", "27"),
            lambda: ("2/5 ÷ 1/10", "4"),
            lambda: ("7/8 ÷ 1/8", "7"),
            lambda: ("10 ÷ 1/5", "50"),
            lambda: ("4/9 ÷ 2/9", "2"),
            lambda: ("How many sixths in 3?", "18"),
            lambda: ("3/4 ÷ 3/8", "2"),
            lambda: ("5/7 ÷ 5/14", "2"),
            lambda: ("12 ÷ 3/4", "16"),
            lambda: ("2/3 ÷ 1/6", "4"),
            lambda: ("15 ÷ 3/5", "25"),
        ]

        banks["6.NS.B.2"] = [
            lambda: ("144 ÷ 12", "12"),
            lambda: ("315 ÷ 15", "21"),
            lambda: ("576 ÷ 24", "24"),
            lambda: ("432 ÷ 18", "24"),
            lambda: ("768 ÷ 32", "24"),
            lambda: ("1000 ÷ 25", "40"),
            lambda: ("1350 ÷ 45", "30"),
            lambda: ("1080 ÷ 36", "30"),
            lambda: ("256 ÷ 16", "16"),
            lambda: ("396 ÷ 22", "18"),
            lambda: ("624 ÷ 26", "24"),
            lambda: ("840 ÷ 35", "24"),
            lambda: ("960 ÷ 40", "24"),
            lambda: ("1200 ÷ 50", "24"),
            lambda: ("648 ÷ 27", "24"),
            lambda: ("720 ÷ 30", "24"),
            lambda: ("900 ÷ 45", "20"),
            lambda: ("1440 ÷ 60", "24"),
            lambda: ("528 ÷ 22", "24"),
            lambda: ("672 ÷ 28", "24"),
            lambda: ("1560 ÷ 65", "24"),
            lambda: ("936 ÷ 39", "24"),
        ]
        
        banks["6.NS.B.3"] = [
            lambda: ("12.5 + 8.7", "21.2"),
            lambda: ("35.8 - 12.3", "23.5"),
            lambda: ("3.5 × 4", "14"),
            lambda: ("15.6 ÷ 2.4", "6.5"),
            lambda: ("24.6 + 17.9", "42.5"),
            lambda: ("48.6 - 19.7", "28.9"),
            lambda: ("2.8 × 5.5", "15.4"),
            lambda: ("28.8 ÷ 3.6", "8"),
            lambda: ("45.2 + 14.8", "60"),
            lambda: ("67.3 - 25.3", "42"),
            lambda: ("4.5 × 6", "27"),
            lambda: ("36.9 ÷ 3", "12.3"),
            lambda: ("15.75 + 9.25", "25"),
            lambda: ("52.4 - 18.4", "34"),
            lambda: ("7.2 × 5", "36"),
            lambda: ("42.5 ÷ 2.5", "17"),
            lambda: ("33.6 + 16.4", "50"),
            lambda: ("78.9 - 33.9", "45"),
            lambda: ("8.4 × 3", "25.2"),
            lambda: ("54.6 ÷ 4.2", "13"),
            lambda: ("19.95 + 20.05", "40"),
            lambda: ("88.8 - 44.8", "44"),
            lambda: ("5.5 × 8", "44"),
            lambda: ("72.8 ÷ 5.6", "13"),
        ]

        banks["6.NS.B.4"] = [
            lambda: ("GCF of 12 and 18", "6"),
            lambda: ("LCM of 4 and 6", "12"),
            lambda: ("GCF of 24 and 36", "12"),
            lambda: ("LCM of 6 and 8", "24"),
            lambda: ("GCF of 15 and 25", "5"),
            lambda: ("LCM of 5 and 7", "35"),
            lambda: ("GCF of 16 and 24", "8"),
            lambda: ("LCM of 9 and 12", "36"),
            lambda: ("GCF of 20 and 30", "10"),
            lambda: ("LCM of 3 and 8", "24"),
            lambda: ("GCF of 18 and 27", "9"),
            lambda: ("LCM of 10 and 15", "30"),
            lambda: ("GCF of 28 and 42", "14"),
            lambda: ("LCM of 8 and 12", "24"),
            lambda: ("GCF of 32 and 48", "16"),
            lambda: ("LCM of 7 and 9", "63"),
            lambda: ("GCF of 36 and 54", "18"),
            lambda: ("LCM of 4 and 10", "20"),
            lambda: ("GCF of 45 and 60", "15"),
            lambda: ("LCM of 6 and 9", "18"),
            lambda: ("GCF of 50 and 75", "25"),
            lambda: ("LCM of 12 and 18", "36"),
            lambda: ("GCF of 40 and 60", "20"),
            lambda: ("LCM of 15 and 20", "60"),
        ]

        banks["6.NS.C.5"] = [
            lambda: ("(-5) + 8", "3"),
            lambda: ("5 - (-8)", "13"),
            lambda: ("(-9) + (-6)", "-15"),
            lambda: ("(-12) + 7", "-5"),
            lambda: ("10 - 15", "-5"),
            lambda: ("(-10) - (-4)", "-6"),
            lambda: ("Temperature: 15°F drops 8°. New temp?", "7"),
            lambda: ("Elevation: 100 ft, descends 45 ft. New?", "55"),
            lambda: ("(-3) + 9", "6"),
            lambda: ("7 - (-5)", "12"),
            lambda: ("(-8) + (-7)", "-15"),
            lambda: ("(-15) + 10", "-5"),
            lambda: ("12 - 20", "-8"),
            lambda: ("(-6) - (-9)", "3"),
            lambda: ("(-4) + 11", "7"),
            lambda: ("14 - (-6)", "20"),
            lambda: ("(-13) + (-7)", "-20"),
            lambda: ("(-20) + 15", "-5"),
            lambda: ("18 - 25", "-7"),
            lambda: ("(-11) - (-16)", "5"),
            lambda: ("Temperature: -5°F rises 12°. New temp?", "7"),
            lambda: ("Account: $50, withdraws $65. Balance?", "-15"),
            lambda: ("(-7) + 19", "12"),
            lambda: ("25 - 40", "-15"),
        ]

        banks["6.NS.C.6"] = [
            lambda: ("Which is greater: -3 or -5?", "-3"),
            lambda: ("Find the opposite of -7", "7"),
            lambda: ("Distance from -4 to 0", "4"),
            lambda: ("Order: -2, 3, 0, -1 (least to greatest)", "-2,-1,0,3"),
            lambda: ("Midpoint between -6 and 2", "-2"),
            lambda: ("Point 5 units left of 2", "-3"),
            lambda: ("Distance from 6 to 0", "6"),
            lambda: ("Which is less: -4 or -9?", "-9"),
            lambda: ("Find the opposite of 12", "-12"),
            lambda: ("Distance from -8 to 0", "8"),
            lambda: ("Which is greater: -7 or -2?", "-2"),
            lambda: ("Point 3 units right of -5", "-2"),
            lambda: ("Distance from -10 to 0", "10"),
            lambda: ("Find the opposite of -15", "15"),
            lambda: ("Which is less: -6 or -1?", "-6"),
            lambda: ("Midpoint between -4 and 4", "0"),
            lambda: ("Point 7 units left of 3", "-4"),
            lambda: ("Distance from 9 to 0", "9"),
            lambda: ("Order: 5, -3, 0, -7 (greatest to least)", "5,0,-3,-7"),
            lambda: ("Which is greater: 0 or -5?", "0"),
            lambda: ("Point 10 units right of -12", "-2"),
            lambda: ("Distance between -3 and 3", "6"),
            lambda: ("Find the opposite of -20", "20"),
            lambda: ("Midpoint between -8 and 4", "-2"),
        ]

        banks["6.NS.C.7"] = [
            lambda: ("Find |−8|", "8"),
            lambda: ("Find |12|", "12"),
            lambda: ("|−3| + |5|", "8"),
            lambda: ("|7| - |−4|", "3"),
            lambda: ("|−6| × 2", "12"),
            lambda: ("Find |-15|", "15"),
            lambda: ("|10| ÷ |-2|", "5"),
            lambda: ("Which is greater: |−10| or |7|?", "10"),
            lambda: ("Find |−20|", "20"),
            lambda: ("Find |25|", "25"),
            lambda: ("|−9| + |6|", "15"),
            lambda: ("|12| - |−8|", "4"),
            lambda: ("|−5| × 3", "15"),
            lambda: ("Find |-18|", "18"),
            lambda: ("|24| ÷ |−6|", "4"),
            lambda: ("Which is greater: |−15| or |12|?", "15"),
            lambda: ("|−4| + |−4|", "8"),
            lambda: ("|16| - |7|", "9"),
            lambda: ("|−7| × 4", "28"),
            lambda: ("Find |-30|", "30"),
            lambda: ("|36| ÷ |−9|", "4"),
            lambda: ("Which is less: |−5| or |8|?", "5"),
            lambda: ("|−11| + |9|", "20"),
            lambda: ("|25| - |−5|", "20"),
        ]

        banks["6.EE.A.1"] = [
            lambda: ("Evaluate: 2³", "8"),
            lambda: ("Evaluate: 5²", "25"),
            lambda: ("Evaluate: 3⁴", "81"),
            lambda: ("Evaluate: 4³", "64"),
            lambda: ("Evaluate: 10²", "100"),
            lambda: ("Evaluate: 2⁵", "32"),
            lambda: ("Evaluate: 6²", "36"),
            lambda: ("Evaluate: 7²", "49"),
            lambda: ("Evaluate: 8²", "64"),
            lambda: ("Evaluate: 9²", "81"),
            lambda: ("Evaluate: 2⁴", "16"),
            lambda: ("Evaluate: 3³", "27"),
            lambda: ("Evaluate: 11²", "121"),
            lambda: ("Evaluate: 2⁶", "64"),
            lambda: ("Evaluate: 4²", "16"),
            lambda: ("Evaluate: 12²", "144"),
            lambda: ("Evaluate: 5³", "125"),
            lambda: ("Evaluate: 2⁷", "128"),
            lambda: ("Evaluate: 15²", "225"),
            lambda: ("Evaluate: 3⁵", "243"),
            lambda: ("Evaluate: 13²", "169"),
            lambda: ("Evaluate: 14²", "196"),
            lambda: ("Evaluate: 20²", "400"),
            lambda: ("Evaluate: 10³", "1000"),
        ]
        
        banks["6.EE.A.2"] = [
            lambda: ("Evaluate 3x + 5 when x = 4", "17"),
            lambda: ("Evaluate 2y - 7 when y = 10", "13"),
            lambda: ("Simplify: 4x + 2x", "6x"),
            lambda: ("Evaluate 5n + 3 when n = 2", "13"),
            lambda: ("Simplify: 7y - 3y", "4y"),
            lambda: ("Evaluate x² when x = 3", "9"),
            lambda: ("Combine: 3x + 5 + 2x", "5x + 5"),
            lambda: ("Evaluate 10 - 2m when m = 3", "4"),
            lambda: ("Evaluate 4x - 2 when x = 5", "18"),
            lambda: ("Simplify: 8x + 3x", "11x"),
            lambda: ("Evaluate 2x + 8 when x = 6", "20"),
            lambda: ("Simplify: 10y - 4y", "6y"),
            lambda: ("Evaluate 3n - 5 when n = 7", "16"),
            lambda: ("Combine: 5x + 7 + 3x", "8x + 7"),
            lambda: ("Evaluate 15 - 3m when m = 4", "3"),
            lambda: ("Simplify: 9x - 2x", "7x"),
            lambda: ("Evaluate x² + 2 when x = 4", "18"),
            lambda: ("Combine: 2x + 9 + 4x", "6x + 9"),
            lambda: ("Evaluate 7x - 3 when x = 3", "18"),
            lambda: ("Simplify: 12y - 7y", "5y"),
            lambda: ("Evaluate 4n + 6 when n = 3", "18"),
            lambda: ("Combine: 6x + 4 + x", "7x + 4"),
            lambda: ("Evaluate 20 - 4m when m = 2", "12"),
            lambda: ("Simplify: 15x - 8x", "7x"),
        ]

        banks["6.EE.A.3"] = [
            lambda: ("Which property: 3(x + 4) = 3x + 12?", "Distributive"),
            lambda: ("Which property: x + 0 = x?", "Identity"),
            lambda: ("Which property: 2 + 3 = 3 + 2?", "Commutative"),
            lambda: ("Which property: (2+3)+4 = 2+(3+4)?", "Associative"),
            lambda: ("Which property: 5 × 1 = 5?", "Identity"),
            lambda: ("Which property: 4(2x) = (4×2)x?", "Associative"),
            lambda: ("Which property: x × 0 = 0?", "Zero"),
            lambda: ("Which property: ab = ba?", "Commutative"),
            lambda: ("Which property: 2(x - 3) = 2x - 6?", "Distributive"),
            lambda: ("Which property: (xy)z = x(yz)?", "Associative"),
            lambda: ("Which property: x + y = y + x?", "Commutative"),
            lambda: ("Which property: 1 × n = n?", "Identity"),
            lambda: ("Which property: (a+b)+c = a+(b+c)?", "Associative"),
            lambda: ("Which property: 5(3 + 2) = 5×3 + 5×2?", "Distributive"),
            lambda: ("Which property: n + 0 = n?", "Identity"),
            lambda: ("Which property: 3×4 = 4×3?", "Commutative"),
            lambda: ("Which property: 0 + x = x?", "Identity"),
            lambda: ("Which property: 4(x + y) = 4x + 4y?", "Distributive"),
            lambda: ("Which property: m × 0 = 0?", "Zero"),
            lambda: ("Which property: (2×3)×4 = 2×(3×4)?", "Associative"),
            lambda: ("Which property: 7 + 8 = 8 + 7?", "Commutative"),
            lambda: ("Which property: 0 × y = 0?", "Zero"),
            lambda: ("Which property: x × 1 = x?", "Identity"),
            lambda: ("Which property: a + b = b + a?", "Commutative"),
        ]

        banks["6.EE.A.4"] = [
            lambda: ("Are 2(x + 3) and 2x + 6 equivalent?", "Yes"),
            lambda: ("Simplify: 3x + 2x - x", "4x"),
            lambda: ("Factor: 6x + 12", "6(x + 2)"),
            lambda: ("Are 5x and x + x + x + x + x equivalent?", "Yes"),
            lambda: ("Simplify: 8x - 3x", "5x"),
            lambda: ("Factor: 10x + 15", "5(2x + 3)"),
            lambda: ("Are 3(x + 2) and 3x + 6 equivalent?", "Yes"),
            lambda: ("Simplify: 7x - 2x + x", "6x"),
            lambda: ("Factor: 8x + 20", "4(2x + 5)"),
            lambda: ("Are 4x + 2 and 2(2x + 1) equivalent?", "Yes"),
            lambda: ("Simplify: 10x - 5x + 2x", "7x"),
            lambda: ("Factor: 12x + 8", "4(3x + 2)"),
            lambda: ("Are 6x and 2x + 4x equivalent?", "Yes"),
            lambda: ("Simplify: 9x - 4x - x", "4x"),
            lambda: ("Factor: 14x + 21", "7(2x + 3)"),
            lambda: ("Are x + x + x and 3x equivalent?", "Yes"),
            lambda: ("Simplify: 11x - 6x + x", "6x"),
            lambda: ("Factor: 16x + 24", "8(2x + 3)"),
            lambda: ("Are 2x + 3x and 5x equivalent?", "Yes"),
            lambda: ("Simplify: 12x - 7x - 2x", "3x"),
            lambda: ("Factor: 18x + 27", "9(2x + 3)"),
            lambda: ("Are 4(x + 1) and 4x + 4 equivalent?", "Yes"),
            lambda: ("Simplify: 15x - 8x + 2x", "9x"),
            lambda: ("Factor: 20x + 30", "10(2x + 3)"),
        ]

        banks["6.EE.B.5"] = [
            lambda: ("Is x = 3 a solution to 2x + 1 = 7?", "Yes"),
            lambda: ("Check if x = 2 satisfies: 4x = 8", "Yes"),
            lambda: ("Is y = 4 a solution to 3y - 2 = 10?", "Yes"),
            lambda: ("Is n = 5 a solution to n + 8 = 12?", "No"),
            lambda: ("Is x = 6 a solution to x - 3 = 3?", "Yes"),
            lambda: ("Check if y = 3 satisfies: 5y = 15", "Yes"),
            lambda: ("Is n = 7 a solution to 2n + 1 = 15?", "Yes"),
            lambda: ("Is x = 4 a solution to 3x = 11?", "No"),
            lambda: ("Check if m = 2 satisfies: 6m - 4 = 8", "Yes"),
            lambda: ("Is y = 5 a solution to y + 7 = 13?", "No"),
            lambda: ("Is x = 8 a solution to x/2 = 4?", "Yes"),
            lambda: ("Check if n = 3 satisfies: 4n + 2 = 14", "Yes"),
            lambda: ("Is m = 6 a solution to 2m - 5 = 7?", "Yes"),
            lambda: ("Is x = 10 a solution to x - 4 = 6?", "Yes"),
            lambda: ("Check if y = 2 satisfies: 7y = 14", "Yes"),
            lambda: ("Is n = 4 a solution to 3n + 3 = 16?", "No"),
            lambda: ("Is x = 5 a solution to 2x - 3 = 7?", "Yes"),
            lambda: ("Check if m = 3 satisfies: 5m = 16", "No"),
            lambda: ("Is y = 6 a solution to y/3 = 2?", "Yes"),
            lambda: ("Is n = 9 a solution to n - 5 = 4?", "Yes"),
            lambda: ("Check if x = 7 satisfies: 3x - 1 = 20", "Yes"),
            lambda: ("Is m = 4 a solution to 4m + 2 = 18?", "Yes"),
            lambda: ("Is y = 8 a solution to 2y = 17?", "No"),
            lambda: ("Check if n = 5 satisfies: n + 10 = 15", "Yes"),
        ]

        banks["6.EE.B.6"] = [
            lambda: ("Express: '3 more than n'", "n + 3"),
            lambda: ("Express: 'Half of a number'", "n/2"),
            lambda: ("Express: 'Five less than x'", "x - 5"),
            lambda: ("Express: 'Twice a number'", "2n"),
            lambda: ("Express: 'Seven more than m'", "m + 7"),
            lambda: ("Express: 'One third of y'", "y/3"),
            lambda: ("Express: 'Eight less than p'", "p - 8"),
            lambda: ("Express: 'Triple a number'", "3n"),
            lambda: ("Express: 'Four times x'", "4x"),
            lambda: ("Express: 'Ten decreased by n'", "10 - n"),
            lambda: ("Express: 'The sum of x and 5'", "x + 5"),
            lambda: ("Express: 'The quotient of m and 4'", "m/4"),
            lambda: ("Express: 'Six more than twice n'", "2n + 6"),
            lambda: ("Express: 'The product of 5 and y'", "5y"),
            lambda: ("Express: 'Nine less than three times x'", "3x - 9"),
            lambda: ("Express: 'One fourth of p'", "p/4"),
            lambda: ("Express: 'The difference of n and 7'", "n - 7"),
            lambda: ("Express: 'Twelve divided by x'", "12/x"),
            lambda: ("Express: 'The sum of m and m'", "2m"),
            lambda: ("Express: 'Five times y minus 2'", "5y - 2"),
            lambda: ("Express: 'A number increased by 6'", "n + 6"),
            lambda: ("Express: 'Half of x plus 3'", "x/2 + 3"),
            lambda: ("Express: 'Double a number minus 4'", "2n - 4"),
            lambda: ("Express: 'The product of 7 and n'", "7n"),
        ]

        banks["6.EE.B.7"] = [
            lambda: ("Solve: x + 5 = 12", "7"),
            lambda: ("Solve: 3x = 21", "7"),
            lambda: ("Solve: x/4 = 6", "24"),
            lambda: ("Solve: x - 8 = 15", "23"),
            lambda: ("Solve: 5x = 35", "7"),
            lambda: ("Solve: x/3 = 9", "27"),
            lambda: ("Solve: x + 9 = 28", "19"),
            lambda: ("Solve: 4x = 32", "8"),
            lambda: ("Solve: x - 6 = 14", "20"),
            lambda: ("Solve: 2x = 18", "9"),
            lambda: ("Solve: x/5 = 7", "35"),
            lambda: ("Solve: x + 11 = 30", "19"),
            lambda: ("Solve: 6x = 42", "7"),
            lambda: ("Solve: x - 10 = 25", "35"),
            lambda: ("Solve: x/2 = 12", "24"),
            lambda: ("Solve: 7x = 49", "7"),
            lambda: ("Solve: x + 15 = 40", "25"),
            lambda: ("Solve: x - 12 = 18", "30"),
            lambda: ("Solve: 8x = 64", "8"),
            lambda: ("Solve: x/6 = 8", "48"),
            lambda: ("Solve: 9x = 63", "7"),
            lambda: ("Solve: x + 20 = 45", "25"),
            lambda: ("Solve: x - 15 = 30", "45"),
            lambda: ("Solve: 10x = 80", "8"),
        ]

        banks["6.EE.C.9"] = [
            lambda: ("If y = 2x, and x = 3, find y", "6"),
            lambda: ("If y = x + 5, and y = 12, find x", "7"),
            lambda: ("If y = 3x, and x = 4, find y", "12"),
            lambda: ("If y = x - 2, and x = 10, find y", "8"),
            lambda: ("If y = 4x, and x = 5, find y", "20"),
            lambda: ("If y = x + 8, and y = 15, find x", "7"),
            lambda: ("If y = 5x, and x = 3, find y", "15"),
            lambda: ("If y = x - 4, and x = 12, find y", "8"),
            lambda: ("If y = 2x + 1, and x = 4, find y", "9"),
            lambda: ("If y = x + 10, and y = 25, find x", "15"),
            lambda: ("If y = 6x, and x = 2, find y", "12"),
            lambda: ("If y = x - 5, and x = 20, find y", "15"),
            lambda: ("If y = 3x + 2, and x = 3, find y", "11"),
            lambda: ("If y = x/2, and x = 14, find y", "7"),
            lambda: ("If y = 7x, and x = 3, find y", "21"),
            lambda: ("If y = x + 12, and y = 30, find x", "18"),
            lambda: ("If y = 2x - 3, and x = 6, find y", "9"),
            lambda: ("If y = x/3, and x = 21, find y", "7"),
            lambda: ("If y = 4x + 1, and x = 2, find y", "9"),
            lambda: ("If y = x - 7, and x = 15, find y", "8"),
            lambda: ("If y = 8x, and x = 2, find y", "16"),
            lambda: ("If y = x + 15, and y = 35, find x", "20"),
            lambda: ("If y = 5x - 2, and x = 3, find y", "13"),
            lambda: ("If y = x/4, and x = 28, find y", "7"),
        ]
        
        banks["6.G.A.1"] = [
            lambda: ("Triangle area: base = 8, height = 6", "24"),
            lambda: ("Rectangle area: length = 7, width = 9", "63"),
            lambda: ("Triangle area: base = 10, height = 4", "20"),
            lambda: ("Parallelogram: base = 10, height = 6", "60"),
            lambda: ("Trapezoid: bases 6 and 10, height 4", "32"),
            lambda: ("Triangle area: base = 12, height = 5", "30"),
            lambda: ("Rectangle area: length = 8, width = 6", "48"),
            lambda: ("Triangle area: base = 14, height = 4", "28"),
            lambda: ("Parallelogram: base = 12, height = 5", "60"),
            lambda: ("Trapezoid: bases 8 and 12, height 5", "50"),
            lambda: ("Triangle area: base = 16, height = 3", "24"),
            lambda: ("Rectangle area: length = 11, width = 4", "44"),
            lambda: ("Triangle area: base = 6, height = 8", "24"),
            lambda: ("Parallelogram: base = 15, height = 4", "60"),
            lambda: ("Trapezoid: bases 5 and 9, height 6", "42"),
            lambda: ("Triangle area: base = 18, height = 4", "36"),
            lambda: ("Rectangle area: length = 13, width = 5", "65"),
            lambda: ("Triangle area: base = 20, height = 3", "30"),
            lambda: ("Parallelogram: base = 8, height = 7", "56"),
            lambda: ("Trapezoid: bases 7 and 11, height 4", "36"),
            lambda: ("Square area: side = 9", "81"),
            lambda: ("Triangle area: base = 15, height = 6", "45"),
            lambda: ("Rectangle area: length = 12, width = 7", "84"),
            lambda: ("Parallelogram: base = 14, height = 3", "42"),
        ]

        banks["6.G.A.2"] = [
            lambda: ("Volume of box: 4 × 3 × 5", "60"),
            lambda: ("Cube with edge 6. Volume?", "216"),
            lambda: ("Prism: 8 × 2 × 3. Volume?", "48"),
            lambda: ("Cube with edge 4. Volume?", "64"),
            lambda: ("Box: 5 × 5 × 4. Volume?", "100"),
            lambda: ("Volume of box: 6 × 4 × 3", "72"),
            lambda: ("Cube with edge 5. Volume?", "125"),
            lambda: ("Prism: 7 × 3 × 4. Volume?", "84"),
            lambda: ("Cube with edge 3. Volume?", "27"),
            lambda: ("Box: 10 × 2 × 5. Volume?", "100"),
            lambda: ("Volume of box: 8 × 3 × 3", "72"),
            lambda: ("Cube with edge 7. Volume?", "343"),
            lambda: ("Prism: 6 × 5 × 2. Volume?", "60"),
            lambda: ("Cube with edge 2. Volume?", "8"),
            lambda: ("Box: 9 × 4 × 2. Volume?", "72"),
            lambda: ("Volume of box: 5 × 6 × 3", "90"),
            lambda: ("Cube with edge 8. Volume?", "512"),
            lambda: ("Prism: 4 × 4 × 6. Volume?", "96"),
            lambda: ("Box: 7 × 5 × 2. Volume?", "70"),
            lambda: ("Volume of box: 12 × 3 × 2", "72"),
            lambda: ("Cube with edge 10. Volume?", "1000"),
            lambda: ("Prism: 11 × 2 × 3. Volume?", "66"),
            lambda: ("Box: 8 × 4 × 3. Volume?", "96"),
            lambda: ("Volume of box: 15 × 2 × 2", "60"),
        ]

        banks["6.G.A.3"] = [
            lambda: ("Distance from (2,3) to (2,7)", "4"),
            lambda: ("Distance from (1,5) to (6,5)", "5"),
            lambda: ("Distance from (0,0) to (3,4)", "5"),
            lambda: ("Area of rectangle: (0,0), (4,0), (4,3), (0,3)", "12"),
            lambda: ("Distance from (3,2) to (3,8)", "6"),
            lambda: ("Distance from (2,4) to (7,4)", "5"),
            lambda: ("Distance from (0,0) to (5,0)", "5"),
            lambda: ("Area of rectangle: (1,1), (5,1), (5,4), (1,4)", "12"),
            lambda: ("Distance from (4,1) to (4,9)", "8"),
            lambda: ("Distance from (3,6) to (10,6)", "7"),
            lambda: ("Distance from (0,0) to (0,8)", "8"),
            lambda: ("Area of rectangle: (2,2), (7,2), (7,5), (2,5)", "15"),
            lambda: ("Distance from (5,3) to (5,12)", "9"),
            lambda: ("Distance from (1,7) to (11,7)", "10"),
            lambda: ("Distance from (0,0) to (6,8)", "10"),
            lambda: ("Area of rectangle: (0,0), (6,0), (6,4), (0,4)", "24"),
            lambda: ("Distance from (2,1) to (2,11)", "10"),
            lambda: ("Distance from (4,3) to (12,3)", "8"),
            lambda: ("Distance from (0,0) to (8,0)", "8"),
            lambda: ("Area of rectangle: (3,3), (8,3), (8,7), (3,7)", "20"),
            lambda: ("Distance from (1,2) to (1,14)", "12"),
            lambda: ("Distance from (5,8) to (15,8)", "10"),
            lambda: ("Distance from (0,0) to (9,12)", "15"),
            lambda: ("Area of rectangle: (1,2), (7,2), (7,8), (1,8)", "36"),
        ]

        banks["6.G.A.4"] = [
            lambda: ("How many faces does a cube have?", "6"),
            lambda: ("Surface area of cube with edge 4", "96"),
            lambda: ("How many edges in rectangular prism?", "12"),
            lambda: ("How many vertices in triangular prism?", "6"),
            lambda: ("How many faces does a rectangular prism have?", "6"),
            lambda: ("Surface area of cube with edge 3", "54"),
            lambda: ("How many edges in a cube?", "12"),
            lambda: ("How many vertices in a cube?", "8"),
            lambda: ("How many faces does a triangular prism have?", "5"),
            lambda: ("Surface area of cube with edge 5", "150"),
            lambda: ("How many edges in triangular pyramid?", "6"),
            lambda: ("How many vertices in rectangular prism?", "8"),
            lambda: ("How many faces does a square pyramid have?", "5"),
            lambda: ("Surface area of cube with edge 2", "24"),
            lambda: ("How many edges in square pyramid?", "8"),
            lambda: ("How many vertices in triangular pyramid?", "4"),
            lambda: ("Net of cube: how many squares?", "6"),
            lambda: ("Surface area of cube with edge 6", "216"),
            lambda: ("How many faces does triangular pyramid have?", "4"),
            lambda: ("How many vertices in square pyramid?", "5"),
            lambda: ("Surface area of cube with edge 7", "294"),
            lambda: ("Net of rectangular prism: how many rectangles?", "6"),
            lambda: ("How many edges in triangular prism?", "9"),
            lambda: ("Surface area of cube with edge 8", "384"),
        ]

        banks["6.SP.A.1"] = [
            lambda: ("Is 'What is your height?' statistical?", "Yes"),
            lambda: ("Is 'What is 2+2?' statistical?", "No"),
            lambda: ("Is 'How many pets?' statistical?", "Yes"),
            lambda: ("Is 'Capital of France?' statistical?", "No"),
            lambda: ("Is 'How old are students?' statistical?", "Yes"),
            lambda: ("Is 'What is 5×3?' statistical?", "No"),
            lambda: ("Is 'Test scores of class?' statistical?", "Yes"),
            lambda: ("Is 'Your birthday date?' statistical?", "No"),
            lambda: ("Is 'How many siblings?' statistical?", "Yes"),
            lambda: ("Is 'What is 10÷2?' statistical?", "No"),
            lambda: ("Is 'Favorite color?' statistical?", "Yes"),
            lambda: ("Is 'Square root of 16?' statistical?", "No"),
            lambda: ("Is 'Hours of sleep?' statistical?", "Yes"),
            lambda: ("Is 'Definition of noun?' statistical?", "No"),
            lambda: ("Is 'Shoe sizes in class?' statistical?", "Yes"),
            lambda: ("Is 'Who wrote Hamlet?' statistical?", "No"),
            lambda: ("Is 'Grade on last test?' statistical?", "Yes"),
            lambda: ("Is 'Days in week?' statistical?", "No"),
            lambda: ("Is 'Heights of trees?' statistical?", "Yes"),
            lambda: ("Is 'Spelling of cat?' statistical?", "No"),
            lambda: ("Is 'Weight of backpacks?' statistical?", "Yes"),
            lambda: ("Is 'Your exact age?' statistical?", "No"),
            lambda: ("Is 'Time to run mile?' statistical?", "Yes"),
            lambda: ("Is 'Formula for area?' statistical?", "No"),
        ]

        banks["6.SP.A.2"] = [
            lambda: ("What describes data spread?", "Range"),
            lambda: ("What describes data center?", "Mean"),
            lambda: ("Measure least affected by outliers?", "Median"),
            lambda: ("Shape with tail on right?", "Right-skewed"),
            lambda: ("What shows data variability?", "Range"),
            lambda: ("Most common value?", "Mode"),
            lambda: ("Shape with tail on left?", "Left-skewed"),
            lambda: ("Middle value when ordered?", "Median"),
            lambda: ("Average of all values?", "Mean"),
            lambda: ("Symmetric distribution shape?", "Bell-shaped"),
            lambda: ("Difference between max and min?", "Range"),
            lambda: ("Value that appears most?", "Mode"),
            lambda: ("Sum divided by count?", "Mean"),
            lambda: ("Distribution with one peak?", "Unimodal"),
            lambda: ("50th percentile?", "Median"),
            lambda: ("Distribution with two peaks?", "Bimodal"),
            lambda: ("Measure of center for skewed data?", "Median"),
            lambda: ("Spread of middle 50%?", "IQR"),
            lambda: ("Q2 is also called?", "Median"),
            lambda: ("Distribution with outliers affects?", "Mean"),
            lambda: ("Flat distribution shape?", "Uniform"),
            lambda: ("Measure for categorical data?", "Mode"),
            lambda: ("Q3 - Q1 equals?", "IQR"),
            lambda: ("Center for symmetric data?", "Mean"),
        ]

        banks["6.SP.B.4"] = [
            lambda: ("Best graph for categories?", "Bar graph"),
            lambda: ("Best graph for change over time?", "Line graph"),
            lambda: ("Graph for part-to-whole?", "Pie chart"),
            lambda: ("Shows distribution shape?", "Histogram"),
            lambda: ("Graph for comparing groups?", "Bar graph"),
            lambda: ("Graph for continuous data?", "Histogram"),
            lambda: ("Shows relationship between variables?", "Scatter plot"),
            lambda: ("Graph for frequency of categories?", "Bar graph"),
            lambda: ("Display for numerical data distribution?", "Box plot"),
            lambda: ("Graph showing trends?", "Line graph"),
            lambda: ("Chart for percentages of whole?", "Pie chart"),
            lambda: ("Graph with bars touching?", "Histogram"),
            lambda: ("Display for five-number summary?", "Box plot"),
            lambda: ("Graph with bars separated?", "Bar graph"),
            lambda: ("Shows correlation?", "Scatter plot"),
            lambda: ("Graph for time series data?", "Line graph"),
            lambda: ("Chart for comparing parts?", "Pie chart"),
            lambda: ("Graph showing frequency distribution?", "Histogram"),
            lambda: ("Display showing median and quartiles?", "Box plot"),
            lambda: ("Graph for discrete categories?", "Bar graph"),
            lambda: ("Shows pattern in paired data?", "Scatter plot"),
            lambda: ("Graph for stock prices over time?", "Line graph"),
            lambda: ("Display for survey results?", "Bar graph"),
            lambda: ("Graph showing data clusters?", "Scatter plot"),
        ]

        banks["6.SP.B.5"] = [
            lambda: ("Find mean: 4, 6, 8, 10, 12", "8"),
            lambda: ("Find median: 3, 5, 7, 9, 11", "7"),
            lambda: ("Find mode: 2, 3, 3, 5, 7", "3"),
            lambda: ("Find range: 12, 18, 23, 9, 15", "14"),
            lambda: ("Find mean: 5, 10, 15, 20", "12.5"),
            lambda: ("Find median: 2, 4, 6, 8", "5"),
            lambda: ("Find mode: 4, 4, 5, 5, 5, 6", "5"),
            lambda: ("Find range: 25, 30, 15, 20", "15"),
            lambda: ("Find mean: 10, 20, 30", "20"),
            lambda: ("Find median: 1, 3, 5, 7, 9, 11", "6"),
            lambda: ("Find mode: 1, 2, 2, 3, 3, 3", "3"),
            lambda: ("Find range: 45, 50, 35, 40", "15"),
            lambda: ("Find mean: 6, 9, 12, 15", "10.5"),
            lambda: ("Find median: 10, 20, 30, 40, 50", "30"),
            lambda: ("Find mode: 7, 7, 8, 9, 9, 9", "9"),
            lambda: ("Find range: 100, 85, 95, 90", "15"),
            lambda: ("Find mean: 2, 4, 6, 8, 10", "6"),
            lambda: ("Find median: 15, 20, 25, 30", "22.5"),
            lambda: ("Find mode: 10, 10, 10, 15, 20", "10"),
            lambda: ("Find range: 78, 82, 85, 75", "10"),
            lambda: ("Find mean: 12, 18, 24", "18"),
            lambda: ("Find median: 5, 10, 15, 20, 25", "15"),
            lambda: ("Find mode: 6, 6, 7, 7, 7, 8", "7"),
            lambda: ("Find range: 55, 65, 60, 50", "15"),
        ]
        
        # 7th Grade Standards - FIXED ANSWERS AND MORE VARIETY
        banks["7.RP.A.1"] = [
            lambda: ("If 3/4 pound costs $3, cost per pound?", "4"),
            lambda: ("Speed: 1/2 mile in 1/4 hour. mph?", "2"),
            lambda: ("2 1/2 cups flour for 5 cookies. Cups per cookie?", "1/2"),
            lambda: ("3/5 mile in 1/5 hour. Miles per hour?", "3"),
            lambda: ("If 2/3 yard costs $4, cost per yard?", "6"),
            lambda: ("1/3 hour to travel 2 miles. Miles per hour?", "6"),
            lambda: ("3/4 gallon fills 3 containers. Gallons per container?", "1/4"),
            lambda: ("5/6 pound costs $5, cost per pound?", "6"),
            lambda: ("Walk 3/4 mile in 1/2 hour. Speed in mph?", "1.5"),
            lambda: ("2/5 of work done in 1/10 hour. Hours for full job?", "1/4"),
        ]
        
        banks["7.RP.A.2"] = [
            lambda: ("Is y = 3x proportional?", "Yes"),
            lambda: ("Is y = 3x + 2 proportional?", "No"),
            lambda: ("In y = 5x, constant of proportionality?", "5"),
            lambda: ("Graph through (0,0) and (2,8). Find k", "4"),
            lambda: ("Is y = x/2 proportional?", "Yes"),
            lambda: ("Graph through (0,0) and (3,15). Find k", "5"),
            lambda: ("Is y = 2x - 1 proportional?", "No"),
            lambda: ("In y = 7x, what is k?", "7"),
            lambda: ("Is y = 4x proportional (passes through origin)?", "Yes"),
            lambda: ("In y = 9x, find constant k", "9"),
        ]
        
        banks["7.RP.A.3"] = [
            lambda: ("Scale 1:20. Model is 5 cm. Actual?", "100"),
            lambda: ("15 is what percent of 60?", "25"),
            lambda: ("Map: 1 inch = 25 miles. 3 inches?", "75"),
            lambda: ("Recipe for 4 uses 3 cups. For 8?", "6"),
            lambda: ("20% of what number is 15?", "75"),
            lambda: ("Scale 1:50. Actual is 200 cm. Model?", "4"),
            lambda: ("12 is what percent of 40?", "30"),
            lambda: ("Map: 2 cm = 10 km. 5 cm?", "25"),
            lambda: ("25% of 120 is?", "30"),
            lambda: ("40% discount on $50. Sale price?", "30"),
        ]
        
        banks["7.NS.A.1"] = [
            lambda: ("(-5) + (-3)", "-8"),
            lambda: ("(-10) - (-4)", "-6"),
            lambda: ("7 + (-12)", "-5"),
            lambda: ("(-15) + 20", "5"),
            lambda: ("Start at -3, move 8 right", "5"),
            lambda: ("(-8) + 3", "-5"),
            lambda: ("12 - 20", "-8"),
            lambda: ("(-7) - 5", "-12"),
            lambda: ("15 + (-18)", "-3"),
            lambda: ("(-25) + 30", "5"),
        ]
        
        banks["7.NS.A.2"] = [
            lambda: ("(-4) × 5", "-20"),
            lambda: ("(-20) ÷ (-4)", "5"),
            lambda: ("(-3) × (-7)", "21"),
            lambda: ("24 ÷ (-6)", "-4"),
            lambda: ("(-2)³", "-8"),
            lambda: ("(-5) × 6", "-30"),
            lambda: ("(-36) ÷ 9", "-4"),
            lambda: ("(-8) × (-3)", "24"),
            lambda: ("45 ÷ (-9)", "-5"),
            lambda: ("(-7) × 4", "-28"),
        ]
        
        banks["7.NS.A.3"] = [
            lambda: ("Temperature drops 3° per hour for 5 hours. Change?", "-15"),
            lambda: ("Stock loses $2 per day for 4 days. Total change?", "-8"),
            lambda: ("Football: +8, -3, -2, +5. Net yards?", "8"),
            lambda: ("Submarine at -200 ft, descends 150 ft. New depth?", "-350"),
            lambda: ("Debt of $50, pays back $20. Balance?", "-30"),
            lambda: ("Elevator: starts floor 10, down 12 floors", "-2"),
            lambda: ("Account: $100, spends $45, then $65. Balance?", "-10"),
            lambda: ("Temperature: -5°C rises 8°. New temp?", "3"),
            lambda: ("Diver at -30 ft, descends 25 ft more", "-55"),
            lambda: ("Account: -$20, deposits $15. New balance?", "-5"),
        ]
        
        banks["7.EE.A.1"] = [
            lambda: ("Factor: 6x + 12", "6(x + 2)"),
            lambda: ("Expand: 3(x + 4)", "3x + 12"),
            lambda: ("Simplify: 4x + 2x + x", "7x"),
            lambda: ("Factor: 15x - 20", "5(3x - 4)"),
            lambda: ("Expand: 4(2x - 3)", "8x - 12"),
            lambda: ("Factor: 8x + 16", "8(x + 2)"),
            lambda: ("Expand: 5(x - 2)", "5x - 10"),
            lambda: ("Simplify: 3x + 4x - 2x", "5x"),
            lambda: ("Factor: 12x + 18", "6(2x + 3)"),
            lambda: ("Expand: 2(3x + 5)", "6x + 10"),
        ]
        
        banks["7.EE.A.2"] = [
            lambda: ("Simplify: 4x - 2x + 3x", "5x"),
            lambda: ("Combine: 2x + 3y + 4x - y", "6x + 2y"),
            lambda: ("Coefficient of x in 7x - 3?", "7"),
            lambda: ("Simplify: 5x - x + 2x", "6x"),
            lambda: ("Combine: 3x + 2 + 2x - 1", "5x + 1"),
            lambda: ("Simplify: 8x - 5x", "3x"),
            lambda: ("Combine: x + 2x + 3x", "6x"),
            lambda: ("Coefficient of x in -4x + 5?", "-4"),
            lambda: ("Simplify: 10x - 7x + x", "4x"),
            lambda: ("Combine: 5y - 2y + y", "4y"),
        ]
        
        banks["7.EE.B.3"] = [
            lambda: ("Solve: 2x + 3 = 11", "4"),
            lambda: ("Solve: 3x - 7 = 8", "5"),
            lambda: ("Solve: 5x + 2 = 27", "5"),
            lambda: ("Solve: 4x - 9 = 15", "6"),
            lambda: ("Solve: x/3 + 2 = 7", "15"),
            lambda: ("Solve: 2x + 5 = 17", "6"),
            lambda: ("Solve: 3x - 4 = 11", "5"),
            lambda: ("Solve: x/2 + 3 = 8", "10"),
            lambda: ("Solve: 6x - 7 = 17", "4"),
            lambda: ("Solve: 2x - 3 = 9", "6"),
        ]
        
        banks["7.EE.B.4"] = [
            lambda: ("Tickets cost $8 each. Cost for 7?", "56"),
            lambda: ("Drive 60 mph for 3 hours. Distance?", "180"),
            lambda: ("Save $15/week. Weeks to save $180?", "12"),
            lambda: ("Phone: $40 base + $0.10 per text. Cost for 150 texts?", "55"),
            lambda: ("Rental: $25/day. Cost for 4 days?", "100"),
            lambda: ("Earn $12/hour. Hours to earn $96?", "8"),
            lambda: ("Pizza: $10 each. Cost for 6?", "60"),
            lambda: ("Subscription: $8/month. Cost for year?", "96"),
            lambda: ("Gas: $3/gallon. Gallons for $45?", "15"),
            lambda: ("Books: $7 each. Cost for 8 books?", "56"),
        ]
        
        banks["7.SP.A.1"] = [
            lambda: ("What measure is affected by outliers?", "Mean"),
            lambda: ("Middle value when ordered?", "Median"),
            lambda: ("Is 'Heights of 7th graders' statistical?", "Yes"),
            lambda: ("Measure of spread for middle 50%?", "IQR"),
        ]
        
        banks["7.SP.A.2"] = [
            lambda: ("Can 30 students represent 600?", "Yes"),
            lambda: ("What makes sample representative?", "Random"),
            lambda: ("Is surveying only honors students biased?", "Yes"),
            lambda: ("Population if you survey 10% of city?", "Entire city"),
        ]
        
        banks["7.SP.B.3"] = [
            lambda: ("Can datasets have same mean, different spread?", "Yes"),
            lambda: ("What shows consistency: MAD of 2 or 10?", "2"),
            lambda: ("What do overlapping box plots suggest?", "Similar"),
            lambda: ("Can different shapes have same center?", "Yes"),
        ]
        
        banks["7.SP.C.5"] = [
            lambda: ("Probability of heads on fair coin?", "0.5"),
            lambda: ("Bag: 3 red, 7 blue. P(red)?", "0.3"),
            lambda: ("Die: P(getting 3 or less)?", "0.5"),
            lambda: ("P(impossible event)?", "0"),
        ]
        
        banks["7.SP.C.7"] = [
            lambda: ("Coin flipped 100 times. Expected heads?", "50"),
            lambda: ("Outcomes when flipping 3 coins?", "8"),
            lambda: ("Is 520 heads in 1000 flips unusual?", "No"),
            lambda: ("Theoretical P(heads)?", "0.5"),
        ]
        
        return banks
    
    def _ratio_problem(self, a, b):
        """Generate ratio simplification problem"""
        g = gcd(a, b)
        return (f"Simplify the ratio {a}:{b}", f"{a//g}:{b//g}")
    
    def _get_riddle_for_length(self, length):
        """Get a riddle with exact length"""
        if length in self.riddle_bank and self.riddle_bank[length]:
            return random.choice(self.riddle_bank[length])
        # Fallback for lengths not in bank
        return (f"Math riddle ({length} letters)", "M" * length, "M" * length)
    
    def _extract_numeric(self, answer):
        """Extract clean numeric value from answer"""
        answer_str = str(answer)
        
        # Handle ratios specially
        if ":" in answer_str:
            return answer_str
        
        # Remove units
        units_to_remove = ["°F", "°C", "°", "$", "%", "mph", "km", "cm", "m", "ft"]
        for unit in units_to_remove:
            answer_str = answer_str.replace(unit, "")
        
        return answer_str.strip()
    
    def _create_full_mapping(self, letter_to_answer, used_answers):
        """Create complete A-Z mapping with consistent formatting"""
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        mapping = {}
        
        # Check answer patterns
        has_decimals = any('.' in str(a) for a in used_answers)
        has_negatives = any(str(a).startswith('-') for a in used_answers)
        has_ratios = any(':' in str(a) for a in used_answers)
        
        # Add known letter mappings
        for letter, answer in letter_to_answer.items():
            mapping[letter] = answer
        
        # Fill remaining letters with consistent format
        for letter in alphabet:
            if letter not in mapping:
                if has_ratios:
                    a = random.randint(1, 9)
                    b = random.randint(1, 9)
                    value = f"{a}:{b}"
                elif has_decimals:
                    value = f"{random.uniform(1, 50):.1f}"
                elif has_negatives:
                    value = str(random.randint(-50, 50))
                else:
                    value = str(random.randint(1, 100))
                
                # Ensure unique value
                while value in used_answers:
                    if has_ratios:
                        a = random.randint(1, 9)
                        b = random.randint(1, 9)
                        value = f"{a}:{b}"
                    else:
                        value = str(random.randint(1, 100))
                
                mapping[letter] = value
                used_answers.add(value)
        
        return mapping
    

    
    def generate_preview(self, standard_code, num_problems, use_riddles):
        """Generate preview of problems with optional riddle"""
        if standard_code not in self.problem_banks:
            return None, None
        
        self.used_problems = []
        
        can_use_riddles = standard_code in RIDDLE_COMPATIBLE_STANDARDS
        
        try:
            if use_riddles and can_use_riddles and num_problems >= 3:
                riddle = self._get_riddle_for_length(num_problems)
                problems = self._generate_problems_with_riddle(standard_code, num_problems, riddle)
                
                self.preview_state = {
                    'problems': problems,
                    'riddle': riddle,
                    'letter_mapping': self.current_letter_mapping,
                    'standard_code': standard_code
                }
                
                return problems, riddle
            else:
                problems = self._generate_problems_no_riddle(standard_code, num_problems)
                
                self.preview_state = {
                    'problems': problems,
                    'riddle': None,
                    'letter_mapping': None,
                    'standard_code': standard_code
                }
                
                return problems, None
        except ValueError as e:
            # If we can't generate enough problems, return error
            raise ValueError(str(e))
    
    def _generate_problems_with_riddle(self, standard_code, num_problems, riddle):
        """Generate problems matching riddle answer letters - NO DUPLICATES, NO FALLBACKS"""
        if standard_code not in self.problem_banks:
            raise ValueError(f"No problem bank for standard {standard_code}")
            
        problems = []
        generators = self.problem_banks[standard_code].copy()
        riddle_answer = riddle[2].upper()
        
        # Track all used problems to prevent duplicates
        used_problem_texts = set()
        
        # Create letter to answer mapping
        unique_letters = list(dict.fromkeys(riddle_answer))
        letter_to_answer = {}
        used_answers = set()
        
        # First, generate all possible problems from this standard
        all_possible_problems = []
        for generator in generators:
            # Try to generate multiple variations
            for _ in range(5):  # Try each generator up to 5 times
                try:
                    problem, answer = generator()
                    clean_answer = self._extract_numeric(answer)
                    if problem not in [p[0] for p in all_possible_problems]:
                        all_possible_problems.append((problem, answer, clean_answer))
                except:
                    continue
        
        # Check if we have enough variety
        if len(all_possible_problems) < num_problems:
            raise ValueError(f"Not enough unique problems available for standard {standard_code}. Need {num_problems}, but only have {len(all_possible_problems)} unique problems.")
        
        # Shuffle the pool
        random.shuffle(all_possible_problems)
        
        # Map unique letters to unique answers from actual problems
        for letter in unique_letters:
            found = False
            for problem, answer, clean_answer in all_possible_problems:
                if clean_answer not in used_answers:
                    letter_to_answer[letter] = clean_answer
                    used_answers.add(clean_answer)
                    found = True
                    break
            
            if not found:
                # Cannot generate valid riddle with available problems
                raise ValueError(f"Cannot generate valid riddle mapping for standard {standard_code}. Not enough unique answers.")
        
        # Now generate problems for each position in riddle
        for position, letter in enumerate(riddle_answer):
            target_answer = letter_to_answer[letter]
            found = False
            
            # Find a problem with matching answer that hasn't been used
            for problem, answer, clean_answer in all_possible_problems:
                if clean_answer == target_answer and problem not in used_problem_texts:
                    problems.append((problem, answer))
                    used_problem_texts.add(problem)
                    found = True
                    break
            
            if not found:
                # Try to find any unused problem and use with adjusted answer
                for problem, _, _ in all_possible_problems:
                    if problem not in used_problem_texts:
                        problems.append((problem, target_answer))
                        used_problem_texts.add(problem)
                        found = True
                        break
            
            if not found:
                # Cannot complete worksheet - not enough unique problems
                raise ValueError(f"Cannot generate {num_problems} unique problems for standard {standard_code}. Consider reducing the number of problems or disabling riddles for this standard.")
        
        # Create full letter mapping
        self.current_letter_mapping = self._create_full_mapping(letter_to_answer, used_answers)
        
        return problems
    
    def _generate_problems_no_riddle(self, standard_code, num_problems):
        """Generate problems without riddle constraint - NO DUPLICATES, NO FALLBACKS"""
        if standard_code not in self.problem_banks:
            raise ValueError(f"No problem bank for standard {standard_code}")
            
        problems = []
        generators = self.problem_banks[standard_code].copy()
        used_problem_texts = set()
        
        # Generate all possible problems from this standard first
        all_possible_problems = []
        for generator in generators:
            # Try each generator multiple times for variations
            for _ in range(5):
                try:
                    problem, answer = generator()
                    if problem not in [p[0] for p in all_possible_problems]:
                        all_possible_problems.append((problem, answer))
                except:
                    continue
        
        # Check if we have enough variety
        if len(all_possible_problems) < num_problems:
            raise ValueError(f"Not enough unique problems available for standard {standard_code}. Need {num_problems}, but only have {len(all_possible_problems)} unique problems.")
        
        # Shuffle for randomness
        random.shuffle(all_possible_problems)
        
        # Select unique problems
        for problem, answer in all_possible_problems:
            if problem not in used_problem_texts:
                problems.append((problem, answer))
                used_problem_texts.add(problem)
                if len(problems) >= num_problems:
                    break
        
        return problems[:num_problems]
    
    def generate_worksheet_from_preview(self, grade, worksheet_num=1):
        """Generate worksheet PDFs from stored preview"""
        if not self.preview_state:
            return None, None
        
        state = self.preview_state
        standard_code = state['standard_code']
        
        # Find standard name
        standard_name = ""
        for category, standards in COMMON_CORE_STANDARDS[grade].items():
            if standard_code in standards:
                standard_name = standards[standard_code]
                break
        
        self.current_riddle = state['riddle']
        self.current_letter_mapping = state['letter_mapping'] or {}
        
        return self._create_pdf_files(
            state['problems'],
            standard_code,
            standard_name,
            grade,
            worksheet_num,
            state['riddle'] is not None
        )
    
    def _create_pdf_files(self, problems, standard_code, standard_name, grade, worksheet_num, use_riddles):
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
        
        c.setFont("Helvetica", 11)
        c.drawString(50, height - 90, f"Standard: {standard_code} - {standard_name}")
        c.drawString(50, height - 110, f"Grade: {grade}")
        
        y_pos = height - 140
        
        # Riddle instructions if applicable
        if use_riddles and self.current_riddle and self.current_letter_mapping:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_pos, "Solve each problem. Match answers to letters to decode the riddle!")
            y_pos -= 25
            
            # Letter mapping table
            c.setFont("Helvetica", 9)
            alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for start in range(0, 26, 9):
                line = []
                for i in range(start, min(start + 9, 26)):
                    letter = alphabet[i]
                    value = self.current_letter_mapping.get(letter, "?")
                    line.append(f"{letter}={value}")
                c.drawString(50, y_pos, "  ".join(line))
                y_pos -= 15
            y_pos -= 10
        
        # Problems
        c.setFont("Helvetica", 11)
        for i, (problem, answer) in enumerate(problems):
            if y_pos < 100:
                c.showPage()
                y_pos = height - 50
                c.setFont("Helvetica", 11)
            
            c.drawString(50, y_pos, f"{i+1}. {problem} = _______")
            
            if use_riddles and self.current_riddle:
                c.rect(width - 100, y_pos - 5, 30, 20)
                c.setFont("Helvetica", 11)
            
            y_pos -= 30
        
        # Riddle section
        if use_riddles and self.current_riddle:
            if y_pos < 150:
                c.showPage()
                y_pos = height - 100
            
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos, "RIDDLE:")
            c.setFont("Helvetica", 12)
            c.drawString(50, y_pos - 25, self.current_riddle[0])
            
            y_pos -= 60
            c.drawString(50, y_pos, "Answer:")
            y_pos -= 35
            
            # Answer boxes
            for i in range(len(self.current_riddle[2])):
                x_pos = 50 + (i * 35)
                if x_pos > width - 100:
                    x_pos = 50 + ((i % 12) * 35)
                    if i % 12 == 0 and i > 0:
                        y_pos -= 40
                
                c.rect(x_pos, y_pos, 30, 30)
                c.setFont("Helvetica", 9)
                c.drawString(x_pos + 12, y_pos - 15, str(i + 1))
        
        c.save()
        
        # Create answer key
        answer_buffer = io.BytesIO()
        c = canvas.Canvas(answer_buffer, pagesize=pagesizes.letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Answer Key - Worksheet #{worksheet_num}")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 80, f"Standard: {standard_code} - {standard_name}")
        
        y_pos = height - 110
        c.setFont("Helvetica", 12)
        
        for i, (problem, answer) in enumerate(problems):
            if y_pos < 100:
                c.showPage()
                y_pos = height - 50
                c.setFont("Helvetica", 12)
            
            c.drawString(50, y_pos, f"{i+1}. {answer}")
            
            if use_riddles and self.current_riddle and i < len(self.current_riddle[2]):
                letter = self.current_riddle[2][i]
                c.drawString(250, y_pos, f"→ Letter: {letter}")
            
            y_pos -= 25
        
        if use_riddles and self.current_riddle:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos - 30, f"RIDDLE ANSWER: {self.current_riddle[1]}")
        
        c.save()
        
        worksheet_buffer.seek(0)
        answer_buffer.seek(0)
        
        return worksheet_buffer.getvalue(), answer_buffer.getvalue()

def main():
    st.set_page_config(page_title="Math Worksheet Generator", layout="wide")
    
    st.title("📚 Common Core Math Worksheet Generator")
    st.markdown("Generate math worksheets perfectly aligned to Common Core standards")
    
    # About section
    with st.expander("ℹ️ About This Generator", expanded=True):
        st.markdown("""
        ### Features:
        - **Common Core Aligned**: Every problem matches selected standards
        - **Smart Riddle System**: Engaging riddles for supported standards
        - **No Duplicates**: Unique problems on each worksheet
        - **PDF Generation**: Professional worksheets and answer keys
        - **Bulk Creation**: Generate multiple versions at once
        
        ### How to Use:
        1. Select grade level and standards from sidebar
        2. Configure settings (problems per worksheet, versions)
        3. Preview a sample worksheet
        4. Generate and download all worksheets as ZIP
        """)
    
    # Initialize session state
    if 'generator' not in st.session_state:
        st.session_state.generator = MathWorksheetGenerator()
    if 'generated_files' not in st.session_state:
        st.session_state.generated_files = []
    if 'preview_cache' not in st.session_state:
        st.session_state.preview_cache = {}
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        grade = st.selectbox("Select Grade", ["6th Grade", "7th Grade"])
        
        st.subheader("📋 Select Standards")
        selected_standards = []
        
        for category, standards in COMMON_CORE_STANDARDS[grade].items():
            with st.expander(category):
                for code, desc in standards.items():
                    if st.checkbox(f"{code}: {desc}", key=f"std_{code}"):
                        selected_standards.append((code, desc))
                        if code not in RIDDLE_COMPATIBLE_STANDARDS:
                            st.caption("   ↳ *Riddles not available*")
        
        st.divider()
        
        st.subheader("📝 Settings")
        
        # Track if settings changed
        prev_versions = st.session_state.get('prev_versions', 1)
        prev_problems = st.session_state.get('prev_problems', 8)
        prev_riddles = st.session_state.get('prev_riddles', True)
        
        versions = st.number_input("Versions per Standard", 1, 10, 1)
        num_problems = st.slider("Problems per Worksheet", 3, 20, 8)
        
        can_use_riddles = any(s[0] in RIDDLE_COMPATIBLE_STANDARDS for s in selected_standards)

        if can_use_riddles:
            if num_problems <= 15:
                use_riddles = st.checkbox("Include riddles (where applicable)", True)
            else:
                use_riddles = st.checkbox("Include riddles (where applicable)", False, disabled=True)
                st.error("⚠️ Riddles are only available for worksheets with 15 questions or fewer. Please reduce the number of problems to enable riddles.")
        else:
            use_riddles = False
            st.info("Selected standards don't support riddles")
        
        # Clear preview cache if settings changed
        if (versions != prev_versions or 
            num_problems != prev_problems or 
            use_riddles != prev_riddles):
            st.session_state.preview_cache = {}
            st.session_state.prev_versions = versions
            st.session_state.prev_problems = num_problems
            st.session_state.prev_riddles = use_riddles
        
        st.divider()
        
        download_option = st.radio(
            "Download Format",
            ["Worksheet + Answer Key", "Worksheet Only", "Answer Key Only"]
        )
    
    # Main content area
    if selected_standards:
        st.header("👁️ Preview & Generate")
        
        # Add standard selector if multiple standards selected
        if len(selected_standards) > 1:
            preview_col1, preview_col2, preview_col3 = st.columns([3, 1, 1])
            with preview_col1:
                # Create options with preview indicators
                standard_options = []
                for code, desc in selected_standards:
                    cache_key = f"{code}_{num_problems}_{use_riddles}"
                    has_preview = cache_key in st.session_state.preview_cache
                    indicator = "✓" if has_preview else "○"
                    standard_options.append(f"{indicator} {code}: {desc[:45]}...")
                
                selected_preview_idx = st.selectbox(
                    "Select standard to preview:",
                    range(len(standard_options)),
                    format_func=lambda x: standard_options[x],
                    key="preview_selector"
                )
                preview_standard = selected_standards[selected_preview_idx]
            with preview_col2:
                st.info(f"📊 {len(selected_standards)} standards")
            with preview_col3:
                if st.button("🔄 Clear All", help="Clear all preview caches"):
                    st.session_state.preview_cache = {}
                    st.rerun()
        else:
            preview_standard = selected_standards[0]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create unique key for current configuration
            cache_key = f"{preview_standard[0]}_{num_problems}_{use_riddles}"
            
            # Check if we have a cached preview for this configuration
            show_preview = False
            if cache_key in st.session_state.preview_cache:
                problems, riddle = st.session_state.preview_cache[cache_key]
                show_preview = True
            
            if st.button("🔄 Generate Preview", type="primary", use_container_width=True):
                st.session_state.generated_files = []
                
                # Generate preview for selected standard
                code, desc = preview_standard
                try:
                    problems, riddle = st.session_state.generator.generate_preview(
                        code, 
                        num_problems,
                        use_riddles and code in RIDDLE_COMPATIBLE_STANDARDS
                    )
                    
                    if problems:
                        # Cache the preview
                        st.session_state.preview_cache[cache_key] = (problems, riddle)
                        show_preview = True
                        st.success(f"✅ Preview generated for {code}: {desc[:40]}...")
                        
                except ValueError as e:
                    st.error(f"⚠️ {str(e)}")
                    st.info("Try reducing the number of problems per worksheet or disabling riddles for this standard.")
                    show_preview = False
            
            # Display preview if available (either from cache or just generated)
            if show_preview and cache_key in st.session_state.preview_cache:
                problems, riddle = st.session_state.preview_cache[cache_key]
                code, desc = preview_standard
                
                # Show which standard is being previewed
                if len(selected_standards) > 1:
                    st.info(f"📋 Previewing: **{code}** - {desc[:60]}...")
                
                # Display problems in columns
                st.subheader("Sample Problems")
                prob_col1, prob_col2 = st.columns(2)
                
                for i, (problem, answer) in enumerate(problems):
                    col = prob_col1 if i % 2 == 0 else prob_col2
                    with col:
                        with st.container():
                            st.markdown(f"**{i+1}.** {problem}")
                            st.caption(f"Answer: {answer}")
                
                # Display riddle if present
                if riddle:
                    st.subheader("🎯 Riddle Component")
                    st.info(f"**Riddle:** {riddle[0]}\n\n**Answer:** {riddle[1]} ({len(riddle[2])} letters)")
                    st.caption("Students solve problems and match answers to decoder letters to reveal the answer!")
            elif len(selected_standards) > 1:
                # Show message when switching to a standard that hasn't been previewed yet
                st.info("👆 Click 'Generate Preview' to see a sample worksheet for this standard")
        
        with col2:
            if st.button("📄 Generate All Worksheets", type="secondary", use_container_width=True):
                with st.spinner("Generating worksheets..."):
                    st.session_state.generated_files = []
                    progress_bar = st.progress(0)
                    total_worksheets = len(selected_standards) * versions
                    current = 0
                    failed_standards = []
                    
                    for code, desc in selected_standards:
                        for v in range(1, versions + 1):
                            try:
                                problems, riddle = st.session_state.generator.generate_preview(
                                    code,
                                    num_problems,
                                    use_riddles and code in RIDDLE_COMPATIBLE_STANDARDS
                                )
                                
                                if problems:
                                    worksheet_pdf, answer_pdf = st.session_state.generator.generate_worksheet_from_preview(
                                        grade,
                                        worksheet_num=v
                                    )
                                    
                                    if worksheet_pdf and answer_pdf:
                                        st.session_state.generated_files.append({
                                            'standard': code,
                                            'version': v,
                                            'worksheet': worksheet_pdf,
                                            'answer': answer_pdf,
                                            'desc': desc
                                        })
                            except ValueError as e:
                                if code not in failed_standards:
                                    failed_standards.append((code, desc, str(e)))
                            
                            current += 1
                            progress_bar.progress(current / total_worksheets)
                    
                    if st.session_state.generated_files:
                        st.success(f"✅ Generated {len(st.session_state.generated_files)} worksheets!")
                    
                    if failed_standards:
                        st.warning("⚠️ Some standards could not generate worksheets:")
                        for code, desc, error in failed_standards:
                            st.write(f"• {code}: {desc[:40]}... - {error}")
                        st.info("Try reducing problems per worksheet or disabling riddles for these standards.")
        
        # Download section
        if st.session_state.generated_files:
            st.divider()
            st.header("📥 Download Files")
            
            # Show what was generated
            with st.expander("📋 Generated Worksheets Summary", expanded=True):
                st.write(f"**Total Worksheets:** {len(st.session_state.generated_files)}")
                st.write(f"**Grade Level:** {grade}")
                st.write(f"**Problems per Worksheet:** {num_problems}")
                
                # Group by standard
                standards_summary = {}
                for file_data in st.session_state.generated_files:
                    std_code = file_data['standard']
                    if std_code not in standards_summary:
                        standards_summary[std_code] = {
                            'desc': file_data['desc'],
                            'count': 0
                        }
                    standards_summary[std_code]['count'] += 1
                
                st.write("**Standards Included:**")
                for std_code, info in standards_summary.items():
                    st.write(f"  • {std_code}: {info['desc'][:50]}... ({info['count']} version{'s' if info['count'] > 1 else ''})")
                
                st.write(f"**Download Format:** {download_option}")
            
            # Create ZIP file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_data in st.session_state.generated_files:
                    standard = file_data['standard']
                    version = file_data['version']
                    
                    if download_option in ["Worksheet + Answer Key", "Worksheet Only"]:
                        zip_file.writestr(
                            f"{standard}_v{version}_worksheet.pdf",
                            file_data['worksheet']
                        )
                    
                    if download_option in ["Worksheet + Answer Key", "Answer Key Only"]:
                        zip_file.writestr(
                            f"{standard}_v{version}_answer_key.pdf",
                            file_data['answer']
                        )
            
            zip_buffer.seek(0)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📦 Download All Files (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"math_worksheets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    type="primary",
                    use_container_width=True
                )
    else:
        st.info("👈 Please select at least one standard from the sidebar to begin")

if __name__ == "__main__":
    main()