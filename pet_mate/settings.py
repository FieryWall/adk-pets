import argparse

DEBUG = False
VERBOSE = False
LOG_LEVEL = "ERROR"
MODEL = "gemini-2.5-flash-lite"

def parse_args():
    global DEBUG, VERBOSE, LOG_LEVEL, MODEL
    parser = argparse.ArgumentParser(description="Pet Mate")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-l", "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR", help="Log level")
    parser.add_argument("-m", "--model", choices=[
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash"
    ], default="gemini-2.5-flash-lite", help="Model to use")
    args = parser.parse_args()
    DEBUG = args.debug
    VERBOSE = args.verbose
    LOG_LEVEL = args.log_level
    MODEL = args.model
    if VERBOSE:
        print(f"Current model: {MODEL}")
    return args

def is_debug():
    return DEBUG

def is_verbose():
    return VERBOSE

def log_level():
    return LOG_LEVEL

def current_model() -> str:
    return MODEL