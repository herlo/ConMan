from platform import architecture

if architecture()[0] != '32bit':
    raise Exception("Don't use this on non-32-bit platforms")

# let ImportError propagate at module load time so that people can notice and fix it
try:
    import psyco
except (ImportError, ie):
    print ie
class PsycoMiddleware(object):
    """
    This middleware enables the psyco extension module which can massively
    speed up the execution of any Python code.
    """
    def process_request(self, request):
        psyco.profile()
        return None
