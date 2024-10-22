from enum import Enum

class Error(Enum):
    INVALID_ARGS = "The provided arguments are invalid. The correct format is taffy.py template_txtfile_path phrases_to_insert_txtfile_path desired_output_directory_path (optional) single_output_file (optional, off by default, use $single_output_file_flag to enable)"
    FP_NOT_PROVIDED = "Please provide filepaths of the txt file containing template phrases, the txt file containing phrases to insert, and the desired output directory.  "
    FILE_NON_EXIST = "The file $fp does not exist"
    INVALID_EXT = "Both input files must be in .txt format"
    FILE_OPEN = "An error occurred while trying to open the file $fp"
    FILE_READ = "An error occurred while trying to read the file $fp"
    FILE_WRITE = "An error occurred while trying to write $l to the file $fp"
    FILE_EMPTY = "Error: Input file $fp is empty"
    INVALID_TEMPLATE_MISSING_INSERTION_SYMBOL = "Error in template file $fp on line $ln, template phrase $tp is missing the insertion symbol, which is $"
    INVALID_TEMPLATE_EXCESS_INSERTION_SYMBOLS = "Error in template file $fp on line $ln, template phrase $tp has too many insertion symbols. Only $num_insertions insertions are allowed per template phrase."
