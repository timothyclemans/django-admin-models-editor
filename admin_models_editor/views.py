from django.http import HttpResponse, HttpResponseRedirect
import os
import json
import logging
import re

try:
    import south
    south_installed = True
except:
    south_installed = False

is_simple_mode = False
try:
    from django.conf import settings
    is_simple_mode = settings.ADMIN_MODELS_EDITOR_SIMPLE_MODE
except:
    pass

def is_one_of(items, target):
    for item in items:
        if item == target:
            return True
    return False

def findall(L, value, start=0):
    return [i for i, x in enumerate(L) if x == value][start:]
        
def get_field_id(key):
    indexes_of_seperator = findall(key, '_')
    print list(findall(key, '_'))
    start = indexes_of_seperator[0] + 1
    stop = indexes_of_seperator[1]
    return key[start: stop]
    
def get_choices_id(key):
    print key
    indexes_of_seperator = findall(key, '_')
    print list(findall(key, '_'))
    start = indexes_of_seperator[0] + 1
    stop = indexes_of_seperator[1]
    return key[start: stop]
    
def get_number_of_fields(post_dict):
    return len(set([get_field_id(i) for i in post_dict.keys() if i.startswith('field_')]))

def get_choice_id(key):
    print key
    indexes_of_seperator = findall(key, '_')
    print list(findall(key, '_'))
    start = indexes_of_seperator[2] + 1
    stop = indexes_of_seperator[3]
    return key[start: stop]    
    
def get_field_ids(post_dict):    
    return sorted(set([get_field_id(i) for i in post_dict.keys() if i.startswith('field_')]))

def get_ordered_ids(post_dict):    
    return sorted(set([get_field_id(i) for i in post_dict.keys() if i.startswith('ordered_')]))    

def get_choices_ids(post_dict):    
    return sorted(set([get_choices_id(i) for i in post_dict.keys() if i.startswith('choices_')]))
