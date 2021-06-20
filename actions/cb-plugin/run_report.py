from reportengines.internal.export_utils import group_environments_cost_summary_csv
from accounts.models import UserProfile, Group
from utilities.logger import ThreadLogger
from utilities.mail import email
from django.conf import settings
from calendar import monthrange
from io import StringIO

import tempfile
import datetime
import csv
import time

logger = ThreadLogger(__name__)


# Fake request object, required to run the report
class FakeRequest(object):
    def __init__(self, profile, group_id, start_date, end_date):
        self.GET = {}

        self.GET['group'] = group_id
        self.GET['start_date'] = start_date
        self.GET['end_date'] = end_date
        self.GET['rep_format'] = 'csv'

        self.profile = profile
        self.user = profile.user

    def get_user_profile(self):
        return self.profile


def run(jobs=None, **kwargs):
    # The current time, used to build date strings
    now = datetime.datetime.now()

    # Constructs the start and end dates to run the report
    # Expects "YYYY-MM-DD" string
    if now.month == 1:
        start_str = '{}-{:02d}-01'.format((now.year - 1), (now.month - 1))
        end_str = '{}-{:02d}-{}'.format((now.year - 1), (now.month - 1), (monthrange(now.year - 1, now.month - 1))[1])
    else:
        start_str = '{}-{:02d}-01'.format(now.year, (now.month - 1))
        end_str = '{}-{:02d}-{}'.format(now.year, (now.month - 1), (monthrange(now.year, now.month - 1))[1])

    profile_id = {{profile_id}}
    profile = UserProfile.objects.get(id=profile_id)
    csv_array = []
    group_count = 0

    for g in Group.objects.all():
        request = FakeRequest(
            profile,
            g.id,
            start_str,
            end_str,
        )

        report_csv = group_environments_cost_summary_csv(request, profile)
        logger.info('\n\n{}\n'.format(report_csv))
        r = StringIO(report_csv)
        reader = csv.reader(r, delimiter=',')
        line_count = 0

        for row in reader:
            if line_count == 0 and group_count == 0:
                row.insert(0, 'group_name')
                csv_array.append(row)
                line_count += 1
            elif line_count == 0:
                line_count += 1
                continue
            else:
                row.insert(0, g.name)
                csv_array.append(row)

        group_count += 1

    file = tempfile.NamedTemporaryFile()

    with open(file.name, 'w') as f:
        writer = csv.writer(f, delimiter=',')

        for l in csv_array:
            writer.writerow(l)

    with open(file.name, 'r') as f:
        email_attachments = [('{}_{}_{}.csv'.format('All_Groups', start_str, end_str), f.read(), 'text/csv')]

    email_context = {'subject': 'Group Server Cost Summary Report', }
    recipients = []

    email(
        recipients=recipients,
        attachments=email_attachments,
        context=email_context,
    )

    file.close()

    return "", "", ""