# routes_gestion_user.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les user.

import pymysql
from flask import render_template, flash, redirect, url_for, request
from APP_INVENTORY import obj_mon_application
from APP_INVENTORY.USER.data_gestion_user import Gestionuser
from APP_INVENTORY.DATABASE.erreurs import *
import re

@obj_mon_application.route("/user_afficher")
def user_afficher():
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_user = Gestionuser()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionuser()
            # Fichier data_gestion_user.py
            data_user = obj_actions_user.user_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data user", data_user, "type ", type(data_user))
            # Différencier les messages si la table est vide.
            if data_user:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash("Données Objet affichées !!", "success")
            else:
                flash("""La table "t_user" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGF Erreur générale. {erreur}","danger")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("user/user_afficher.html", data=data_user)


# OM 2020.04.06 Pour une simple démo. On insère deux fois des valeurs dans la table user
# Une fois de manière fixe, vous devez changer les valeurs pour voir le résultat dans la table "t_user"
# La 2ème il faut entrer la valeur du titre du user par le clavier, il ne doit pas être vide.
# Pour les autres valeurs elles doivent être changées ci-dessous.
# Une des valeurs est "None" ce qui en MySql donne "NULL" pour l'attribut "t_user.cover_link_user"
# Pour la tester http://127.0.0.1:5005/user_add
@obj_mon_application.route("/user_add", methods=['GET', 'POST'])
def user_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_user = Gestionuser()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "user_add.html"
            Nom = request.form['Nom_html']
            print("Ici ok")
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            # if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
            #                 equipe_user):
            #     print("Ici OK")
            #     # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
            #     flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
            #           f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")
            #     # On doit afficher à nouveau le formulaire "user_add.html" à cause des erreurs de "claviotage"
            #     return render_template("user/user_add.html")
            # else:

            # Constitution d'un dictionnaire et insertion dans la BD
            valeurs_insertion_dictionnaire = {"value_Nom": Nom}
            obj_actions_user.add_user_data(valeurs_insertion_dictionnaire)

            # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Données insérées !!", "success")
            print(f"Données insérées !!")
            # On va interpréter la "route" 'user_afficher', car l'utilisateur
            # doit voir le nouveau user qu'il vient d'insérer. Et on l'affiche de manière
            # à voir le dernier élément inséré.
            return redirect(url_for('user_afficher', order_by = 'DESC', id_user_sel=0))

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
    return render_template("user/user_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /user_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un user de user par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/user_edit', methods=['POST', 'GET'])
def user_edit ():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "user_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "id_user" du formulaire html "user_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_user"
            # grâce à la variable "id_user_edit_html"
            # <a href="{{ url_for('user_edit', id_user_edit_html=row.id_user) }}">Edit</a>
            id_user_edit = request.values['id_user_edit_html']

            # Pour afficher dans la console la valeur de "id_user_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_user_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_user": id_user_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_user = Gestionuser()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_user = obj_actions_user.edit_user_data(valeur_select_dictionnaire)
            print("dataiduser ", data_id_user, "type ", type(data_id_user))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le user d'un user !!!", "success")

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

    return render_template("user/user_edit.html", data=data_id_user)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /user_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un user de user par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/user_update', methods=['POST', 'GET'])
def user_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "user_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du user alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "id_user" du formulaire html "user_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_user"
            # grâce à la variable "id_user_edit_html"
            # <a href="{{ url_for('user_edit', id_user_edit_html=row.id_user) }}">Edit</a>
            id_user_edit = request.values['id_user_edit_html']

            # Récupère le contenu du champ "equipe_user" dans le formulaire HTML "userEdit.html"
            Nom = request.values['Nom_html']
            valeur_edit_list = [{'id_user': id_user_edit, 'Nom': Nom}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            Nom):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "equipe_user" dans le formulaire HTML "userEdit.html"
                # equipe_user = request.values['name_edit_equipe_user_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")

                # On doit afficher à nouveau le formulaire "user_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "user_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_user': 13, 'equipe_user': 'philosophique'}]
                valeur_edit_list = [{'id_user': id_user_edit, 'Nom': Nom}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "user_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('user/user_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_user": id_user_edit, "value_Nom": Nom}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_user = Gestionuser()

                # La commande MySql est envoyée à la BD
                data_id_user = obj_actions_user.update_user_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataiduser ", data_id_user, "type ", type(data_id_user))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur user modifiée. ", "success")
                # On affiche les user avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('user_afficher', order_by="ASC", id_user_sel=id_user_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème user ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_equipe_user_html" alors on renvoie le formulaire "EDIT"
    return render_template('user/user_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /user_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un user de user par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/user_select_delete', methods=['POST', 'GET'])
def user_select_delete ():
    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_user = Gestionuser()
            # OM 2019.04.04 Récupère la valeur de "iduserDeleteHTML" du formulaire html "userDelete.html"
            id_user_delete = request.args.get('id_user_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_user": id_user_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_user = obj_actions_user.delete_select_user_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur user_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur user_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('user/user_delete.html', data=data_id_user)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /userUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un user, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/user_delete', methods=['POST', 'GET'])
def user_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_user = Gestionuser()
            # OM 2019.04.02 Récupère la valeur de "id_user" du formulaire html "userAfficher.html"
            id_user_delete = request.form['id_user_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_user": id_user_delete}

            data_user = obj_actions_user.delete_user_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des user des user
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les user
            return redirect(url_for('user_afficher',order_by="ASC",id_user_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "user" de user qui est associé dans "t_user_user".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des user !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce user est associé à des user dans la t_user_user !!! : {erreur}")
                # Afficher la liste des user des user
                return redirect(url_for('user_afficher', order_by="ASC", id_user_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur user_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur user_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('user/user_afficher.html', data=data_user)

