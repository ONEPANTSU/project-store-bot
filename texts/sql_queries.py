insert_project_query = """
        INSERT INTO 
        `project` (`seller_id`, `name`, `price`, `status_id`, `subscribers`, 
        `income`, `comment`, `vip_ending`, `link`, `is_verified`) 
        VALUES (%s);
        """
insert_status_query = """
        INSERT INTO
        `status` (`status_name`)
        VALUES
        (%s);
        """
insert_theme_query = """
        INSERT INTO
        `theme` (`theme_name`)
        VALUES
        (%s);
        """
insert_project_theme_query = """
        INSERT INTO
        `project_theme` (`project_id`, `theme_id`)
        VALUES
        (%s);
        """
insert_seller_query = """
        INSERT INTO
        `seller` (`telegram_name`)
        VALUES
        (%s);
        """

select_vip_projects_id_query = (
    "SELECT id FROM `project` "
    "WHERE `status_id` = 1;"
)
select_all_projects_id_query = (
    "SELECT id FROM `project` "
    "ORDER BY `status_id` DESC, `vip_ending` DESC, `is_verified` DESC;"
)
select_projects_id_by_prices_query = (
    "SELECT id FROM `project` WHERE price >= '%s' AND price <= '%s'  "
    "ORDER BY `status_id` DESC, `vip_ending` DESC, `is_verified` DESC;"
)
select_project_by_id_query = (
    "SELECT * FROM `project` WHERE `id` = '%s' "
    "ORDER BY `status_id` DESC, `vip_ending` DESC, `is_verified` DESC;"
)
select_seller_name_by_seller_id_query = (
    "SELECT `telegram_name` FROM `seller` WHERE `id` = '%s';"
)
select_seller_id_by_project_id_query = (
    "SELECT `seller_id` FROM `project` WHERE `id` = '%s';"
)
select_seller_id_by_seller_name_query = (
    "SELECT `id` FROM `seller` WHERE `telegram_name` = '%s';"
)
select_project_by_seller_id_query = (
    "SELECT * FROM `project` WHERE `seller_id` = '%s' "
    "ORDER BY `status_id` DESC, `vip_ending` DESC, `is_verified` DESC;"
)
select_project_by_seller_name_query = (
    "SELECT project.id FROM `project` "
    "INNER JOIN `seller` ON project.seller_id = seller.id  "
    "WHERE `telegram_name` = '%s' "
    "ORDER BY project.`status_id` DESC, `vip_ending` DESC, `is_verified` DESC;"
)
select_projects_id_by_theme_id_query = (
    "SELECT `project_id` FROM `project_theme` "
    "WHERE `theme_id` = '%s';"
)
select_all_project_info_by_id_query = (
    "SELECT project.id, project.seller_id, project.name, project.price, "
    "project.status_id, project.subscribers, project.income, project.comment, "
    "seller.telegram_name, status.status_name, theme.id "
    "AS theme_id, theme.theme_name, project.vip_ending, project.link, project.is_verified "
    "FROM `project` "
    "INNER JOIN `seller` ON project.seller_id = seller.id "
    "INNER JOIN `project_theme` ON project.id = project_theme.project_id "
    "INNER JOIN `theme` ON project_theme.theme_id = theme.id "
    "INNER JOIN `status` ON project.status_id = status.id "
    "WHERE project.id = '%s' ORDER BY `status_id` DESC, `vip_ending` DESC, `is_verified` DESC;"
)
select_theme_name_by_theme_id_query = (
    "SELECT `theme_name` FROM `theme` WHERE `id` = '%s';"
)
select_theme_id_by_theme_name_query = (
    "SELECT `id` FROM `theme` WHERE `theme_name` = '%s';"
)
select_themes_id_by_project_id_query = (
    "SELECT `theme_id` FROM `project_theme` WHERE `project_id` = '%s';"
)
select_all_themes_query = "SELECT * FROM `theme`;"
select_filled_themes_query = (
    "SELECT theme.id, theme.theme_name FROM `project_theme` "
    "INNER JOIN `theme` ON theme.id = project_theme.theme_id "
    "GROUP BY theme.theme_name;"
)
select_status_name_by_status_id_query = (
    "SELECT `status_name` FROM `status` WHERE `id` = '%s';"
)
select_all_settings_info_query = "SELECT * FROM `settings`;"

update_project_query = """
        UPDATE
        `project`
        SET `seller_id` = '%s', `name` = '%s', `price` = '%s', `status_id` = '%s', `subscribers` = '%s', 
        `income` = '%s', `comment` = '%s', `vip_ending` = '%s', `link` = '%s', `is_verified` = '%s'
        WHERE `id` = '%s';
        """
update_seller_query = """
        UPDATE
        `seller` ()
        SET `telegram_name` = '%s'
        WHERE `id` = '%s';
        """

delete_project_query = "DELETE FROM `project` WHERE `id` = '%s';"
delete_seller_query = "DELETE FROM `seller` WHERE `id` = '%s';"
delete_project_theme_query = "DELETE FROM `project_theme` WHERE `project_id` = '%s';"

QUERIES = {
    "insert_project": insert_project_query,
    "insert_status": insert_status_query,
    "insert_theme": insert_theme_query,
    "insert_project_theme": insert_project_theme_query,
    "insert_seller": insert_seller_query,
    "select_vip_projects_id": select_vip_projects_id_query,
    "select_all_projects_id": select_all_projects_id_query,
    "select_projects_id_by_prices": select_projects_id_by_prices_query,
    "select_project_by_id": select_project_by_id_query,
    "select_seller_name_by_seller_id": select_seller_name_by_seller_id_query,
    "select_seller_id_by_project_id": select_seller_id_by_project_id_query,
    "select_seller_id_by_seller_name": select_seller_id_by_seller_name_query,
    "select_project_by_seller_id": select_project_by_seller_id_query,
    "select_project_by_seller_name": select_project_by_seller_name_query,
    "select_projects_id_by_theme_id": select_projects_id_by_theme_id_query,
    "select_all_project_info_by_id": select_all_project_info_by_id_query,
    "select_theme_name_by_theme_id": select_theme_name_by_theme_id_query,
    "select_theme_id_by_theme_name": select_theme_id_by_theme_name_query,
    "select_themes_id_by_project_id": select_themes_id_by_project_id_query,
    "select_all_themes": select_all_themes_query,
    "select_filled_themes": select_filled_themes_query,
    "select_status_name_by_status_id": select_status_name_by_status_id_query,
    "select_all_settings_info": select_all_settings_info_query,
    "update_project": update_project_query,
    "update_seller": update_seller_query,
    "delete_project": delete_project_query,
    "delete_seller": delete_seller_query,
    "delete_project_theme": delete_project_theme_query,
}