def get_choice_ids(choices_id, post_dict):    
    return sorted(set([get_choice_id(i) for i in post_dict.keys() if i.startswith('choices_%s_choice' % choices_id)]))

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
    import re
    from django.utils.importlib import import_module
    request.POST = request.POST.copy()
    if 'is_app_name_valid' in request.GET:
        is_valid = True
        app_name = request.GET['is_app_name_valid']
        # validate app_name
        is_app_name_valid = re.match(r'^[a-z][a-z0-9_]+[a-z0-9]$', app_name)
        if not is_app_name_valid:
            is_valid = False
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            is_valid = False
        if app_name in os.listdir('.'):
            is_valid = False
        response_data = {'is_valid': is_valid}
        
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    if 'create_app' in request.POST:
        os.system('python manage.py startapp %s' % (request.POST['app_name']))
        app_name = request.POST['app_name']
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
        new_app = "    '%s',\n" % (app_name)
        settings_lines.insert(stop, new_app)
        new_settings = ''.join(settings_lines)
        f = open(settings_path, 'w')
        f.write(new_settings)
        f.close()
        if south_installed:
            os.system('python manage.py schemamigration %s --initial' % (app_name))
            os.system('python manage.py migrate %s')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if 'is_simple_mode' in request.GET:
        response_data = {'is_simple_mode': is_simple_mode}
        
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
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

        
        return HttpResponse(os.path.join(os.getcwd(), "models.py"), mimetype="text/plain")
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
        apps = sorted(apps, key=lambda x: x[0])
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
    code = ''
    #code += str(request.POST) + '\n\n\n'
    import re
    model_name = ''
    request.POST['name'].capitalize()
    code_from_input = request.POST['code'].split('\n')[0]
    def_lines = ''
    if '    def' in request.POST['code']:
        for i, line in enumerate(request.POST['code'].split('\n')):
            if line.startswith('    def'):
                def_lines = '\n'.join(request.POST['code'].split('\n')[i:])
                break
    default_deflines = """
    def __unicode__(self):
        return ''
"""
    default_deflines = [i.strip() for i in default_deflines.strip().split('\n') if i]
    if [i.strip() for i in def_lines.strip().split('\n') if i] == default_deflines:
        def_lines = ''
    last_code_from_input = request.POST['last_code'].split('\n')[0]
    # check if model name in source changed
    model_name_in_last_source = ''
    model_name_in_code = ''
    if last_code_from_input.startswith('class'):
        m = re.match(r"class (\w+)\(models.Model\):", last_code_from_input)
        try:
            model_name_in_last_source = m.group(1)
        except:
            pass
    if code_from_input.startswith('class'):
        m = re.match(r"class (\w+)\(models.Model\):", code_from_input)
        try:
            model_name_in_code = m.group(1)
        except:
            pass
    if model_name_in_last_source != model_name_in_code:
        model_name = model_name_in_code
    else:
        model_name = request.POST['name']
    
    # grab names of fields if names in code changed
    old_code = request.POST['last_code']
    new_code = request.POST['code']
    new_field_names = []
    if old_code != new_code:
        field_lines = [line for line in new_code.split('\n') if 'models.' in line and not 'models.Model' in line]
        for i, line in enumerate(field_lines):
            #m = re.match(r"    (\w[_]+) = models.(\w+)\((^[\(\)])\)", last_code_from_input)
            #if m:
            if line.startswith('    ') and ' =' in line: 
                start = 4
                stop = line.index(' =')
                new_field_names.append(('field_%s_name' % i, line[start: stop]))
                request.POST['field_%s_name' % i] = line[start: stop]                
                #new_field_names.append('field_%s_name' % i, m.group(1))
                #request.POST['field_%s_name' % i] = m.group(1)
    code += "class %s(models.Model):\n" % (model_name) 
    for choices_id in get_choices_ids(request.POST):
        if 'choices_%s_name' % (choices_id) in request.POST:
            code += '    %s = (\n' % (request.POST['choices_%s_name' % (choices_id)])
            for choice_id in get_choice_ids(choices_id, request.POST):
                code += '        ('
                if 'choices_%s_choice_%s_value' % (choices_id, choice_id) in request.POST:
                    code += "'%s'" % (request.POST['choices_%s_choice_%s_value' % (choices_id, choice_id)])
                code += ', '
                if 'choices_%s_choice_%s_label' % (choices_id, choice_id) in request.POST:
                    code += "'%s'" % (request.POST['choices_%s_choice_%s_label' % (choices_id, choice_id)])
                code += '),\n'
            code += '    )\n'
    is_name_field = False
    for field_id in get_field_ids(request.POST):
        field = get_field_dict(field_id, request.POST)
        
        arguments = []
        if field['type'] == 'Char':
            if field['name'] == 'name':
                is_name_field = True
            if 'max_length' in field:
                arguments.append("max_length=%s" % (field['max_length']))
        elif field['type'] == 'Decimal':
            if 'max_digits' in field:
                arguments.append("max_digits=%s" % (field['max_digits']))
            if 'decimal_places' in field:
                arguments.append("decimal_places=%s" % (field['decimal_places']))
        elif is_one_of(['Email', 'Slug', 'Url'], field['type']):
            defaults = {'Email': 75, 'Slug': 50, 'Url': 200}
            if 'max_length' in field:
                if not int(field['max_length']) == defaults[field['type']]:
                    arguments.append("max_length=%s" % (field['max_length']))
        elif is_one_of(['File', 'Image'], field['type']):
            if 'upload_to' in field:
                arguments.append("upload_to='%s'" % (field['upload_to']))
            if field['type'] == 'Image':
                if 'height' in field:
                    arguments.append("height=%s" % (field['height']))
                if 'width' in field:
                    arguments.append("width=%s" % (field['width']))
        elif is_one_of(['ForeignKey', 'ManyToMany', 'OneToOne'], field['type']):
            if 'self' in field:
                arguments.append("'self'")
            elif 'related_model' in field:
                related_model = field['related_model'].strip("'")
                related_model = related_model.strip('"')
                arguments.append("'%s'" % (related_model))
            if field['type'] == 'ManyToMany':
                if 'through' in field:
                    through = field['through'].strip("'")
                    through = through.strip('"')
                    arguments.append("through='%s'" % (through))
        for i in ['unique', 'null', 'blank', 'auto_now', 'auto_now_add']:
            if i in field:
                arguments.append("%s=True" % (i))
        if not 'required' in field:
            if not field['type'] == 'Char':
                arguments.append("null=True")
            arguments.append("blank=True")
        if 'default' in field:
            if field['default']:
                if is_one_of(['Char', 'Text'], field['type']):
                    arguments.append("default='%s'" % (field['default']))
                elif is_one_of(['Boolean', 'NullBoolean'], field['type']):
                    if field['default'] == 'true':
                        arguments.append("default=True")
                    elif field['default'] == 'false':
                        arguments.append("default=False")
                else:
                    arguments.append("default=%s" % (field['default']))
        if 'choices' in field:
            if not field['choices'] == 'no_choices':
                arguments.append("choices=%s" % (field['choices']))
        code += "    %s = models.%s(%s)\n" % (field['name'], get_field_class(field['type']), ', '.join(arguments))
    
    ordered_ids = get_ordered_ids(request.POST)
    ordered_field_names = ', '.join(["'-%s'" % (request.POST['field_%s_name' % (i)]) if 'ordered_%s_descending' % (i) in request.POST else "'%s'" % (request.POST['field_%s_name' % (i)]) for i in ordered_ids])
    if ordered_ids:
        code += """
    class Meta:
        ordering = [%s]
""" % (ordered_field_names)
        
    if def_lines:
        code += '\n' + def_lines
    else:
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
    cmd_output = ''
    refresh = False
    #response += str(request.POST.items())
    if 'save' in request.POST:
        print 'SAVE =========\n' * 50
        print 
        filepath = request.POST['file_path'].strip()
        try:
            f = open(filepath, 'r')
            codefile = f.read()
            f.close()
            f = open(filepath, 'w')
            f.write(codefile + '\n' + code)
            f.close()
        except IOError as e:
            f = open(filepath, 'w')
            f.write('from django.db import models\n\n' + code)
            f.close()
        if south_installed:
            os.system('python manage.py schemamigration %s --auto' % (app_name))
            os.system('python manage.py migrate %s')
        else:
            cmd_output = os.popen('python manage.py syncdb').read()
        refresh = True
    
    response_data = {'post_dict': str(request.POST), 'new_field_names': new_field_names, 'code': code, 'model_name': model_name, 'cmd_output': cmd_output, 'refresh': refresh}
        
    return HttpResponse(json.dumps(response_data), mimetype="application/json")    