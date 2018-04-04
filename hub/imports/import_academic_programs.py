from utils import get_rows, get_base_kwargs, get_base_m2m, sanity_check
from hub.apps.content.types.academic import AcademicProgram
from hub.apps.metadata.models import ProgramType, SustainabilityTopic

from datetime import datetime

columns = [
    "Program Name",
    "Description",
    "Organization1",
    "Organization1 ID",
    "Organization2",
    "Organization2 ID",
    "Topic1",
    "Topic2",
    "Acad Discipline1",
    "Acad Discipline2",
    "Acad Discipline3",
    "Tag(s): (comma separated)",
    "Year Founded (200x)",
    "Program Type",
    "Learning Outcomes",
    "Expected completion time",
    "Approx # students completing program annually",
    "Distance Ed.",
    "Commitment",
    "Link URL",
]

column_mappings = {
    'title': "Program Name",
    'description': "Description",
    'organizations_id': "Organization%d ID",
    'topics': "Topic%d"
    'disciplines': "Acad Discipline%d",
    'keywords': "Tag(s): (comma separated)",
    'date_created': "Year Founded (200x)",
    'program_type': "Program Type",
    'outcomes': "Learning Outcomes",
    'completion': "Expected completion time",
    'num_students': "Approx # students completing program annually",
    'distance': "Distance Ed.",
    'commitment': "Commitment",
    'website_url': "Link URL",
}

#foreign keys
# program_type,
