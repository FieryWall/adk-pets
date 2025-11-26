import inspect
from google.adk.tools.google_search_tool import google_search
print('type:', type(google_search))
print('\nNon-private attributes:')
for name in dir(google_search):
    if name.startswith('_'):
        continue
    attr = getattr(google_search, name)
    print(name, '->', type(attr))
    try:
        if inspect.iscoroutinefunction(attr) or inspect.isfunction(attr):
            print('  (callable) signature:', inspect.signature(attr))
    except Exception:
        pass
