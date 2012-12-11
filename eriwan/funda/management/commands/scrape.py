from django.core.management.base import NoArgsCommand, make_option

class Command(NoArgsCommand):
  help = "Scrape the Parliament Website and Update the Models"
  option_list = NoArgsCommand.option_list + (
    make_option('--verbose', action='store_true'),
    )
  def handle_noargs(self, **options):
    print "works!"
