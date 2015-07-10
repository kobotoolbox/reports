from django.db import models
from django.contrib.auth.models import User
import tempfile
import os
import subprocess


class Template(models.Model):
    rmd = models.TextField()
    name = models.TextField()


class Rendering(models.Model):
    # I'm putting a user here because each rendering may access
    # private data that relies on the user for authentication.
    user = models.ForeignKey(User)
    template = models.ForeignKey(Template)
    data = models.URLField()
    md = models.TextField()
    html = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def render(self):
        folder = tempfile.gettempdir()
        filename = '%s.Rmd' % self.template.name

        path = os.path.join(folder, filename)
        with open(path, 'w') as f:
            f.write(self.template.rmd)

        cmd = '''Rscript -e "knitr::knit2html('%(filename)s', quiet=TRUE)"''' % locals()
        subprocess.call(cmd, shell=True, cwd=folder)

        for extension in ['md', 'html']:
            path = os.path.join(folder, self.template.name + '.' + extension)
            with open(path) as f:
                text = f.read()
                setattr(self, extension, text)

        self.save()
            # ## Create temporary file for saving compiled report.
        # report_html = tempfile.NamedTemporaryFile(delete=False)

        # ## Call the compiler.
        # compiler_dir = os.path.join(THIS_DIRECTORY, '..', '..', 'compiler')
        # compiler_path = os.path.join(compiler_dir, 'compiler.R')
        # cmd = ' '.join(['Rscript', compiler_path, config_json.name, report_html.name])
        # 

        # ## Pull the text out of the compiled report.
        # with open(report_html.name) as f:
        #     text = f.read()

        # ## Clean up temporary files.
        # os.remove(config_json.name)
        # os.remove(report_html.name)

        # return HttpResponse(text)
