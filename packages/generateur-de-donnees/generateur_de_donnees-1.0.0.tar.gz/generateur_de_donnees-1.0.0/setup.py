from setuptools import setup

setup(
    name='generateur_de_donnees',
    version='1.0.0',    
    description='Module de génération de données numérique et textuel',
    url='https://github.com/Energisse/generateur_de_donnees',  
    packages=['src'],
    install_requires=['datetime',
                      'numpy', 
                      'requests',
                      'pdfkit',
                      'bs4',
                      'markdownify',
                      'pandas',
                      ],

)
