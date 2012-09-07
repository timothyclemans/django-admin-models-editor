from django.http import HttpResponse
def findall(L, value, start=0):
    return [i for i, x in enumerate(L) if x == value][start:]
        
def get_field_id(key):
    indexes_of_seperator = findall(key, '_')
    print list(findall(key, '_'))
    start = indexes_of_seperator[0] + 1
    stop = indexes_of_seperator[1]
    return key[start: stop]
    
def get_number_of_fields(post_dict):
    return len(set([get_field_id(i) for i in post_dict.keys() if i.startswith('field_')]))

def get_field_ids(post_dict):    
    return sorted(set([get_field_id(i) for i in post_dict.keys() if i.startswith('field_')]))
field_class_names = {'char': 'CharField', 'foreignkey': 'ForeignKey'} 
    


    
def get_field_dict(field_id, post_dict):
    startswith = 'field_%s_' % (field_id)
    items = [(i[0][len(startswith):], i[1]) for i in post_dict.items() if i[0].startswith(startswith)]
    return dict(items)
    
def create_model(request):
    #response = 'hello' + 'number of fields: %s' % (get_number_of_fields(request.POST))
    #response += str([list(findall(i, '_')) for i in request.POST.keys() if '_' in i])
    #response += str([(get_field_id(i[0]), i[1]) for i in request.POST.keys() if i.startswith('field_')])
    code = "class %s(models.Model):\n" % (request.POST['name']) 
    for field_id in get_field_ids(request.POST):
        field = get_field_dict(field_id, request.POST)
        
        arguments = []
        if field['type'] == 'char':
            if 'max_length' in field:
                arguments.append("max_length=%s" % (field['max_length']))
        if field['type'] == 'foreignkey':
            arguments.append("'%s'" % (field['related_model']))
        if 'unique' in field:
            arguments.append("unique=True")
        code += "    %s = models.%s(%s)\n" % (field['name'], field_class_names[field['type']], ', '.join(arguments))
    #response += str(request.POST.items())
    return HttpResponse(code, content_type='text')