from django.http import HttpResponse
import os
import json
import logging

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
field_class_names = {'auto': 'AutoField', 'biginteger': 'BigIntegerField', 'boolean': 'BooleanField', 'char': 'CharField', 'commaseparatedinteger': 'CommaSeparatedIntegerField', 'foreignkey': 'ForeignKey', 'onetoone': 'OneToOneField', 'manytomany': 'ManyToManyField', 'text': 'TextField', 'time': 'TimeField'} 
    


    
def get_field_dict(field_id, post_dict):
    startswith = 'field_%s_' % (field_id)
    items = [(i[0][len(startswith):], i[1]) for i in post_dict.items() if i[0].startswith(startswith)]
    return dict(items)
    
def get_field_class(field_type):
    if field_type == 'ForeignKey':
        return 'ForeignKey'
    else:
        return field_type + 'Field'
    
def create_model(request):
    if 'syncdb' in request.GET:
        cmd_output = ''
        try:
            cmd_output = os.popen('python manage.py syncdb').read()
            success = True
        except:
            success = False
        response_data = {'success': success, 'cmd_output': cmd_output}
        
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    if 'get_file_path' in request.GET:

        
        return HttpResponse(os.path.join(os.getcwd(), "models.py"))
    if 'list_apps' in request.GET:
        settings_file = ''
        settings_path = ''
        if 'settings.py' in os.listdir('.'):
            settings_path = 'settings.py'
        else:
            for dir in [i for i in os.listdir('.') if os.path.isdir(i)]:
                if 'settings.py' in os.listdir(dir):
                    settings_path = os.path.join(dir, 'settings.py')
        f = open(os.path.join(os.getcwd(), settings_path), 'r')
        settings_file = f.read()
        f.close()
        logging.info("=====================\n%s" % (settings_file))
        f = open(settings_path, 'r')
        settings_lines = f.readlines()
        f.close()
        for i, line in enumerate(settings_lines):
             if line.startswith('INSTALLED_APPS = ('):
                 start = i
                 break
        for i, line in enumerate(settings_lines[start:]):
             if line.startswith(')'):
                 stop = start + i
                 break
        installed_apps = '\n'.join(settings_lines[start:stop])
        apps = [(dirname.strip('./'), os.path.join(os.path.join(os.getcwd(), dirname.strip('./')), "models.py"), dirname.strip('./') in installed_apps) for dirname, dirnames, filenames in os.walk('.') if 'views.py' in os.listdir(dirname) or 'urls.py' in os.listdir(dirname)]
        response_data = {'apps': apps}
        
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    if 'install_app' in request.GET:
        # add app to settings.py
        settings_path = ''
        if 'settings.py' in os.listdir('.'):
            settings_path = 'settings.py'
        else:
            for dir in [i for i in os.listdir('.') if os.path.isdir(i)]:
                if 'settings.py' in os.listdir(dir):
                    settings_path = os.path.join(dir, 'settings.py')
        f = open(settings_path, 'r')
        settings_lines = f.readlines()
        f.close()
        for i, line in enumerate(settings_lines):
             if line.startswith('INSTALLED_APPS = ('):
                 start = i
                 break
        for i, line in enumerate(settings_lines[start:]):
             if line.startswith(')'):
                 stop = start + i
                 break
        new_app = "    '%s',\n" % (request.GET['install_app'])
        settings_lines.insert(stop, new_app)
        new_settings = ''.join(settings_lines)
        f = open(settings_path, 'w')
        f.write(new_settings)
        f.close()
        response_data = {'success': 'true'}
        
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
        
    #response = 'hello' + 'number of fields: %s' % (get_number_of_fields(request.POST))
    #response += str([list(findall(i, '_')) for i in request.POST.keys() if '_' in i])
    #response += str([(get_field_id(i[0]), i[1]) for i in request.POST.keys() if i.startswith('field_')])
    code = "class %s(models.Model):\n" % (request.POST['name'].capitalize()) 
    is_name_field = False
    for field_id in get_field_ids(request.POST):
        field = get_field_dict(field_id, request.POST)
        
        arguments = []
        if field['type'] == 'Char':
            if field['name'] == 'name':
                is_name_field = True
            if 'max_length' in field:
                arguments.append("max_length=%s" % (field['max_length']))
        if field['type'] == 'ForeignKey':
            if 'self' in field:
                arguments.append("'self'")
        elif 'related_model' in field:
            arguments.append("'%s'" % (field['related_model']))
        for i in ['unique', 'null', 'blank']:
            if i in field:
                arguments.append("%s=True" % (i))
        code += "    %s = models.%s(%s)\n" % (field['name'], get_field_class(field['type']), ', '.join(arguments))
    if is_name_field:
        code += """
    def __unicode__(self):
        return '%s' % (self.name)
"""
    else:
        code += """
    def __unicode__(self):
        return ''
"""
    
    #response += str(request.POST.items())
    if 'save' in request.POST:
        try:
           f = open(request.POST['file_path'], 'r')
           file = f.read()
           f.close()
           f = open(request.POST['file_path'], 'w')
           f.write(file + '\n' + code)
           f.close()
        except IOError as e:
           f = open(request.POST['file_path'], 'w')
           f.write('from django.db import models\n\n' + code)
           f.close()
    return HttpResponse(code, content_type='text')