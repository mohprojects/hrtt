INSERT INTO `app_users` (`user_id`, `user_type`, `user_username`, `user_auth_key`, `user_password_hash`, `user_password_reset_token`, `user_name`, `user_gender`, `user_contact_phone_number`, `user_contact_email_id`, `user_profile_photo_file_path`, `user_role`, `organization_id`,`user_created_at`, `user_created_by`, `user_updated_at`, `user_updated_by`, `user_status`) VALUES ('1', 'super-admin', 'support@qtglobal.rw', 'xc48ITBOTVBu87185KUSK2TlKxKiLJiw', 'pbkdf2_sha256$120000$AFnd3A0K4BUG$/UrvoujZon1lirkkLZfsM9beN0PgC4X/zCJBWS2orJo=', 'dmcWxmsxcF3mhEM7l7uzhifNRczvstrK', 'QT Support', '', '', 'support@qtglobal.rw', '', '-','0','0','1589300636', '1', '1589300636', '1', '0');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('user-create', 'user-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('user-update', 'user-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('user-view', 'user-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('user-delete', 'user-delete', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('dashboard-view', 'dashboard-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('settings-view', 'settings-view', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('log-create', 'log-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('log-update', 'log-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('log-view', 'log-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('log-delete', 'log-delete', '1589300636', '1589300636');



INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('1', '1589300636', '1', 'user-create', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('2', '1589300636', '1', 'user-update', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('3', '1589300636', '1', 'user-view', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('4', '1589300636', '1', 'user-delete', '1');

INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('5', '1589300636', '1', 'dashboard-view', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('6', '1589300636', '1', 'settings-view', '1');

INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('7', '1589300636', '1', 'log-create', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('8', '1589300636', '1', 'log-update', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('9', '1589300636', '1', 'log-view', '1');
INSERT INTO `app_user_access_permissions` (`user_access_permission_id`, `user_access_permission_updated_at`, `user_access_permission_updated_by`, `access_permissions_access_permission_name_id`, `users_user_id_id`) VALUES ('10', '1589300636', '1', 'log-delete', '1');

-- other permissions
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('organizations-create', 'organizations-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('organizations-update', 'organizations-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('organizations-view', 'organizations-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('organizations-delete', 'organizations-delete', '1589300636', '1589300636');

-- INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('divisions-create', 'divisions-create', '1589300636', '1589300636');
-- INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('divisions-update', 'divisions-update', '1589300636', '1589300636');
-- INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('divisions-view', 'divisions-view', '1589300636', '1589300636');
-- INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('divisions-delete', 'divisions-delete', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('projects-create', 'projects-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('projects-update', 'projects-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('projects-view', 'projects-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('projects-delete', 'projects-delete', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('projects-assign', 'projects-assign', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-create', 'activities-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-update', 'activities-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-view', 'activities-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-delete', 'activities-delete', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-submit', 'activities-submit', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-accept', 'activities-accept', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-reject', 'activities-reject', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-approve', 'activities-approve', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('activities-deny', 'activities-deny', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-create', 'capital-formation-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-update', 'capital-formation-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-view', 'capital-formation-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-delete', 'capital-formation-delete', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-submit', 'capital-formation-submit', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-accept', 'capital-formation-accept', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-reject', 'capital-formation-reject', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-approve', 'capital-formation-approve', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('capital-formation-deny', 'capital-formation-deny', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('levels-create', 'levels-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('levels-update', 'levels-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('levels-view', 'levels-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('levels-delete', 'levels-delete', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('comments-create', 'comments-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('comments-update', 'comments-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('comments-view', 'comments-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('comments-delete', 'comments-delete', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('currency-rate-create', 'currency-rate-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('currency-rate-update', 'currency-rate-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('currency-rate-view', 'currency-rate-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('currency-rate-delete', 'currency-rate-delete', '1589300636', '1589300636');

INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('system-reports-create', 'system-reports-create', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('system-reports-update', 'system-reports-update', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('system-reports-view', 'system-reports-view', '1589300636', '1589300636');
INSERT INTO `app_access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES ('system-reports-delete', 'system-reports-delete', '1589300636', '1589300636');