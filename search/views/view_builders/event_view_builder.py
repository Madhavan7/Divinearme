class EventViewDirector():
    pass

class EventViewBuilder():
    def build(self, event, response):
        pass
    
class EventNormalView(EventViewBuilder):
    def build(self, event, response):
        return super().build(event, response)
    
class EventAdminView(EventViewBuilder):
    def build(self, event, response):
        return super().build(event, response)
    
class EventGuestView(EventViewBuilder):
    def build(self, event, response):
        return super().build(event, response)