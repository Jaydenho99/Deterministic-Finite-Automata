from flask import Flask, render_template, request, jsonify, make_response, session, url_for, redirect, flash, Markup
from urllib.request import urlopen
import simplejson

app = Flask(__name__)
app.secret_key = "super secret key"

def find_substring(char_substring,pattern):

    substrings = set()
    current_substring = ""

    for c in char_substring:
        if c != ' ':
            current_substring += c
        else:
            if current_substring != "":
                if current_substring in pattern:
                    substrings.add(current_substring)
                current_substring = ""

    # Check the last substring if it exists
    if current_substring != "" and current_substring in pattern:
        substrings.add(current_substring)

    return substrings

def calc_occurrence_count(substrings_found,sentence):
    occurrence_count = {}
    # Calculate and display occurrence count
    for substring in substrings_found:
        count=sentence.count(substring)
        if substring in occurrence_count:
            occurrence_count[substring]+=count
        else:
            occurrence_count[substring]=count
    return occurrence_count

def find_position_index(sentence,pattern):
    positions = {}
    for input_pattern in pattern:
        pos_list = [pos for pos in range(len(sentence)) if sentence.startswith(input_pattern, pos)]
        if pos_list:
            positions[input_pattern] = pos_list
    return positions

@app.route('/',methods=['POST', 'GET'])
def home():
    pattern=["and","most","good","bad","pretty","dirty","blue"]
    states = ["q0","q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12","q13","q14","q15","q16","q17","q18","q19","q20","q21","q22","q23","q24","q25","q26","q27","q28"]
    alphabets = ["a","n","d","m","o","s","t","g","b","p","r","e","y","i","l","u"]
    start_state = "q0"
    accept_states = ["q3","q7","q11","q14","q20","q25","q28"]

    transition = {
    ('q0', 'a'): 'q1',
    ('q0', 'n'): 'q0',
    ('q0', 'd'): 'q21',
    ('q0',' '):'q0',
    ('q0', 'm'): 'q4',
    ('q0', 'o'): 'q0',
    ('q0', 's'): 'q0',
    ('q0', 't'): 'q0',
    ('q0', 'g'): 'q8',
    ('q0', 'b'): 'q12',
    ('q0', 'p'): 'q15',
    ('q0', 'r'): 'q0',
    ('q0', 'e'): 'q0',
    ('q0', 'y'): 'q0',
    ('q0', 'i'): 'q0',
    ('q0', 'l'): 'q0',
    ('q0', 'u'): 'q0',
    
    ('q1', 'a'): 'q0',
    ('q1', 'n'): 'q2',
    ('q1', 'd'): 'q0',
    ('q1',' '):'q0',
    ('q1', 'm'): 'q0',
    ('q1', 'o'): 'q0',
    ('q1', 's'): 'q0',
    ('q1', 't'): 'q0',
    ('q1', 'g'): 'q0',
    ('q1', 'b'): 'q0',
    ('q1', 'p'): 'q0',
    ('q1', 'r'): 'q0',
    ('q1', 'e'): 'q0',
    ('q1', 'y'): 'q0',
    ('q1', 'i'): 'q0',
    ('q1', 'l'): 'q0',
    ('q1', 'u'): 'q0',
    
    ('q2', 'a'): 'q0',
    ('q2', 'n'): 'q0',
    ('q2', 'd'): 'q3',
    ('q2',' '):'q0',
    ('q2', 'm'): 'q0',
    ('q2', 'o'): 'q0',
    ('q2', 's'): 'q0',
    ('q2', 't'): 'q0',
    ('q2', 'g'): 'q0',
    ('q2', 'b'): 'q0',
    ('q2', 'p'): 'q0',
    ('q2', 'r'): 'q0',
    ('q2', 'e'): 'q0',
    ('q2', 'y'): 'q0',
    ('q2', 'i'): 'q0',
    ('q2', 'l'): 'q0',
    ('q2', 'u'): 'q0',
        
    ('q3', 'a'): 'q0',
    ('q3', 'n'): 'q0',
    ('q3', 'd'): 'q3',
    ('q3',' '):'q0',
    ('q3', 'm'): 'q0',
    ('q3', 'o'): 'q0',
    ('q3', 's'): 'q0',
    ('q3', 't'): 'q0',
    ('q3', 'g'): 'q0',
    ('q3', 'b'): 'q0',
    ('q3', 'p'): 'q0',
    ('q3', 'r'): 'q0',
    ('q3', 'e'): 'q0',
    ('q3', 'y'): 'q0',
    ('q3', 'i'): 'q0',
    ('q3', 'l'): 'q0',
    ('q3', 'u'): 'q0',
    
    ('q4', 'a'): 'q0',
    ('q4', 'n'): 'q0',
    ('q4', 'd'): 'q0',
    ('q4',' '):'q0',
    ('q4', 'm'): 'q0',
    ('q4', 'o'): 'q5',
    ('q4', 's'): 'q0',
    ('q4', 't'): 'q0',
    ('q4', 'g'): 'q0',
    ('q4', 'b'): 'q0',
    ('q4', 'p'): 'q0',
    ('q4', 'r'): 'q0',
    ('q4', 'e'): 'q0',
    ('q4', 'y'): 'q0',
    ('q4', 'i'): 'q0',
    ('q4', 'l'): 'q0',
    ('q4', 'u'): 'q0',
    
    ('q5', 'a'): 'q0',
    ('q5', 'n'): 'q0',
    ('q5', 'd'): 'q0',
    ('q5',' '):'q0',
    ('q5', 'm'): 'q0',
    ('q5', 'o'): 'q0',
    ('q5', 's'): 'q6',
    ('q5', 't'): 'q0',
    ('q5', 'g'): 'q0',
    ('q5', 'b'): 'q0',
    ('q5', 'p'): 'q0',
    ('q5', 'r'): 'q0',
    ('q5', 'e'): 'q0',
    ('q5', 'y'): 'q0',
    ('q5', 'i'): 'q0',
    ('q5', 'l'): 'q0',
    ('q5', 'u'): 'q0',
    
    ('q6', 'a'): 'q0',
    ('q6', 'n'): 'q0',
    ('q6', 'd'): 'q0',
    ('q6',' '):'q0',
    ('q6', 'm'): 'q0',
    ('q6', 'o'): 'q0',
    ('q6', 's'): 'q6',
    ('q6', 't'): 'q7',
    ('q6', 'g'): 'q0',
    ('q6', 'b'): 'q0',
    ('q6', 'p'): 'q0',
    ('q6', 'r'): 'q0',
    ('q6', 'e'): 'q0',
    ('q6', 'y'): 'q0',
    ('q6', 'i'): 'q0',
    ('q6', 'l'): 'q0',
    ('q6', 'u'): 'q0',

    ('q7', 'a'): 'q0',
    ('q7', 'n'): 'q0',
    ('q7', 'd'): 'q0',
    ('q7',' '):'q0',
    ('q7', 'm'): 'q0',
    ('q7', 'o'): 'q0',
    ('q7', 's'): 'q0',
    ('q7', 't'): 'q7',
    ('q7', 'g'): 'q0',
    ('q7', 'b'): 'q0',
    ('q7', 'p'): 'q0',
    ('q7', 'r'): 'q0',
    ('q7', 'e'): 'q0',
    ('q7', 'y'): 'q0',
    ('q7', 'i'): 'q0',
    ('q7', 'l'): 'q0',
    ('q7', 'u'): 'q0',
        
    ('q8', 'a'): 'q0',
    ('q8', 'n'): 'q0',
    ('q8', 'd'): 'q0',
    ('q8',' '):'q0',
    ('q8', 'm'): 'q0',
    ('q8', 'o'): 'q9',
    ('q8', 's'): 'q0',
    ('q8', 't'): 'q0',
    ('q8', 'g'): 'q0',
    ('q8', 'b'): 'q0',
    ('q8', 'p'): 'q0',
    ('q8', 'r'): 'q0',
    ('q8', 'e'): 'q0',
    ('q8', 'y'): 'q0',
    ('q8', 'i'): 'q0',
    ('q8', 'l'): 'q0',
    ('q8', 'u'): 'q0',
        
    ('q9', 'a'): 'q0',
    ('q9', 'n'): 'q0',
    ('q9', 'd'): 'q0',
    ('q9',' '):'q0',
    ('q9', 'm'): 'q0',
    ('q9', 'o'): 'q10',
    ('q9', 's'): 'q0',
    ('q9', 't'): 'q0',
    ('q9', 'g'): 'q0',
    ('q9', 'b'): 'q0',
    ('q9', 'p'): 'q0',
    ('q9', 'r'): 'q0',
    ('q9', 'e'): 'q0',
    ('q9', 'y'): 'q0',
    ('q9', 'i'): 'q0',
    ('q9', 'l'): 'q0',
    ('q9', 'u'): 'q0',
    
    ('q10', 'a'): 'q0',
    ('q10', 'n'): 'q0',
    ('q10', 'd'): 'q11',
    ('q10',' '):'q0',
    ('q10', 'm'): 'q0',
    ('q10', 'o'): 'q0',
    ('q10', 's'): 'q0',
    ('q10', 't'): 'q0',
    ('q10', 'g'): 'q0',
    ('q10', 'b'): 'q0',
    ('q10', 'p'): 'q0',
    ('q10', 'r'): 'q0',
    ('q10', 'e'): 'q0',
    ('q10', 'y'): 'q0',
    ('q10', 'i'): 'q0',
    ('q10', 'l'): 'q0',
    ('q10', 'u'): 'q0',

    ('q11', 'a'): 'q0',
    ('q11', 'n'): 'q0',
    ('q11', 'd'): 'q0',
    ('q11',' '):'q0',
    ('q11', 'm'): 'q0',
    ('q11', 'o'): 'q0',
    ('q11', 's'): 'q0',
    ('q11', 't'): 'q0',
    ('q11', 'g'): 'q0',
    ('q11', 'b'): 'q0',
    ('q11', 'p'): 'q0',
    ('q11', 'r'): 'q0',
    ('q11', 'e'): 'q0',
    ('q11', 'y'): 'q0',
    ('q11', 'i'): 'q0',
    ('q11', 'l'): 'q0',
    ('q11', 'u'): 'q0',
    
    ('q12', 'a'): 'q13',
    ('q12', 'n'): 'q0',
    ('q12', 'd'): 'q0',
    ('q12',' '):'q0',
    ('q12', 'm'): 'q0',
    ('q12', 'o'): 'q0',
    ('q12', 's'): 'q0',
    ('q12', 't'): 'q0',
    ('q12', 'g'): 'q0',
    ('q12', 'b'): 'q0',
    ('q12', 'p'): 'q0',
    ('q12', 'r'): 'q0',
    ('q12', 'e'): 'q0',
    ('q12', 'y'): 'q0',
    ('q12', 'i'): 'q0',
    ('q12', 'l'): 'q26',
    ('q12', 'u'): 'q0',
    
    ('q13', 'a'): 'q0',
    ('q13', 'n'): 'q0',
    ('q13', 'd'): 'q14',
    ('q13',' '):'q0',
    ('q13', 'm'): 'q0',
    ('q13', 'o'): 'q0',
    ('q13', 's'): 'q0',
    ('q13', 't'): 'q0',
    ('q13', 'g'): 'q0',
    ('q13', 'b'): 'q0',
    ('q13', 'p'): 'q0',
    ('q13', 'r'): 'q0',
    ('q13', 'e'): 'q0',
    ('q13', 'y'): 'q0',
    ('q13', 'i'): 'q0',
    ('q13', 'l'): 'q0',
    ('q13', 'u'): 'q0',
        
    ('q14', 'a'): 'q0',
    ('q14', 'n'): 'q0',
    ('q14', 'd'): 'q0',
    ('q14',' '):'q0',
    ('q14', 'm'): 'q0',
    ('q14', 'o'): 'q0',
    ('q14', 's'): 'q0',
    ('q14', 't'): 'q0',
    ('q14', 'g'): 'q0',
    ('q14', 'b'): 'q0',
    ('q14', 'p'): 'q0',
    ('q14', 'r'): 'q0',
    ('q14', 'e'): 'q0',
    ('q14', 'y'): 'q0',
    ('q14', 'i'): 'q0',
    ('q14', 'l'): 'q0',
    ('q14', 'u'): 'q0',
        
    ('q15', 'a'): 'q0',
    ('q15', 'n'): 'q0',
    ('q15', 'd'): 'q0',
    ('q15',' '):'q0',
    ('q15', 'm'): 'q0',
    ('q15', 'o'): 'q0',
    ('q15', 's'): 'q0',
    ('q15', 't'): 'q0',
    ('q15', 'g'): 'q0',
    ('q15', 'b'): 'q0',
    ('q15', 'p'): 'q0',
    ('q15', 'r'): 'q16',
    ('q15', 'e'): 'q0',
    ('q15', 'y'): 'q0',
    ('q15', 'i'): 'q0',
    ('q15', 'l'): 'q0',
    ('q15', 'u'): 'q0',
        
    ('q16', 'a'): 'q0',
    ('q16', 'n'): 'q0',
    ('q16', 'd'): 'q0',
    ('q16',' '):'q0',
    ('q16', 'm'): 'q0',
    ('q16', 'o'): 'q0',
    ('q16', 's'): 'q0',
    ('q16', 't'): 'q0',
    ('q16', 'g'): 'q0',
    ('q16', 'b'): 'q0',
    ('q16', 'p'): 'q0',
    ('q16', 'r'): 'q0',
    ('q16', 'e'): 'q17',
    ('q16', 'y'): 'q0',
    ('q16', 'i'): 'q0',
    ('q16', 'l'): 'q0',
    ('q16', 'u'): 'q0',
        
    ('q17', 'a'): 'q0',
    ('q17', 'n'): 'q0',
    ('q17', 'd'): 'q0',
    ('q17',' '):'q0',
    ('q17', 'm'): 'q0',
    ('q17', 'o'): 'q0',
    ('q17', 's'): 'q0',
    ('q17', 't'): 'q18',
    ('q17', 'g'): 'q0',
    ('q17', 'b'): 'q0',
    ('q17', 'p'): 'q0',
    ('q17', 'r'): 'q0',
    ('q17', 'e'): 'q0',
    ('q17', 'y'): 'q0',
    ('q17', 'i'): 'q0',
    ('q17', 'l'): 'q0',
    ('q17', 'u'): 'q0',
        
    ('q18', 'a'): 'q0',
    ('q18', 'n'): 'q0',
    ('q18', 'd'): 'q0',
    ('q18',' '):'q0',
    ('q18', 'm'): 'q0',
    ('q18', 'o'): 'q0',
    ('q18', 's'): 'q0',
    ('q18', 't'): 'q19',
    ('q18', 'g'): 'q0',
    ('q18', 'b'): 'q0',
    ('q18', 'p'): 'q0',
    ('q18', 'r'): 'q0',
    ('q18', 'e'): 'q0',
    ('q18', 'y'): 'q0',
    ('q18', 'i'): 'q0',
    ('q18', 'l'): 'q0',
    ('q18', 'u'): 'q0',
        
    ('q19', 'a'): 'q0',
    ('q19', 'n'): 'q0',
    ('q19', 'd'): 'q0',
    ('q19',' '):'q0',
    ('q19', 'm'): 'q0',
    ('q19', 'o'): 'q0',
    ('q19', 's'): 'q0',
    ('q19', 't'): 'q0',
    ('q19', 'g'): 'q0',
    ('q19', 'b'): 'q0',
    ('q19', 'p'): 'q0',
    ('q19', 'r'): 'q0',
    ('q19', 'e'): 'q0',
    ('q19', 'y'): 'q20',
    ('q19', 'i'): 'q0',
    ('q19', 'l'): 'q0',
    ('q19', 'u'): 'q0',
        
    ('q20', 'a'): 'q0',
    ('q20', 'n'): 'q0',
    ('q20', 'd'): 'q0',
    ('q20',' '):'q0',
    ('q20', 'm'): 'q0',
    ('q20', 'o'): 'q0',
    ('q20', 's'): 'q0',
    ('q20', 't'): 'q0',
    ('q20', 'g'): 'q0',
    ('q20', 'b'): 'q0',
    ('q20', 'p'): 'q0',
    ('q20', 'r'): 'q0',
    ('q20', 'e'): 'q0',
    ('q20', 'y'): 'q0',
    ('q20', 'i'): 'q0',
    ('q20', 'l'): 'q0',
    ('q20', 'u'): 'q0',
    
    ('q21', 'a'): 'q0',
    ('q21', 'n'): 'q0',
    ('q21', 'd'): 'q0',
    ('q21',' '):'q0',
    ('q21', 'm'): 'q0',
    ('q21', 'o'): 'q0',
    ('q21', 's'): 'q0',
    ('q21', 't'): 'q0',
    ('q21', 'g'): 'q0',
    ('q21', 'b'): 'q0',
    ('q21', 'p'): 'q0',
    ('q21', 'r'): 'q0',
    ('q21', 'e'): 'q0',
    ('q21', 'y'): 'q0',
    ('q21', 'i'): 'q22',
    ('q21', 'l'): 'q0',
    ('q21', 'u'): 'q0',
        
    ('q22', 'a'): 'q0',
    ('q22', 'n'): 'q0',
    ('q22', 'd'): 'q0',
    ('q22',' '):'q0',
    ('q22', 'm'): 'q0',
    ('q22', 'o'): 'q0',
    ('q22', 's'): 'q0',
    ('q22', 't'): 'q0',
    ('q22', 'g'): 'q0',
    ('q22', 'b'): 'q0',
    ('q22', 'p'): 'q0',
    ('q22', 'r'): 'q23',
    ('q22', 'e'): 'q0',
    ('q22', 'y'): 'q0',
    ('q22', 'i'): 'q0',
    ('q22', 'l'): 'q0',
    ('q22', 'u'): 'q0',
        
    ('q23', 'a'): 'q0',
    ('q23', 'n'): 'q0',
    ('q23', 'd'): 'q0',
    ('q23',' '):'q0',
    ('q23', 'm'): 'q0',
    ('q23', 'o'): 'q0',
    ('q23', 's'): 'q0',
    ('q23', 't'): 'q24',
    ('q23', 'g'): 'q0',
    ('q23', 'b'): 'q0',
    ('q23', 'p'): 'q0',
    ('q23', 'r'): 'q0',
    ('q23', 'e'): 'q0',
    ('q23', 'y'): 'q0',
    ('q23', 'i'): 'q0',
    ('q23', 'l'): 'q0',
    ('q23', 'u'): 'q0',
        
    ('q24', 'a'): 'q0',
    ('q24', 'n'): 'q0',
    ('q24', 'd'): 'q0',
    ('q24',' '):'q0',
    ('q24', 'm'): 'q0',
    ('q24', 'o'): 'q0',
    ('q24', 's'): 'q0',
    ('q24', 't'): 'q0',
    ('q24', 'g'): 'q0',
    ('q24', 'b'): 'q0',
    ('q24', 'p'): 'q0',
    ('q24', 'r'): 'q0',
    ('q24', 'e'): 'q0',
    ('q24', 'y'): 'q25',
    ('q24', 'i'): 'q0',
    ('q24', 'l'): 'q0',
    ('q24', 'u'): 'q0',
        
    ('q25', 'a'): 'q0',
    ('q25', 'n'): 'q0',
    ('q25', 'd'): 'q0',
    ('q25',' '):'q0',
    ('q25', 'm'): 'q0',
    ('q25', 'o'): 'q0',
    ('q25', 's'): 'q0',
    ('q25', 't'): 'q0',
    ('q25', 'g'): 'q0',
    ('q25', 'b'): 'q0',
    ('q25', 'p'): 'q0',
    ('q25', 'r'): 'q0',
    ('q25', 'e'): 'q0',
    ('q25', 'y'): 'q0',
    ('q25', 'i'): 'q0',
    ('q25', 'l'): 'q0',
    ('q25', 'u'): 'q0',
    
    ('q26', 'a'): 'q0',
    ('q26', 'n'): 'q0',
    ('q26', 'd'): 'q0',
    ('q26',' '):'q0',
    ('q26', 'm'): 'q0',
    ('q26', 'o'): 'q0',
    ('q26', 's'): 'q0',
    ('q26', 't'): 'q0',
    ('q26', 'g'): 'q0',
    ('q26', 'b'): 'q0',
    ('q26', 'p'): 'q0',
    ('q26', 'r'): 'q0',
    ('q26', 'e'): 'q0',
    ('q26', 'y'): 'q0',
    ('q26', 'i'): 'q0',
    ('q26', 'l'): 'q0',
    ('q26', 'u'): 'q27',
    
    ('q27', 'a'): 'q0',
    ('q27', 'n'): 'q0',
    ('q27', 'd'): 'q0',
    ('q27',' '):'q0',
    ('q27', 'm'): 'q0',
    ('q27', 'o'): 'q0',
    ('q27', 's'): 'q0',
    ('q27', 't'): 'q0',
    ('q27', 'g'): 'q0',
    ('q27', 'b'): 'q0',
    ('q27', 'p'): 'q0',
    ('q27', 'r'): 'q0',
    ('q27', 'e'): 'q28',
    ('q27', 'y'): 'q0',
    ('q27', 'i'): 'q0',
    ('q27', 'l'): 'q0',
    ('q27', 'u'): 'q0',
    
    ('q28', 'a'): 'q0',
    ('q28', 'n'): 'q0',
    ('q28', 'd'): 'q0',
    ('q28',' '):'q0',
    ('q28', 'm'): 'q0',
    ('q28', 'o'): 'q0',
    ('q28', 's'): 'q0',
    ('q28', 't'): 'q0',
    ('q28', 'g'): 'q0',
    ('q28', 'b'): 'q0',
    ('q28', 'p'): 'q0',
    ('q28', 'r'): 'q0',
    ('q28', 'e'): 'q0',
    ('q28', 'y'): 'q0',
    ('q28', 'i'): 'q0',
    ('q28', 'l'): 'q0',
    ('q28', 'u'): 'q0',
    }

    if request.args.get('generateDFA'):
        text=request.args.get('text')
        sentences_string=text.split('.')
        total_occurrence_count = {pattern[i]: 0 for i in range(len(pattern))}  # Initialize the total occurrence count dynamically
        sentences_data = []

        for sentence in sentences_string:
            current_state = start_state  # Reset the current state for the next sentence
            transition_link = []  # List to store the transitions
            char_substring = []
            
            for char in sentence.lower():
                if (current_state, char) in transition:
                    next_state = transition[(current_state, char)]
                    current_state = next_state
                    char_substring.append(char)
                    transition_link.append(f"{current_state}")
                elif char not in alphabets:
                    continue  # Skip characters not present in alphabets
                    
            substrings_found = find_substring(char_substring, pattern)
            
            if substrings_found:
                status='Accepted'
                occurrence_count=calc_occurrence_count(substrings_found,sentence)
                positions=find_position_index(sentence,pattern)
            else:
                status='Rejected'
                occurrence_count={}
                positions=""

            sentence_data = {
                    'sentence': sentence,
                    'char_substring': char_substring,
                    'transition_link': transition_link,
                    'substrings_found': substrings_found,
                    'status':status,
                    'occurrence_count':occurrence_count,
                    'position':positions
                }
            sentences_data.append(sentence_data)

        return render_template('index.html',pattern=pattern,states=states,alphabets=alphabets,start_state=start_state,accept_states=accept_states,sentences_string=sentences_string,sentences_data=sentences_data)

    return render_template('index.html',pattern=pattern,states=states,alphabets=alphabets,start_state=start_state,accept_states=accept_states)


if __name__ == "__main__":
    app.run(debug=True)
