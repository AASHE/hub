# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0012_remove_contenttype_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='submitted_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='material',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='outreachmaterial',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='photograph',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='video',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"This should work: By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted file(s) in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted file(s), or have obtained all necessary licenses and/or permissions to use the submitted file(s), and that AASHE's use of such file(s) will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
    ]
