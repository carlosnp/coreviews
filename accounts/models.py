# python
from datetime import timedelta, datetime, date
# Django
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.utils.timesince import timesince
from django.db.models.signals import pre_save, post_save
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l