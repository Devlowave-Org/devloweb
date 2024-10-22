from flask import render_template, request, redirect, url_for

def load(user_db):
    return redirect("/admin_space/panel/Infos")

def load_infos_section(user_db):
    return render_template("admin_space/Infos.html")