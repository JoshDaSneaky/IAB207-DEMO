from travel import db, createApp
app = createApp()
ctx = app.app_context()
ctx.push()
db.create_all()
quit()