

def check_is_on(json, id):
    """
    For a given json response from the light,
    check that it is on. For the zwave this isnt so
    easy - so we need to check if the bulb is using power
    :param json:
    :return:
    """
    for state in json[f'Device_Num_{id}']['states']:
        if state['service'] == 'urn:micasaverde-com:serviceId:EnergyMetering1' and state['variable'] == "Watts":
            if float(state['value']) > 0.0:
                return True
            return False
