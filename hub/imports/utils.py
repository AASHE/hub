import os
from datetime import datetime

import requests
from boto.s3.connection import S3Connection
from django.conf import settings
from django.contrib.auth.models import User
from django.core import files
from django.utils.text import slugify
from io import BytesIO

from hub.apps.content.models import ContentType, Author, File, Website, Image
from hub.apps.metadata.models import (
    Organization, SustainabilityTopic, AcademicDiscipline, InstitutionalOffice)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


from openpyxl import load_workbook


def get_rows(path, sheet):
    wb = load_workbook(path, read_only=True)
    ws = wb[sheet]  # ws is now an IterableWorksheet
    return ws.rows


def sanity_check(rows, columns, column_mappings):
    """
        Just checks to make sure all the organizations exist
        and prints any failures

        Returns a list of resource titles where the issue occurs
    """
    index_list = []

    organizations_key = "Organization%d"
    organizations_id_key = "Organization%did"
    if 'organizations' in column_mappings.keys():
        organizations_key = column_mappings['organizations']
    if 'organizations_id' in column_mappings.keys():
        organizations_id_key = column_mappings['organizations_id']

    count = 0
    for row in rows:

        count += 1
        # skip the headers
        if count == 1:
            continue

        try:
            # match organizations
            for i in range(1, 7):
                name_key = organizations_key % i
                id_key = organizations_id_key % i
                if name_key in columns:
                    org_name = row[columns.index(name_key)].value
                    org_id = row[columns.index(id_key)].value
                    if org_id:
                        try:
                            org = Organization.objects.get(pk=org_id)
                        except Organization.DoesNotExist:
                            print count
                            if count not in index_list:
                                index_list.append(count)
                            print "Org not found: %s (%s)" % (org_name, org_id)
                        if org.org_name.lower() != org_name.lower():
                            print count
                            if count not in index_list:
                                index_list.append(count)
                            print "Org name doesn't match db:"
                            print "%s != %s" % (org.org_name, org_name)

            # match author organizations
            # authors
            author_name_key = "Author%d_Name"
            author_title_key = "Author%d_Title"
            author_org_name_key = "Author%d_Org"
            author_org_id_key = "Author%d_OrgID"
            if 'author_name' in column_mappings.keys():
                author_name_key = column_mappings['author_name']
            if 'author_title' in column_mappings.keys():
                author_title_key = column_mappings['author_title']
            if 'author_org' in column_mappings.keys():
                author_org_name_key = column_mappings['author_org']
            if 'author_org_id' in column_mappings.keys():
                author_org_id_key = column_mappings['author_org_id']
            for i in range(1, 7):
                if author_name_key % i in columns:
                    org_name = row[
                        columns.index(author_org_name_key % i)].value
                    org_id = row[columns.index(author_org_id_key % i)].value
                    if org_name and org_id:
                        # confirm org exists
                        try:
                            org = Organization.objects.get(pk=org_id)
                        except Organization.DoesNotExist:
                            print count
                            if count not in index_list:
                                index_list.append(count)
                            print "Author Org not found: %s (%s)" % (
                                org_name, org_id)
                        if org.org_name.lower() != org_name.lower():
                            print count
                            if count not in index_list:
                                index_list.append(count)
                            print "Author Org name doesn't match db:"
                            print "%s != %s" % (org.org_name, org_name)
        except IndexError:
            # print "Had an index error... !?!"
            pass

    return index_list


def create_file_from_url(parent, file_url, label=None, image=False):
    """
        Thanks:
        http://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
    """

    # Use stream to give access to the raw content
    try:
        request = requests.get(file_url, stream=True)
    except requests.ConnectionError:
        print "Connection error for {}".format(file_url)
        return
    except requests.exceptions.MissingSchema:
        print "Not a URL ||| {}".format(file_url)
        return

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        print "File Request Failed: %s" % file_url
        return
    print "requesting: %s" % file_url

    # Get the filename from the url, used for saving later
    file_name = file_url.split('/')[-1]
    if len(file_name) > 92:
        file_name = file_name[-91:-2]
    if not label:
        label = file_name
    file_name = "uploads/" + file_name

    s3_conn = S3Connection(
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY)
    # TODO hard coding bucket name because stage can't access aashe-hub-prod
    # the problem with this script is that it doesn't put the file under /uploads
    s3_bucket = s3_conn.get_bucket('aashe-hub-production')

    s3_key = s3_bucket.get_key(file_name)
    if s3_key:
        # TODO check if file is same, or resolve to different name
        print 'File name already exists in bucket {}'.format(file_name)
    else:
        s3_key = s3_bucket.new_key(file_name)
        print 'sending {} to S3 bucket'.format(file_name)
        s3_key.set_contents_from_file(BytesIO(request.raw.read()))
        s3_key.set_acl('public-read')

    if not image:
        new_file = File(ct=parent, label=label, affirmation=True)
        # TODO calculate URL based on settings
        new_file.item = 'https://hub-media.aashe.org/{}'.format(file_name)
        new_file.save()
    else:
        image = Image(ct=parent, affirmation=True)
        image.image.save(file_name, files.File(lf))


