# Code par "le merveilleux @Guilhem"
# Oui j'ose vous citer

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

loader = FileSystemLoader('./ressources/theme')

env = Environment(
    loader = loader,
    autoescape=select_autoescape()
)

# Ici, on load le theme que l'utilisateur a choisit.


projects = [
  {
    "title": "Project 1",
    "description": "Description of project 1",
    "image": "img/eco1.jpg"
  },
  {
    "title": "Project 2", 
    "description": "Description of project 2",
    "image": "img/eco1.jpg"
  },
  {
    "title": "Project 3",
    "description": "Description of project 3",
    "image": "img/eco1.jpg"
  }
]

arguments = [
  {
    "title": "Valeur 1",
    "strong": "Description of project 1",
    "image": "img/feuille.svg"
  },
  {
    "title": "Valeur 2",
    "strong": "Description of project 1",
    "image": "img/feuille.svg"
  },
  {
    "title": "Valeur 3",
    "strong": "Description of project 1",
    "image": "img/feuille.svg"
  }
]

trust = [
  {
    "title": "Project 1",
    "description": "Description of project 1",
    "image": "Template_fichiers/feuille.svg"
  },
  {
    "title": "Project 1",
    "description": "Description of project 1",
    "image": "Template_fichiers/feuille.svg"
  },
  {
    "title": "Project 1",
    "description": "Description of project 1",
    "image": "img/feuille.svg"
  },
  {
    "title": "Project 1",
    "description": "Description of project 1",
    "image": "Template_fichiers/feuille.svg"
  }
]

images = ["https://picsum.photos/900/1600?blur=2",
          "https://picsum.photos/seed/funa/1600/900?blur=2",
          "https://picsum.photos/seed/fantai/1600/900?blur=2",
          "https://picsum.photos/seed/benkuku/1600/900?blur=2",
          "https://picsum.photos/seed/vaati/1600/900?blur=2"]

# Pas besoin de vous montrer que c'est des variables, la synatxe est plutot claire

def compile_theme(choosed_theme, projects, arguments, trust, images, output="/www/", title="Mon Super", title_strong="Titre", attache="on des", attache_strong="Conséquances", description="Ceci est une description, mais parse avec Jijna 🤌", valeurs="On a vraiment des superbes valeurs :"):
    template = env.get_template(f"{choosed_theme}.html")
    file = open(f"{output}{choosed_theme}.html", "w", encoding='utf-8')
    file.write(template.render(
        title=title,
        title_strong=title_strong,
        attache=attache,
        attache_strong=attache_strong, 
        description=description,
        projets=projects,
        arguments=arguments,
        trust=trust,
        valeurs=valeurs,
        images=images
        ))
    file.close