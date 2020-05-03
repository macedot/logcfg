from convertion import Conversion
from xml.dom import minidom
import argparse

def infixToPosfix(src : str) -> str:
    obj = Conversion(len(src))
    return obj.infixToPostfix(src)

def getParamsLogger(xmlFile : str, protocol : str) -> dict:
    logger = minidom.parse(xmlFile)
    for item in logger.getElementsByTagName('protocol'):
        if protocol == item.getAttribute('id'):
            items = item.getElementsByTagName('parameter')
            dictParams = {elem.getAttribute('id'): elem
                          for elem in items}
            return dictParams
    raise Exception("Invalid XML file: No protocol {}".format(protocol))


def readProfile(xmlFile : str) -> list:
    xmlProfile = minidom.parse(xmlFile)
    profile = xmlProfile.getElementsByTagName('profile')[0]
    protocol = profile.getAttribute('protocol')
    params = profile.getElementsByTagName('parameter')
    selected = [elem for elem in params
                if elem.getAttribute('dash') == "selected"]
    dictSelected = {elem.getAttribute('id'): elem.getAttribute('units')
                    for elem in selected}
    return [protocol, dictSelected]


def getParam(paramsLogger, id : str, unit : str) -> dict:
    for key, elem in paramsLogger.items():
        if key == id:
            return paramsToDict(elem, unit)
    return None

def getConversion(nodeParam, unit : str) -> str:
    for item in nodeParam.getElementsByTagName('conversion'):
        if unit == item.getAttribute('units'):
            expr =  item.getAttribute('expr')
            return infixToPosfix(expr)
    return None


def paramsToDict(nodeParam, unit : str):
    dictRet = dict()
    dictRet['id'] = nodeParam.getAttribute('id')
    dictRet['name'] = nodeParam.getAttribute('name')
    dictRet['paramname'] = (dictRet['name'] + "_({})".format(unit)).replace(' ', '_')

    addr = nodeParam.getElementsByTagName('address')
    if addr and addr[0]:
        dictRet['paramid'] = addr[0].firstChild.nodeValue
    else:
        dictRet['paramid'] = None

    dictRet['depends'] = list()
    depends = nodeParam.getElementsByTagName('ref')
    for ref in depends:
        dictRet['depends'].append(ref.getAttribute('parameter'))

    dictRet['unit'] = unit
    dictRet['scalingrpn'] = getConversion(nodeParam, unit)
    return dictRet


class LOGCFG:

    def __init__(self, rr_log_xml, logger_xml):
        self.protocol, self.paramsProfile = readProfile(rr_log_xml)
        self.paramsLogger = getParamsLogger(logger_xml, self.protocol)
        self.paramSelected = {key: elem
                              for key, elem in self.paramsLogger.items()
                              if key in self.paramsProfile.keys()}
        self.dictParams = {key: paramsToDict(elem, self.paramsProfile[key])
                           for key, elem in self.paramsLogger.items()
                           if key in self.paramsProfile.keys()}

    def toPostfix(self, infix_src):
        return infix_src

    def print(self, typeFile = 'ssmk'):
        print('type = {}'.format(typeFile))

        idx = 1
        for key, elem in self.dictParams.items():
            skip = ''
            if ':' in elem['scalingrpn']:
                skip = ';'
            print('')
            print(";{:03d}: {} - {} ({})".format(idx, elem['id'], elem['name'], elem['unit']))
            for key in ['paramname', 'paramid', 'scalingrpn']:
                if elem.get(key):
                    print("{}{} = {}".format(skip, key, elem[key]))
            idx += 1

        paramRPM = self.dictParams['P8']['paramname']
        print('')
        print('; Start log when RPM > 0')
        print("conditionrpn = {},0,>".format(paramRPM))
        print('action = start')

        print('')
        print('; Stop log when RPM = 0')
        print("conditionrpn = {},0,==".format(paramRPM))
        print('action = stop')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--profile', type=str, help='RomRaider XML Profile', required=True)
    requiredNamed.add_argument('--logger', type=str, help='Logger XML file', required=True)
    args = parser.parse_args()
    logcfg = LOGCFG(args.profile, args.logger)
    logcfg.print()
