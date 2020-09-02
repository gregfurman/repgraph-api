from app import create_app

app=create_app()
app.run(debug=True,threaded=True,port=8000,host="localhost")