from flask import request, render_template, session, redirect, flash, url_for

def pannel():
    return render_template("admin_pannel/pannel.html")
