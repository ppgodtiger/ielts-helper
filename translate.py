from flask import Blueprint, render_template, request
from english_dict import english_dict


dft_blueprint = Blueprint("wp1",__name__) #第一个是字符串

@dft_blueprint.route("/translate",methods = ['GET','POST'])
def translate():
    result = ""
    if request.method=="POST":
        keyword = request.form.get("keyword")
        print(keyword)
        result = english_dict.query(keyword)
    return render_template("translate.html",result = result)
