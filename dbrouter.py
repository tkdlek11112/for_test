class DbRouter:
    def db_for_read(self, model, **hints):
        return 'read1'

    def db_for_write(self,model,**hints):
        return 'default'  # return None

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default', 'read')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
