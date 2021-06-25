from background_task import background


@background(schedule=60)
def update_label(item, slug):
    # lookup user by id and send them a message
    item.label = None
    item.save()
