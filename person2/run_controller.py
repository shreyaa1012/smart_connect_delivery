from os_ken.base import app_manager

app_manager.AppManager.run_apps(
    [
        'os_ken.controller.ofp_handler',
        'smart_content_controller_osken'
    ]
)
