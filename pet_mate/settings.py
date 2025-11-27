import argparse

VERBOSE = False
LOG_LEVEL = "ERROR"
MODEL = "gemini-2.5-flash-lite"

def parse_args():
    global VERBOSE, LOG_LEVEL
    parser = argparse.ArgumentParser(description="Pet Mate")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR", help="Log level")
    parser.add_argument("--model", choices=[
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash"
    ], default="gemini-2.5-flash-lite", help="Model to use")
    args = parser.parse_args()
    VERBOSE = args.verbose
    LOG_LEVEL = args.log_level
    MODEL = args.model
    return args

def is_verbose():
    return VERBOSE

def log_level():
    return LOG_LEVEL

def current_model() -> str:
    return MODEL