def create_file_from_path(parent, files_dir, path, upload=True):

    file_name = 'uploads/{}'.format(path)
    if len(path) > 100:
        n, e = os.path.splitext(path)
        file_label = '{}__{}'.format(n[:100 - (len(e) + len('__'))], e)
    else:
        file_label = path

    if upload:

        s3_conn = S3Connection(
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY)
        # TODO hard coding bucket name because stage can't access aashe-hub-prod
        s3_bucket = s3_conn.get_bucket('aashe-hub-production')

        s3_key = s3_bucket.get_key(file_name)
        if s3_key:
            # TODO check if file is same, or resolve to different name
            print 'File name already exists in bucket {}'.format(file_name)
        else:
            try:
                file = open(os.path.join(files_dir, path), 'rb')
            except IOError:
                print 'File not found: {}'.format(
                    os.path.join(files_dir, path))
                return
            s3_key = s3_bucket.new_key(file_name)
            print 'sending {} to S3 bucket'.format(file_name)
            s3_key.set_contents_from_file(file)
            s3_key.set_acl('public-read')
            file.close()

    new_file = File(ct=parent, label=file_label, affirmation=True)
    # TODO calculate URL based on settings
    new_file.item = 'https://hub-media.aashe.org/{}'.format(file_name)
    new_file.save()


def get_base_kwargs(
        columns, column_mappings, row,
        default_permission=ContentType.PERMISSION_CHOICES.member,
        published_date=None,
        submitter=None):
    """
        content_type = models.CharField(max_length=40)
        status = models.CharField(default=STATUS_CHOICES.new)
        permission = models.CharField(default=PERMISSION_CHOICES.member)
        published = models.DateTimeField(blank=True,null=True,)
        submitted_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, blank=True, null=True)
        title = models.CharField(
            max_length=500)  # label set by self.title_label
        slug = models.CharField(max_length=500, editable=False)
        description = models.TextField('Description', blank=True, null=True)

        notes = models.TextField('Notes', blank=True, null=True, default='',
                                 help_text="Internal notes.")
    """
    title_key = "Title"
    if 'title' in column_mappings:
        title_key = column_mappings['title']

    description_key = "Description"
    if 'description' in column_mappings:
        description_key = column_mappings['description']

    desc = row[columns.index(description_key)].value
    if desc:
        desc = desc.replace("\n", "\n\n")
    if not submitter:
        submitter = User.objects.get(email='jade@aashe.org')

    kwargs = {
        'status': ContentType.STATUS_CHOICES.published,
        'permission': default_permission,
        'published': datetime.now().date(),
        'submitted_by': submitter,
        'title': row[columns.index(title_key)].value,
        'slug': slugify(row[columns.index(title_key)].value),
        'description': desc
    }

    if published_date:
        kwargs['published'] = published_date

    return kwargs


