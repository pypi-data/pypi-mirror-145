# This is your Project Root
import pkg_resources

CONFIG_PATH = pkg_resources.resource_filename('atlas_client', 'config/config.ini')

TEMPLATE_FOLDER_PATH = pkg_resources.resource_filename('atlas_client',
                                                       'entity_source_generation/template')