from django.core.management.base import BaseCommand
from grid.models import Grid_data

class Command(BaseCommand):
    help = 'Update state and vehical_type fields to uppercase for all grids'

    def handle(self, *args, **options):
        grids = Grid_data.objects.all()

        for grid in grids:
            # grid.state = grid.state.upper()
            # grid.vehical_type = grid.vehical_type.upper()

            # # Update vehical_subtype based on specific conditions
            # if grid.vehical_subtype == "GVW 12000 - 20000 kgs":
            #     grid.vehical_subtype = "GVW 12000 - 20000"
            # elif grid.vehical_subtype == "GVW 20000 - 40000 kgs":
            #     grid.vehical_subtype = "GVW 20000 - 40000"
            # elif grid.vehical_subtype == "GVW 2500 - 3500 kgs":
            #     grid.vehical_subtype = "GVW 2500 - 3500"
            # elif grid.vehical_subtype == "GVW 3500 - 7500 kgs":
            #     grid.vehical_subtype = "GVW 3500 - 7500"
            # elif grid.vehical_subtype == "GVW 7500 - 12000 kgs":
            #     grid.vehical_subtype = "GVW 7500 - 12000"
            # elif grid.vehical_subtype == "GVW < 7500 kgs":
            #     grid.vehical_subtype = "GVW < 7500"
            # elif grid.vehical_subtype == "GVW Up to 2500 kgs":
            #     grid.vehical_subtype = "GVW Up to 2500"
            # elif grid.vehical_subtype == "GVW exceeding 40000 kgs":
            #     grid.vehical_subtype = "GVW exceeding 40000"

            if grid.vehical_type == "Misc.D":
                grid.vehical_type = "Misc. D"
            
            

            grid.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated state and vehical_type to uppercase for all records.'))
