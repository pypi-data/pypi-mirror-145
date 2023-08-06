import saspy

def SASLogin(id, pw, sys='viya') :    
    if sys == 'viya' :
        sas = saspy.SASsession(ip='147.47.206.193', user=str(id), pw=str(pw), verify=False, context='SAS Studio compute context', encoding='utf-8')
    if sys == 'oda' :
        sas = saspy.SASsession(java='/usr/bin/java', iomhost=['odaws01-apse1.oda.sas.com','odaws02-apse1.oda.sas.com'], iomport=8591, encoding='utf-8', omruser=str(id), omrpw=str(pw))
    return sas