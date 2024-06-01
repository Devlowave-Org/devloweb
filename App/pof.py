from flask import render_template, Flask, session, redirect, url_for, g, has_app_context


def proof_of_concept():
    return render_template("pof.html")