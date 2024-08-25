from flask import request, render_template, session, redirect, flash, url_for

def pannel():
    return render_template("templates/admin_space/pannel.html")
