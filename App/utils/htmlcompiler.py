# Code par "le merveilleux @Guilhem"
# Oui j'ose vous citer

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

loader = FileSystemLoader('./ressources/theme')

env = Environment(
    loader = loader,
    autoescape=select_autoescape()
)

# Ici, on load le theme que l'utilisateur a choisit.
class ThemeCompiler:
  def compile_theme(choosed_theme, output="./www/", data=None):
    template = env.get_template(f"{choosed_theme}.html")
    file = open(f"{output}{choosed_theme}.html", "w", encoding='utf-8')
    file.write(template.render(data = data))
    file.close
    


# Pas besoin de vous montrer que c'est des variables, la synatxe est plutot claire

