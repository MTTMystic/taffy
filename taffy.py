import sys 
import os
from datetime import datetime
from enum import Enum
from Error import Error

insertion_symbol = "$"
num_insertions_per_template_phrase = 1
use_single_output_file_flag = "sof"
default_output_dir = "./"
default_use_single_output_file = False

# to be valid, the user must provide both a template file (first arg)
# and insertion file (second arg)
# and both files must be .txt files
def validate_args(args):
    output_dir = default_output_dir
    use_single_output_file = default_use_single_output_file
    #at minimum user must supply two filepaths to two .txt files
    #by default less than 2 args is invalid input
    if len(args) < 2:
        print(Error.INVALID_ARGS.value.replace("$use_single_output_file_flag", use_single_output_file_flag))
    elif len(args) >= 2:
        #check the first two args are valid .txt filepaths
        for idx, fp in enumerate(args[0:2]):
            if not os.path.exists(fp):
                print(Error.FILE_NON_EXIST.value.replace("$fp", fp))
            elif os.path.splitext(fp)[1] !=  ".txt":
                print(Error.INVALID_EXT.value)
        #check that the output dir exists, if os dir provided
        #TODO user may specify if program should create output dir if it doesn't exist, otherwise program will not create it and will throw error
        if len(args) > 2:
            specified_output_dir = args[2]
            if not os.path.exists(os.path.abspath(specified_output_dir)):
                print(ERROR.FILE_NON_EXIST.value.replace("$fp", specified_output_dir))
            print(specified_output_dir)
            output_dir = specified_output_dir
        #mark single output file flag if user specified (optional)
        if len(args) > 3 and args[3] == use_single_output_file_flag:
            use_single_output_file = True
    return (output_dir, use_single_output_file)
def load_template_phrases(fp):
    try:
        tphrases_file = open(fp, "r")
        try:
            tphrases = []
            template_valid = False
            for idx, line in enumerate(tphrases_file):
                actual_line = line.strip()
                if (actual_line):
                    #line must contain an insertion symbol
                    no_insertion_symbol = actual_line.count(insertion_symbol) == 0 
                    #line must not contain too many insertion symbols
                    too_many_insertions = actual_line.count(insertion_symbol) > num_insertions_per_template_phrase
                    error_msg = None
                    if (no_insertion_symbol):
                        error_msg = Error.INVALID_TEMPLATE_MISSING_INSERTION_SYMBOL.value
                    if (too_many_insertions):
                        error_msg = Error.INVALID_TEMPLATE_EXCESS_INSERTION_SYMBOLS.value.replace("$num_insertions", str(num_insertions_per_template_phrase))
                    if (error_msg):
                        error_msg = error_msg.replace("$fp", fp).replace("$ln", str(idx+1)).replace("$tp", '"' + actual_line + '"')
                        print(error_msg)
                    else:
                        tphrases.append(actual_line)
                #template valid if no other issues were found
            template_valid = True
            if len(tphrases) == 0 and not template_valid:
                print(Error.FILE_EMPTY.value.replace("$fp", fp))
            return tphrases
        except:
            print(Error.FILE_READ.value.replace("$fp", fp))
        tphrases_file.close()
    except:
        print(Error.FILE_OPEN.value.replace("$fp", fp))
    

def load_insertion_phrases(fp):
    try:
        insertion_file = open(fp, 'r')
        try:
            iphrases = []
            for idx, line in enumerate(insertion_file):
                actual_line = line.strip()
                if (actual_line):
                    iphrases.append(actual_line)
            if (len(iphrases) == 0) :
                print(Error.FILE_EMPTY.value.replace("$fp", fp))
            return iphrases
        except:
            print(Error.FILE_READ.value.replace("$fp", fp))
        insertion_file.close()
    except:
        print(Error.FILE_OPEN.value.replace("$fp", fp))


def gen_output_folder_name():
    formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M')
    output_dir_name = "taffy " + formatted_datetime
    return output_dir_name

def gen_output_filenames(template_phrases):
    output_fps = []
    for phrase in template_phrases:
        output_fps.append(phrase + ".txt")
    return output_fps

def write_completed_phrases_to_file(phrases, fp):
    try:
        file = open(fp, 'a')

        for phrase in phrases:
            try:
                file.write(phrase)
                file.write('\n')
            except:
                print(Error.FILE_WRITE.value.replace("$l", phrase).replace("$fp", fp))
        file.close()
    except:
        print(Error.FILE_OPEN.value.replace("$fp", fp))

def make_output_file(completed_phrases, output_dir):
    final_fp = gen_output_folder_name() + ".txt"
    final_dir = os.path.join(output_dir, final_fp)
    file = open(final_dir, 'a')
    file.close()
    
    template_phrases = list(completed_phrases.keys())
    for template_phrase in template_phrases:
        write_completed_phrases_to_file(completed_phrases[template_phrase], final_dir)


def make_output_files(completed_phrases, output_dir):
    final_output_dir = os.path.join(os.path.abspath(output_dir), gen_output_folder_name())
    os.mkdir(final_output_dir)
    template_phrases = list(completed_phrases.keys())
    fps = gen_output_filenames(template_phrases)
    for i in range(len(fps)):
        fp = fps[i]
        template_phrase = template_phrases[i]
        output_fp = os.path.join(final_output_dir, fp)
        try:
            file = open(output_fp, 'a')
            file.close()
        except:
            print(Error.FILE_OPEN.value.replace("$fp", output_fp))
        write_completed_phrases_to_file(completed_phrases[template_phrase], output_fp)
        
def make_insertions(tphrases, iphrases):
    completed_phrases = {}
    for tphrase in tphrases:
        completed_phrases[tphrase] = []
        for iphrase in iphrases:
            completed_phrase = tphrase.replace("$", iphrase)
            completed_phrases[tphrase].append(completed_phrase)
    return completed_phrases
            
    
def taffy(template_fp, insertion_fp, taffy_output_dir , use_single_output_file):
    tphrases = load_template_phrases(template_fp)
    iphrases = load_insertion_phrases(insertion_fp)

    #TODO make it easier for users to use output of one taffy operation as the input for another
    gen_phrases = make_insertions(tphrases, iphrases)
    
    if (use_single_output_file):
        make_output_file(gen_phrases, taffy_output_dir)
    else:
        make_output_files(gen_phrases, taffy_output_dir)


def main(args):
    #args without program name
    truncated_args = args[1:]
    output_dir, sof = validate_args(truncated_args)
    taffy(truncated_args[0], truncated_args[1], output_dir, sof)

if __name__ == "__main__":
    main(sys.argv)

