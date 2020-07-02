# routes_gestion_material_user.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les films et les genres.

from flask import render_template, request, flash, session
from APP_INVENTORY import obj_mon_application
from APP_INVENTORY.MATERIAL.data_gestion_material import GestionMaterials
from APP_INVENTORY.MATERIAL_USER.data_gestion_material_user import GestionMaterialsUsers


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /materials_users_afficher_concat
# Récupère la liste de tous les films et de tous les genres associés aux films.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/materials_users_afficher_concat/<int:id_user_sel>", methods=['GET', 'POST'])
def materials_users_afficher_concat (id_user_sel):
    print("id_user_sel ", id_user_sel)
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_materials = GestionMaterialsUsers()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionMaterials()
            # Fichier data_gestion_genres.py
            data_materials_users_afficher_concat = obj_actions_materials.materials_users_afficher_data_concat(id_user_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data genres", data_materials_users_afficher_concat, "type ", type(data_materials_users_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_materials_users_afficher_concat:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichés dans GenresFilms!!", "success")
            else:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_genres_films" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("material_user/material_user_afficher.html",
                           data=data_materials_users_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.21 Définition d'une "route" /gf_edit_material_user_selected
# Récupère la liste de tous les genres du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_material_user_selected", methods=['GET', 'POST'])
def gf_edit_material_user_selected ():
    if request.method == "GET":
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_materials = GestionMaterials()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionMaterials()
            # Fichier data_gestion_genres.py
            # Pour savoir si la table "t_genres" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(material_user_modifier_tags_dropbox.html)
            data_materials_all = obj_actions_materials.materials_afficher_data('ASC', 0)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_materials = GestionMaterialsUsers()

            # OM 2020.04.21 Récupère la valeur de "id_film" du formulaire html "material_user_afficher.html"
            # l'utilisateur clique sur le lien "Modifier genres de ce film" et on récupère la valeur de "id_film" grâce à la variable "id_user_materials_edit_html"
            # <a href="{{ url_for('gf_edit_material_user_selected', id_user_materials_edit_html=row.id_film) }}">Modifier les genres de ce film</a>
            id_user_materials_edit = request.values['id_user_materials_edit_html']

            # OM 2020.04.21 Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_user_materials_edit'] = id_user_materials_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_user_selected_dictionnaire = {"value_id_user_selected": id_user_materials_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionMaterialsUsers()
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # Fichier data_gestion_material_user.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "materials_users_afficher_data"
            data_material_user_selected, data_materials_users_non_attribues, data_materials_users_attribues = \
                obj_actions_materials.materials_users_afficher_data(valeur_id_user_selected_dictionnaire)

            lst_data_user_selected = [item['id_user'] for item in data_material_user_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_user_selected  ", lst_data_user_selected,
                  type(lst_data_user_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_materials_users_non_attribues = [item['id_material'] for item in data_materials_users_non_attribues]
            session['session_lst_data_materials_users_non_attribues'] = lst_data_materials_users_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_materials_users_non_attribues  ", lst_data_materials_users_non_attribues,
                  type(lst_data_materials_users_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_materials_users_old_attribues = [item['id_material'] for item in data_materials_users_attribues]
            session['session_lst_data_materials_users_non_attribues'] = lst_data_materials_users_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_materials_users_old_attribues  ", lst_data_materials_users_old_attribues,
                  type(lst_data_materials_users_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_material_user_selected", data_material_user_selected, "type ", type(data_material_user_selected))
            print(" data data_materials_users_non_attribues ", data_materials_users_non_attribues, "type ",
                  type(data_materials_users_non_attribues))
            print(" data_materials_users_attribues ", data_materials_users_attribues, "type ",
                  type(data_materials_users_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "Material"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_material
            lst_data_materials_users_non_attribues = [item['Material'] for item in data_materials_users_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_materials gf_edit_material_user_selected ", lst_data_materials_users_non_attribues,
                  type(lst_data_materials_users_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_user_selected == [None]:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_genres_films" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichées dans GenresFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("material_user/material_user_modifier_tags_dropbox.html",
                           data_materials=data_materials_all,
                           data_user_selected=data_material_user_selected,
                           data_materials_attribues=data_materials_users_attribues,
                           data_materials_non_attribues=data_materials_users_non_attribues)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /gf_update_material_user_selected
# Récupère la liste de tous les genres du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_material_user_selected", methods=['GET', 'POST'])
def gf_update_material_user_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_user_selected = session['session_id_user_materials_edit']
            print("session['session_id_user_materials_edit'] ", session['session_id_user_materials_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_materials_users_non_attribues = session['session_lst_data_materials_users_non_attribues']
            print("old_lst_data_materials_users_non_attribues ", old_lst_data_materials_users_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_materials_users_attribues = session['session_lst_data_materials_users_non_attribues']
            print("old_lst_data_genres_films_old_attribues ", old_lst_data_materials_users_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "material_user_modifier_tags_dropbox.html"
            new_lst_str_materials_users = request.form.getlist('name_select_tags')
            print("new_lst_str_materials_users ", new_lst_str_materials_users)

            # OM 2020.04.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_str_int_materials_users_old = list(map(int, new_lst_str_materials_users))
            print("new_lst_materials_users ", new_lst_str_int_materials_users_old, "type new_lst_materials_users ",
                  type(new_lst_str_int_materials_users_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2020.04.29 Une liste de "id_material" qui doivent être effacés de la table intermédiaire "t_genres_films".
            lst_diff_materials_delete_b = list(
                set(old_lst_data_materials_users_attribues) - set(new_lst_str_int_materials_users_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_materials_delete_b ", lst_diff_materials_delete_b)

            # OM 2020.04.29 Une liste de "id_material" qui doivent être ajoutés à la BD
            lst_diff_materials_insert_a = list(
                set(new_lst_str_int_materials_users_old) - set(old_lst_data_materials_users_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_materials_insert_a ", lst_diff_materials_insert_a)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_materials = GestionMaterialsUsers()

            # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genres_films".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_material_ins in lst_diff_materials_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_material_ins" (l'id du genre dans la liste) associé à une variable.
                valeurs_user_sel_material_sel_dictionnaire = {"value_fk_user": id_user_selected,
                                                           "value_fk_material": id_material_ins}
                # Insérer une association entre un(des) genre(s) et le film sélectionner.
                obj_actions_materials.materials_users_add(valeurs_user_sel_material_sel_dictionnaire)

            # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_genres_films".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_material_del in lst_diff_materials_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_material_del" (l'id du genre dans la liste) associé à une variable.
                valeurs_user_sel_material_sel_dictionnaire = {"value_fk_user": id_user_selected,
                                                           "value_fk_material": id_material_del}
                # Effacer une association entre un(des) genre(s) et le film sélectionner.
                obj_actions_materials.materials_users_delete(valeurs_user_sel_material_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionMaterials()
            # Fichier data_gestion_genres.py
            # Afficher seulement le film dont les genres sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_materials_users_afficher_concat = obj_actions_materials.materials_users_afficher_data_concat(id_user_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data genres", data_materials_users_afficher_concat, "type ", type(data_materials_users_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_materials_users_afficher_concat == None:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_genres_films" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichées dans GenresFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_genres_films",
    # on affiche les films et le(urs) genre(s) associé(s).
    return render_template("material_user/material_user_afficher.html",
                           data=data_materials_users_afficher_concat)
