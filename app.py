from flask import Flask, render_template, request, jsonify, make_response, session, url_for, redirect, flash, Markup
from urllib.request import urlopen
import simplejson
import re

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
    ('q0', 'd'): 'q21',
    ('q0',' '):'q0',
    ('q0', 'm'): 'q4',
    ('q0', 'g'): 'q8',
    ('q0', 'b'): 'q12',
    ('q0', 'p'): 'q15',
    ('q1', 'n'): 'q2',
    ('q1',' '):'q0',
    ('q2', 'd'): 'q3',
    ('q2',' '):'q0',
    ('q3', 'd'): 'q3',
    ('q3',' '):'q0',
    ('q4',' '):'q0',
    ('q4', 'o'): 'q5',
    ('q5',' '):'q0',
    ('q5', 's'): 'q6',
    ('q6',' '):'q0',
    ('q6', 's'): 'q6',
    ('q6', 't'): 'q7',
    ('q7',' '):'q0',
    ('q7', 't'): 'q7',
    ('q8',' '):'q0',
    ('q8', 'o'): 'q9',
    ('q9',' '):'q0',
    ('q9', 'o'): 'q10',
    ('q10', 'd'): 'q11',
    ('q10',' '):'q0',
    ('q11',' '):'q0',
    ('q12', 'a'): 'q13',
    ('q12',' '):'q0',
    ('q12', 'l'): 'q26',
    ('q13', 'd'): 'q14',
    ('q13',' '):'q0',
    ('q14',' '):'q0',
    ('q15',' '):'q0',
    ('q15', 'r'): 'q16',
    ('q16',' '):'q0',
    ('q16', 'e'): 'q17',
    ('q17',' '):'q0',
    ('q17', 't'): 'q18',
    ('q18',' '):'q0',
    ('q18', 't'): 'q19',
    ('q19',' '):'q0',
    ('q19', 'y'): 'q20',
    ('q20',' '):'q0',
    ('q21',' '):'q0',
    ('q21', 'i'): 'q22',
    ('q22',' '):'q0',
    ('q22', 'r'): 'q23',
    ('q23',' '):'q0',
    ('q23', 't'): 'q24',
    ('q24',' '):'q0',
    ('q24', 'y'): 'q25',
    ('q25',' '):'q0',
    ('q26',' '):'q0',
    ('q26', 'u'): 'q27',
    ('q27',' '):'q0',
    ('q27', 'e'): 'q28',
    ('q28',' '):'q0',
    }


    if request.args.get('generateDFA'):
        text=request.args.get('text')
        sentences_string = re.split(r'[.\n]+', text)
        clean_sentences = [sentence for sentence in sentences_string if sentence.strip()]
        total_occurrence_count = {pattern[i]: 0 for i in range(len(pattern))}  # Initialize the total occurrence count dynamically
        sentences_data = []

        for sentence in clean_sentences:
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
                elif (current_state, char) not in transition:
                    continue
                    
            substrings_found = find_substring(char_substring, pattern)
            
            if substrings_found:
                status='Accepted'
                occurrence_count=calc_occurrence_count(substrings_found,sentence)
                positions=find_position_index(sentence,pattern)
                for input_pattern, count in occurrence_count.items():
                    total_occurrence_count[input_pattern] += count
            else:
                status='Rejected'
                occurrence_count={}
                positions={}

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

        return render_template('index.html',pattern=pattern,states=states,alphabets=alphabets,start_state=start_state,accept_states=accept_states,sentences_string=clean_sentences,sentences_data=sentences_data,total_occurrence_count=total_occurrence_count,transition=transition)

    return render_template('index.html',pattern=pattern,states=states,alphabets=alphabets,start_state=start_state,accept_states=accept_states)


if __name__ == "__main__":
    app.run(debug=True)
