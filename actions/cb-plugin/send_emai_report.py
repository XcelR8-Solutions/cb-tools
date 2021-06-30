"""
Plugin: Send Email Report
"""
from common.methods import set_progress
from utilities.mail import email


def run(job, *args, **kwargs):
    set_progress("This will show up in the job details page in the CB UI, and in the job log")

    # Example of how to fetch arguments passed to this plug-in ('server' will be available in
    # some cases)
    server = kwargs.get('server')
    if server:
        set_progress("This plug-in is running for server {}".format(server))

    set_progress("Dictionary of keyword args passed to this plug-in: {}".format(kwargs.items()))
    message = 'Hello from CloudBolt'
    email_context = dict(message=message)
    recipients = ['jbrassard@cloudbolt.io']
    email(slug='attached-report', recipients=recipients, context=email_context)
    if True:
        return "SUCCESS", "Sample output message", ""
    else:
        return "FAILURE", "Sample output message", "Sample error message, this is shown in red"


from tempfile import TemporaryFile
from csv import writer as make_csv_writer
def run(job, *args, **kwargs):
        directory = "/tmp"
        if not os.path.exists(directory):
            os.makedirs(directory)
        base_filename = "eurofxref.csv"
        filename = os.path.join(directory, base_filename)
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(
                [
                    "Date",
                ])
            writer.writerow(
                [
                    "18 October 2019",
                    "16.4566",
                ])
        zip_path = os.path.join("/tmp", base_filename )
        with open(zip_path, "rb") as f:
            contents = f.read()
        message = "Please find attached your report"
        email_context = dict(message=message)
        recipients = ['mfaiz@cloudbolt.io']
        attachments=[('report.zip', contents, 'application/zip')]
        email(slug='attached-report', recipients=recipients, context=email_context, attachments=attachments)
        return "SUCCESS", "Email was sent", ""