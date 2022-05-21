"""
Analyse data generated by generate.py.
We need to know all possible modifiers and also, keys for things like abiliities.
"""

import json


class WoWsAnalyse:
    """
    Helper functions
    """

    def _read_json(self, filename: str) -> dict:
        with open(filename, 'r', encoding='utf8') as f:
            json_dict = json.load(f)
        return json_dict

    def _convert_to_dart_type(self, python_type: str) -> str:
        dart_type = python_type
        if dart_type == 'float':
            dart_type = 'double'
        elif dart_type == 'str':
            dart_type = 'String'
        elif dart_type == 'list':
            dart_type = 'List<String>'
        elif dart_type == 'dict':
            dart_type = 'Map<String, double>'
        return dart_type

    def _lower_two_letter(self, string: str) -> str:
        return string[:2].lower() + string[2:]

    def ability_info(self):
        json_dict = self._read_json('abilities.json')
        abilities_keys = {}
        abilities_filters: list[str] = []
        for key in json_dict:
            abilities = json_dict[key]
            filter_name = abilities['filter']
            abilities_filters.append(filter_name)
            for ability_key in abilities['abilities']:
                current_ability = abilities['abilities'][ability_key]
                for variable in current_ability:
                    abilities_keys[variable] = type(
                        current_ability[variable],
                    ).__name__

        abilities_fields = ''
        abilities_fromJson = ''
        abilities_init = ''
        for key in abilities_keys:
            dart_type = self._convert_to_dart_type(abilities_keys[key])
            abilities_fields += 'final {}? {};\n'.format(dart_type, key)
            abilities_init += 'this.{},\n'.format(key)
            abilities_fromJson += "{}: json['{}'],\n".format(key, key)

        # print(abilities_init)
        # print(abilities_fields)
        # print(abilities_fromJson)
        print(list(set(abilities_filters)))

    def exterior_info(self):
        json_dict = self._read_json('exteriors.json')
        exterior_keys = {}
        exterior_types: list[str] = []
        for key in json_dict:
            modifiers = json_dict[key]
            exterior_types.append(modifiers['type'])
            if not 'modifiers' in modifiers:
                continue

            modifiers = modifiers['modifiers']
            for variable in modifiers:
                exterior_keys[variable] = type(
                    modifiers[variable],
                ).__name__

        exterior_fields = ''
        exterior_fromJson = ''
        exterior_init = ''
        for key in exterior_keys:
            dart_type = self._convert_to_dart_type(exterior_keys[key])
            formatted = self._lower_two_letter(key)
            exterior_fields += 'final {}? {};\n'.format(dart_type, formatted)
            exterior_init += 'this.{},\n'.format(formatted)
            exterior_fromJson += "{}: json['{}'],\n".format(formatted, key)

        # print(exterior_init)
        # print(exterior_fields)
        print(exterior_fromJson)
        # print(list(set(exterior_types)))

    def modernization_info(self):
        json_dict = self._read_json('modernizations.json')
        modernization_keys = {}
        for key in json_dict:
            modernization = json_dict[key]
            if not 'modifiers' in modernization:
                continue

            modifiers = modernization['modifiers']
            for variable in modifiers:
                modernization_keys[variable] = type(
                    modifiers[variable],
                ).__name__

        modernization_fields = ''
        modernization_fromJson = ''
        modernization_init = ''
        for key in modernization_keys:
            dart_type = self._convert_to_dart_type(modernization_keys[key])
            formatted = self._lower_two_letter(key)
            modernization_fields += 'final {}? {};\n'.format(
                dart_type, formatted)
            modernization_init += 'this.{},\n'.format(formatted)
            modernization_fromJson += "{}: json['{}'],\n".format(
                formatted, key)

        print(modernization_init)
        print(modernization_fields)
        print(modernization_fromJson)

    def projectile_info(self):
        json_dict = self._read_json('projectiles.json')
        projectile_keys = {}
        projectile_types: list[str] = []
        for key in json_dict:
            projectile = json_dict[key]
            projectile_types.append(projectile['type'])
            for variable in projectile:
                projectile_keys[variable] = type(
                    projectile[variable],
                ).__name__

        projectile_fields = ''
        projectile_fromJson = ''
        projectile_init = ''
        for key in projectile_keys:
            dart_type = self._convert_to_dart_type(projectile_keys[key])
            formatted = self._lower_two_letter(key)
            projectile_fields += 'final {}? {};\n'.format(dart_type, formatted)
            projectile_init += 'this.{},\n'.format(formatted)
            projectile_fromJson += "{}: json['{}'],\n".format(formatted, key)

        # print(projectile_init)
        # print(projectile_fields)
        # print(projectile_fromJson)
        print(list(set(projectile_types)))
        print(len(projectile_keys))

    def ship_info(self):
        json_dict = self._read_json('ships.json')
        ship_groups = {}
        module_types = {}
        for key in json_dict:
            ship = json_dict[key]
            ship_groups[ship['group']] = True
            for module in ship['modules']:
                module_types[module] = True

        # ship_fields = ''
        # ship_fromJson = ''
        # ship_init = ''
        # for key in ship_keys:
        #     dart_type = self._convert_to_dart_type(ship_keys[key])
        #     formatted = self._lower_two_letter(key)
        #     ship_fields += 'final {}? {};\n'.format(dart_type, formatted)
        #     ship_init += 'this.{},\n'.format(formatted)
        #     ship_fromJson += "{}: json['{}'],\n".format(formatted, key)

        # print(list(ship_groups.keys()))
        print(list(module_types.keys()))


if __name__ == "__main__":
    analyse = WoWsAnalyse()
    # analyse.ability_info()
    # analyse.exterior_info()
    # analyse.modernization_info()
    # analyse.projectile_info()
    analyse.ship_info()
