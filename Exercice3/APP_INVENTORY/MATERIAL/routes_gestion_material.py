# routes_gestion_material.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les material.

from flask import render_template, flash, redirect, url_for, request
from APP_INVENTORY import obj_mon_application
from APP_INVENTORY.MATERIAL.data_gestion_material import GestionMaterials
from APP_INVENTORY.DATABASE.erreurs import *
# OM 2020.04.10 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /material_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/material_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/material_afficher/<string:order_by>/<int:id_material_sel>", methods=['GET', 'POST'])
def material_afficher(order_by,id_material_sel):
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_material = GestionMaterials()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionMaterials()
            # Fichier data_gestion_material.py
            # "order_by" permet de choisir l'ordre d'affichage des material.
            data_material = obj_actions_material.material_afficher_data(order_by, id_material_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data material", data_material, "type ", type(data_material))

            # Différencier les messages si la table est vide.
            if not data_material and id_material_sel == 0:
                flash("""La table "t_material" est vide. !!""", "warning")
            elif not data_material and id_material_sel > 0:
                # Si l'utilisateur change l'id_material dans l'URL et que le material n'existe pas,
                flash(f"Le material demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_material" est vide.
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données material affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("material/material_afficher.html", data=data_material)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /material_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "material_add.html"
# Pour la tester http://127.0.0.1:5005/material_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/material_add", methods=['GET', 'POST'])
def material_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_material = GestionMaterials()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "material_add.html"
            name_material = request.form['name_material_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            name_material):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")
                # On doit afficher à nouveau le formulaire "material_add.html" à cause des erreurs de "claviotage"
                return render_template("material/material_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_material": name_material}
                obj_actions_material.add_material_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'material_afficher', car l'utilisateur
                # doit voir le nouveau material qu'il vient d'insérer. Et on l'affiche de manière
                # à voir le dernier élément inséré.
                return redirect(url_for('material_afficher', order_by = 'DESC', id_material_sel=0))

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur:
            flash(f"Autre erreur {erreur}", "danger")
            raise MonErreur(f"Autre erreur")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(
                f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("material/material_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /material_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un material de user par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/material_edit', methods=['POST', 'GET'])
def material_edit ():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "material_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "id_material" du formulaire html "material_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_material"
            # grâce à la variable "id_material_edit_html"
            # <a href="{{ url_for('material_edit', id_material_edit_html=row.id_material) }}">Edit</a>
            id_material_edit = request.values['id_material_edit_html']

            # Pour afficher dans la console la valeur de "id_material_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_material_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_material": id_material_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_material = GestionMaterials()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_material = obj_actions_material.edit_material_data(valeur_select_dictionnaire)
            print("dataIdmaterial ", data_id_material, "type ", type(data_id_material))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le material d'un film !!!", "success")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            # On indique un problème, mais on ne dit rien en ce qui concerne la résolution.
            print("Problème avec la BD ! : %s", erreur)
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']}"
                                      f"et son status {msg_erreurs['ErreurConnexionBD']['status']}")

    return render_template("material/material_edit.html", data=data_id_material)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /material_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un material de user par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/material_update', methods=['POST', 'GET'])
def material_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "material_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du material alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "id_material" du formulaire html "material_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_material"
            # grâce à la variable "id_material_edit_html"
            # <a href="{{ url_for('material_edit', id_material_edit_html=row.id_material) }}">Edit</a>
            id_material_edit = request.values['id_material_edit_html']

            # Récupère le contenu du champ "intitule_material" dans le formulaire HTML "materialEdit.html"
            name_material = request.values['name_edit_material_html']
            valeur_edit_list = [{'id_material': id_material_edit, 'material': name_material}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            name_material):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_material" dans le formulaire HTML "materialEdit.html"
                # name_material = request.values['name_edit_material_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")

                # On doit afficher à nouveau le formulaire "material_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "material_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_material': 13, 'intitule_material': 'philosophique'}]
                valeur_edit_list = [{'id_material': id_material_edit, 'material': name_material}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "material_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('material/material_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_material": id_material_edit, "value_material": name_material}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_material = GestionMaterials()

                # La commande MySql est envoyée à la BD
                data_id_material = obj_actions_material.update_material_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdmaterial ", data_id_material, "type ", type(data_id_material))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur material modifiée. ", "success")
                # On affiche les material avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('material_afficher', order_by="ASC", id_material_sel=id_material_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème material ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_material_html" alors on renvoie le formulaire "EDIT"
    return render_template('material/material_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /material_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un material de user par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/material_select_delete', methods=['POST', 'GET'])
def material_select_delete ():
    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_material = GestionMaterials()
            # OM 2019.04.04 Récupère la valeur de "idmaterialDeleteHTML" du formulaire html "materialDelete.html"
            id_material_delete = request.args.get('id_material_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_material": id_material_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_material = obj_actions_material.delete_select_material_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur material_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur material_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('material/material_delete.html', data=data_id_material)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /materialUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un material, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/material_delete', methods=['POST', 'GET'])
def material_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_material = GestionMaterials()
            # OM 2019.04.02 Récupère la valeur de "id_material" du formulaire html "materialAfficher.html"
            id_material_delete = request.form['id_material_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_material": id_material_delete}

            data_material = obj_actions_material.delete_material_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des material des user
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les material
            return redirect(url_for('material_afficher',order_by="ASC",id_material_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "material" de user qui est associé dans "t_material_user".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des user !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce material est associé à des user dans la t_material_user !!! : {erreur}")
                # Afficher la liste des material des user
                return redirect(url_for('material_afficher', order_by="ASC", id_material_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur material_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur material_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('material/material_afficher.html', data=data_material)
