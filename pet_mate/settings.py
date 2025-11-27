import argparse

VERBOSE = False
LOG_LEVEL = "ERROR"

def parse_args():
    global VERBOSE, LOG_LEVEL
    parser = argparse.ArgumentParser(description="Pet Mate")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR", help="Log level")
    args = parser.parse_args()
    VERBOSE = args.verbose
    LOG_LEVEL = args.log_level
    return args

def is_verbose():
    return VERBOSE

def log_level():
    return LOG_LEVEL