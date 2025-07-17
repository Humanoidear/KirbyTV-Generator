# Kirby TV File generator

## This small python script will generate the required XML files for the Kirby TV Channel to function in the different supported locales.


### How to add languages
Simply create a folder for the locale you want to generate.
You must create a {{locale}}.py file and a gb_config_{{locale}}.xml file (this last one will contain most of the translated strings)

Then in {{locale}}.py you will include the functions:
sing - Singularizer
deltaconv - Convert the time from seconds to a human readable string
get_ordinal_suffix - Returns ordinal suffices
format_date_with_ordinal - Returns a normal human date
get_dynamic_text - Returns the text that will be included in the channel's intro screen to notify of the episodes air date
get_xml_file_path - File path to the XML for the locale

You must modify these functions so they generate the appropriate results for your language so they don't look off