def get_base_m2m(
        parent, columns, column_mappings, row,
        bucket_prefix='/uploads/'):
    """
    bucket_prefix is the bucket location where the file is.
    """
    organizations_key = "Organization%d"
    organizations_id_key = "Organization%did"
    if 'organizations' in column_mappings.keys():
        organizations_key = column_mappings['organizations']
    if 'organizations_id' in column_mappings.keys():
        organizations_id_key = column_mappings['organizations_id']

    # match organizations
    for i in range(1, 7):
        name_key = organizations_key % i
        if name_key in columns:
            id_key = organizations_id_key % i
            org_name = row[columns.index(name_key)].value
            org_id = row[columns.index(id_key)].value
            if org_id:
                print "%s: %d" % (org_name, org_id)
                try:
                    org = Organization.objects.get(pk=org_id)
                    if org.org_name.lower() != org_name.lower():
                        print "ORG NAME WRONG!!!"
                        print org.org_name
                        print org_name
                        assert False
                    parent.organizations.add(org)
                except Organization.DoesNotExist:
                    print "***********Organization not found: %s" % org_name

    # match topics
    topic_key = "SustainabilityTopic%d"
    if 'topics' in column_mappings.keys():
        topic_key = column_mappings['topics']
    print "adding topics"
    for i in range(1, 4):
        key = topic_key % i
        if key in columns:
            topic_name = row[columns.index(key)].value
            if topic_name:
                topic = SustainabilityTopic.objects.get(name=topic_name)
                parent.topics.add(topic)
                print topic

    # match disciplines
    disc_key = "AcademicDisc%d"
    if 'disciplines' in column_mappings.keys():
        disc_key = column_mappings['disciplines']
    print "adding disciplines"
    for i in range(1, 4):
        key = disc_key % i
        if key in columns:
            disc_name = row[columns.index(key)].value
            if disc_name:
                print disc_name
                disc = AcademicDiscipline.objects.get(name=disc_name)
                parent.disciplines.add(disc)

    # match institution offices
    inst_key = "OfficeDept%d"
    if 'institutions' in column_mappings.keys():
        inst_key = column_mappings['institutions']
    print "Adding institution offices"
    for i in range(1, 3):
        key = inst_key % i
        if key in columns:
            office_name = row[columns.index(key)].value
            if office_name:
                try:
                    office = InstitutionalOffice.objects.get(name=office_name)
                except InstitutionalOffice.DoesNotExist:
                    office = InstitutionalOffice.objects.create(
                        name=office_name)
                    print "creating office: %s" % office
                parent.institutions.add(office)

    # set keywords
    tag_key = "Tags"
    if 'tags' in column_mappings.keys():
        tag_key = column_mappings['tags']
    print "adding tags"
    tags = row[columns.index(tag_key)].value
    if tags:
        for tag in tags.split(','):
            print tag
            parent.keywords.add(tag)

    # authors
    print "adding authors"
    author_name_key = "Author%dName"
    author_title_key = "Author%dTitle"
    author_org_name_key = "Author%dOrg"
    author_org_id_key = "Author%dOrgID"
    if 'author_name' in column_mappings.keys():
        author_name_key = column_mappings['author_name']
    if 'author_title' in column_mappings.keys():
        author_title_key = column_mappings['author_title']
    if 'author_org' in column_mappings.keys():
        author_org_name_key = column_mappings['author_org']
    if 'author_org_id' in column_mappings.keys():
        author_org_id_key = column_mappings['author_org_id']
    for i in range(1, 7):
        if author_name_key % i in columns:
            name = row[columns.index(author_name_key % i)].value
            title = row[columns.index(author_title_key % i)].value
            org_name = row[columns.index(author_org_name_key % i)].value
            org_id = row[columns.index(author_org_id_key % i)].value
            if name:
                author = Author(ct=parent, name=name, title=title)
                # confirm org exists
                if org_id:
                    try:
                        org = Organization.objects.get(pk=org_id)
                        if org.org_name.lower() != org_name.lower():
                            print "ORG NAME WRONG!!!"
                            print org.org_name
                            print org_name
                            assert False
                        author.organization = org
                        author.save()
                        print author
                    except Organization.DoesNotExist:
                        print "Organization does not exist: %s (%d)" % (
                            org_name, org_id)

    # files
    file_key = "File%d"
    if 'files' in column_mappings.keys():
        file_key = column_mappings['files']
    for i in range(1, 5):
        key = file_key % i
        if key in columns:
            try:
                filename = row[columns.index(key)].value
                if filename:
                    url = "https://hub-media.aashe.org%s%s" % (
                        bucket_prefix, filename)
                    file = File.objects.create(
                        ct=parent, label=filename, item=url, affirmation=True)
            except IndexError:
                # row length varies :(
                pass

    # images
    image_key = "Image%d"
    if 'images' in column_mappings.keys():
        image_key = column_mappings['images']
    for i in range(1, 3):
        key = image_key % i
        if key in columns:
            try:
                filename = row[columns.index(key)].value
                if filename:
                    url = "https://hub-media.aashe.org%s%s" % (
                        bucket_prefix, filename)
                    file = File.objects.create(
                        ct=parent, image=url, affirmation=True)
            except IndexError:
                # row length varies :(
                pass

    # links
    link_key = "Link%d"
    if 'links' in column_mappings.keys():
        link_key = column_mappings['links']
    if 'links_label' in column_mappings.keys():
        label_key = column_mappings['links_label']

    for i in range(1, 5):
        key = link_key % i
        if key in columns:
            url = row[columns.index(key)].value
            if label_key:
                l_key = label_key % i
                label = row[columns.index(l_key)].value
            else:
                label = None
            if url:
                Website.objects.create(ct=parent, url=url, label=label)
