from configparser import ConfigParser
from distutils.version import StrictVersion


class Plugin(object):

    def __init__(self, plugin_name, plugin_path):
        self.__details = ConfigParser()
        self.__name = plugin_name
        self.__path = plugin_path
        self.__fill_empty_fields()

        # variables for stuff created during the plugin lifetime
        self.plugin_object = None

    def __fill_empty_fields(self):
        if not self.details.has_option("Documentation", "Author"):
            self.author = "Unknown"
        if not self.details.has_option("Documentation", "Version"):
            self.version = "0.0"
        if not self.details.has_option("Documentation", "Website"):
            self.website = "None"
        if not self.details.has_option("Documentation", "Copyright"):
            self.copyright = "Unknown"
        if not self.details.has_option("Documentation", "Description"):
            self.description = ""

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, config_details):
        name = self.__name
        path = self.__path
        self.__details = config_details
        self.__name = name
        self.__path = path
        self.__fill_empty_fields()

    @property
    def name(self):
        return self.details.get("Core", "Name")

    @name.setter
    def name(self, name):
        if not self.details.has_section("Core"):
            self.details.add_section("Core")
        self.details.set("Core", "Name", name)

    @property
    def path(self):
        return self.details.get("Core", "Module")

    @path.setter
    def path(self, path):
        if not self.details.has_section("Core"):
            self.details.add_section("Core")
        self.details.set("Core", "Module", path)

    @property
    def version(self):
        return StrictVersion(self.details.get("Documentation", "Version"))

    @version.setter
    def version(self, ver):
        if isinstance(ver, StrictVersion):
            ver = str(ver)
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Version", ver)

    @property
    def author(self):
        return self.details.get("Documentation", "Author")

    @author.setter
    def author(self, author):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Author", author)

    @property
    def copyright(self):
        return self.details.get("Documentation", "Copyright")

    @copyright.setter
    def copyright(self, copyright):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Copyright", copyright)

    @property
    def website(self):
        return self.details.get("Documentation", "Website")

    @website.setter
    def website(self, website):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Website", website)

    @property
    def description(self):
        return self.details.get("Documentation", "Description")

    @description.setter
    def description(self, description):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Description", description)
