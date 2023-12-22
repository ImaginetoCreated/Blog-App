def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        return l

    return _length

field = "afew3243faw3FSjj"


l = field and len(field) or 0

print(l)

print(234 and 2344 or 0)
