from enum import Enum

class Specs(Enum):
    INSERTION_SYM  = "$"
    OUTPUT_DIR = "./"
    #Generate a directory by taffy [datetime] for each chew. If false use user-provided output dir, or throw error
    TAFFY_GEN_OUTPUT_DIR = True
    USE_SFO = False
    CREATE_DIR = False
    CONTINUE_ON_ERROR = False
