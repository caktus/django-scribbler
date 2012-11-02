from django.db import models

class DaysLog(models.Model):
    day = models.DateField(unique=True)
    happenings = models.TextField(
        default="<h1>Things that happened today</h1>\n"
                "<ol>\n  <li>Clock ticked over midnight.</li>\n</ol>")

    def __unicode__(self):
        return "Day's log for {0}".format(self.day)
