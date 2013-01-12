from flask import render_template
from flask import Flask
from flask import request,url_for
from flask import redirect,Response
import sqlite3
app = Flask(__name__)
@app.route("/")
@app.route("/<imagename>",methods=["GET", "POST"])
def LoadSaveImage(imagename=None):
	if request.method=="POST":
		data=request.form["pdata"]
		name=request.form["pname"]
		conn=sqlite3.connect("Image.db")
		c=conn.cursor()
		image=(name,data)
		iname=(name,)
		c.execute("""CREATE TABLE IF NOT EXISTS Image(file text,data text)""" )
		c.execute("""DELETE FROM Image WHERE file=?""",iname)
		c.execute("""INSERT INTO Image VALUES (?,?)""",image)
		conn.commit()
		conn.close()
		
	else:
		if imagename:
			conn=sqlite3.connect("Image.db")
			c=conn.cursor()
			filename=(imagename,)
			c.execute("""CREATE TABLE IF NOT EXISTS Image(file text,data text)""")
			t=0
			for row in c.execute("""SELECT * FROM Image WHERE file=?""",filename):
				t=t+1
			if t>0:		
				data=""
				for row in c.execute("""SELECT * FROM Image WHERE file=?""",filename):
					(name,data)=row
				resp = Response("""<script>var data=JSON.parse(' """+data+""" ');</script>"""+render_template("paint.html"), status=200, mimetype='html')
				return resp					
			else:
				return "Image not Found"
			
		else:
			return render_template("paint.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

