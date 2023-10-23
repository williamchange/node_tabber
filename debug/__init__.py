import cProfile
import shutil
from pstats import Stats, SortKey
from pathlib import Path

DEBUG_FOLDER = Path(__file__).parent
PROFILE_FOLDER = DEBUG_FOLDER / "profiles"


if not PROFILE_FOLDER.exists():
    PROFILE_FOLDER.mkdir()

def dump_stats(name, profile):
    stats = Stats(profile)
    stats.sort_stats(SortKey.TIME)
    stats.dump_stats(PROFILE_FOLDER / f"{name}.prof")

def delete_profiles():
    if PROFILE_FOLDER.exists():
        shutil.rmtree(PROFILE_FOLDER)
    
    PROFILE_FOLDER.mkdir()
    

def profile_code(func_type='FUNCTION'):
    if func_type == 'EXECUTE':
        return profile_execute
    elif func_type == 'INVOKE':
        return profile_invoke
    else:
        return profile_function


def profile_function(func):
    def wrapped_func(*args, **kwargs):
        with cProfile.Profile() as pr:
            output = func(*args, **kwargs)
        
        dump_stats(name=func.__name__, profile=pr)
        return output

    return wrapped_func


def profile_execute(func):
    def wrapped_func(self, context):
        with cProfile.Profile() as pr:
            output = func(self, context)
        
        dump_stats(name=func.__name__, profile=pr)
        return output

    return wrapped_func


def profile_invoke(func):
    def wrapped_func(self, context, event):
        with cProfile.Profile() as pr:
            output = func(self, context, event)

        dump_stats(name=func.__name__, profile=pr)
        return output

    return wrapped_func


if __name__ == "__main__":
    delete_profiles()