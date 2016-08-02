from hub.apps.content.models import ContentType

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Merge any duplicate tags'

    def handle(self, *args, **options):
        print "merging tags!"

        tag_model = ContentType.keywords.tag_model

        # merge tags with leading spaces where possible
        for tag in tag_model.objects.order_by('name'):
            # fix empty tags
            if tag.name == '':
                tag.delete()
            elif tag.name[0] == " ":
                # if there is another tag with this name merge into that one
                try:
                    good_tag = tag_model.objects.get(name=tag.name[1:])
                    print "merging: '%s' into '%s'" % (tag.name, good_tag.name)
                    good_tag.merge_tags([tag])
                    # make sure it's deleted (sometimes merge doesn't delete!?)
                    try:
                        bad_tag = tag_model.objects.get(name=tag.name)
                        if not bad_tag.get_related_objects():
                            bad_tag.delete()
                        else:
                            err_msg = "Bad Tag (%s) still has objects!!!"
                            print err_msg % bad_tag.name()
                    except:
                        pass  # expected
                except tag_model.DoesNotExist:
                    print "good tag not found for: '%s'" % tag.name

        # remove leading spaces from all other tags
        for tag in tag_model.objects.order_by('name'):
            if tag.name[0] == " ":
                print "fixing '%s'" % tag.name
                tag.name = tag.name[1:]
                tag.save()

        # do any slugs have a "1" in thems?
        for tag in tag_model.objects.order_by('name'):
            if tag.slug[-1] == "1":
                print "found: '%s'" % tag.slug
                try:
                    good_tag = tag_model.objects.get(slug=tag.slug[0:-2])
                    print "merging: '%s' into '%s'" % (tag.slug, good_tag.slug)
                    good_tag.merge_tags([tag])
                except tag_model.DoesNotExist:
                    print "fixing '%s'" % tag.slug
                    tag.slug = tag.slug[0:-2]
                    tag.save()
