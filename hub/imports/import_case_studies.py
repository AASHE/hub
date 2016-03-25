from utils import get_rows, get_base_kwargs, get_base_m2m, sanity_check
from hub.apps.content.types.casestudies import CaseStudy
from hub.apps.content.models import ContentType
        
from aashe.aasheauth.services import AASHEUserService
from aashe.aasheauth.middleware import AASHEAccountMiddleware

import datetime

columns = [
    "Title",
    "Project Overview",
    "Org1 Name",
    "Org1 ID",
    "Org2 Name",
    "Org2 ID",
    "Org3 Name",
    "Org3 ID",
    "Sust_Topic1",
    "Sust_Topic2",
    "Sust_Topic3",
    "Acad_Discipline1",
    "Acad_Discipline2",
    "Office_Department1",
    "Office_Department2",
    "Tags",
    "Background",
    "Project Goals",
    "Project Implementation",
    "Project Timeline",
    "Financing",
    "Project Results and Realized Benefits",
    "Lessons Learned",
    "Author1_Name",
    "Author1_Title",
    "Author1_Organization",
    "Author1_Organization_ID",
    "Author1_Email",
    "Author2_Name",
    "Author2_Title",
    "Author2_Organization",
    "Author2_Organization_ID",
    "Author2_Email",
    "Author3_Name",
    "Author3_Title",
    "Author3_Organization",
    "Author3_Organization_ID",
    "Author3_Email",
    "Author4_Name",
    "Author4_Title",
    "Author4_Organization",
    "Author4_Organization_ID",
    "Author4_Email",
    "Author5_Name",
    "Author5_Title",
    "Author5_Organization",
    "Author5_Organization_ID",
    "Author5_Email",
    "Author6_Name",
    "Author6_Title",
    "Author6_Organization",
    "Author6_Organization_ID",
    "Author6_Email",
    "Image1",
    "Image2",
    "Image3",
    "Image4",
    "Image5",
    "File1",
    "File2",
    "File3",
    "File4",
    "File5",
    "Link1",
    "Link2",
    "Date Submitted"
]

column_mappings = {
    'topics': "Sust_Topic%d",
    'organizations': "Org%d Name",
    'organizations_id': "Org%d ID",
    'disciplines': "Acad_Discipline%d",
    'files': "File%d",
    'links': "Link1%d",
    'description': "Project Overview",
    'author_name': "Author%d_Name",
    'author_title': "Author%d_Title",
    'author_org': "Author%d_Organization",
    'author_org_id': "Author%d_Organization_ID"
}

def get_obj_kwargs():
    """
        "Background",
        "Project Goals",
        "Project Implementation",
        "Project Timeline",
        "Financing",
        "Project Results and Realized Benefits",
        "Lessons Learned",
        
        background = models.TextField
        goals = models.TextField
        implementation = models.TextField
        timeline = models.TextField
        financing = models.TextField
        results = models.TextField
        lessons_learned = models.TextField
        consider_for_award = models.BooleanField('Student Leadership Award',
            help_text='''Would you like this case study to be considered for an
            AASHE Student Leadership Award? The first author must be a student.''')
    """
    kwargs = {}
    
    kwargs['consider_for_award'] = False
    
    #background
    def update_kwargs_with_value(column_name, key_name, kwargs):
        _value = row[columns.index(column_name)].value
        if _value:
            kwargs[key_name] = _value
            
    key_map = [
        ("Background", 'background'),
        ("Project Goals", 'goals'),
        ("Project Implementation", 'implementation'),
        ("Project Timeline", 'timeline'),
        ("Financing", 'financing'),
        ("Project Results and Realized Benefits", 'results'),
        ("Lessons Learned", 'lessons_learned')
    ]
    
    for mapping in key_map:
        update_kwargs_with_value(mapping[0], mapping[1], kwargs)
    
    return kwargs

# run the sanity check first
rows = get_rows('hub/imports/fixtures/case_studies.xlsx', 'Sheet1')
skip_index_list = sanity_check(rows, columns, column_mappings)
print "SKIP"
print skip_index_list
    
rows = get_rows('hub/imports/fixtures/case_studies.xlsx', 'Sheet1')

count = 0
for row in rows:
    
    count += 1
    if count == 1 or count in skip_index_list:
        continue
    print count
    if row[0].value == None:
        break
        
    service = AASHEUserService()
    middleware = AASHEAccountMiddleware()
    email = row[columns.index("Author1_Email")].value
    user = None
    if email:
        user_dict = service.get_by_email(email)
        if user_dict:
            profile = middleware.get_full_drupal_profile(user_dict[0]['uid'])
            aasheuser = middleware.get_aasheuser_from_user_dict(user_dict[0], profile, 'bogus')
            user = aasheuser.user

    kwargs = get_base_kwargs(
        columns, column_mappings, row,
        published_date=row[columns.index("Date Submitted")].value,
        submitter=user)
    kwargs.update(get_obj_kwargs())
    program = CaseStudy.objects.create(**kwargs)
    get_base_m2m(program, columns, column_mappings, row)
