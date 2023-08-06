import sqlparse
import csv
import os
import zipfile
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
import itertools
import re

ns = {'xmi': "http://www.omg.org/XMI",
      'xsi':  "http://www.w3.org/2001/XMLSchema-instance",
      'datafoundation': "http://com.businessobjects.mds.datafoundation"}


def _is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def _extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if item.is_group:
            for x in _extract_from_part(item):
                yield x
        if from_seen:
            if _is_subselect(item):
                for x in _extract_from_part(item):
                    yield x
            elif item.ttype is Keyword and item.value.upper() in ['ORDER', 'GROUP', 'BY', 'HAVING', 'GROUP BY', 'ORDER BY']:
                from_seen = False
                StopIteration
            else:
                yield item
        if item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def _extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                value = identifier.value.replace('"', '').lower()
        elif isinstance(item, Identifier):
            value = item.value.replace('"', '').lower()
            yield value


def _clean_table_name(table_name):
    import re
    table_name = table_name.strip()
    if re.match(r'^[\w\.]+\s+(as\s+)?\w+$', table_name):
        table_name = table_name.split()[0]
    return table_name


def _extract_tables(sql):
    extracted_tables = []
    statements = list(sqlparse.parse(sql))
    for statement in statements:
        if statement.get_type() != 'UNKNOWN':
            stream = _extract_from_part(statement)
            extracted_tables.append(set(list(_extract_table_identifiers(stream))))
        else:
            print('Wrong sql!')
            exit(1)
    ret1 = list(itertools.chain(*extracted_tables))
    ret2 = [ ]
    for x in ret1:
        """
        sometimes sql is not parsed correctly (mainly subselects), so we need to 
        delete some obvious junk.
        """
        if '.' not in x:
            pass
        elif '(SELECT' in x.upper():
            pass
        elif ' AS ' in x.upper():
            ret2.append(x.split()[0])
        else:
            ret2.append(x.upper())
    ret3 = [_clean_table_name(tn) for tn in ret2]
    return list(set(ret3)) # make unique


def parse_dfx(dfx_path: str, results_dir: str):
    if not os.path.exists(dfx_path):
        return
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    csv_res_file = os.path.join(results_dir, os.path.basename(dfx_path).replace('.dfx', '.csv'))
    dfx = zipfile.ZipFile(dfx_path)
    xml = ''
    for filename in dfx.namelist():
        if filename.endswith('.dfx'):
            xml = filename
            break
    if not xml:
        return 
    mapping = ET.parse(dfx.open(xml))
    root = mapping.getroot()
    parse_results = []
    namespaces = dict([
        node for _, node in ElementTree.iterparse(
            dfx.open(xml), events=['start-ns'])
    ])
    for tag in root.findall('tables', namespaces):
        tables = []
        xsi_type = tag.get('{http://www.w3.org/2001/XMLSchema-instance}type')
        type = tag.get('type')
        owner = tag.get('owner')
        businessname = tag.get('businessName')
        qualifier = tag.get('qualifier')
        expression_raw = tag.get('expression')
        keywords = ''
        if expression_raw and xsi_type == 'datafoundation:DerivedTable':
            expression_clean = sqlparse.format(expression_raw, reindent=True, keyword_case='upper', strip_comments=True)
            keywrds = re.findall(r'.*(?P<keyword>@\w+)\((?P<value>[^)]*)\)',
                                 string=expression_clean,
                                 flags=re.MULTILINE | re.VERBOSE)
            for keyword in keywrds:
                keywords += str(keyword)
            tables = _extract_tables(expression_clean)
            if not tables:
                if 'FROM DUAL' in expression_clean.upper():
                    tables = ['DUAL']
                else:
                    """
                    Process the condition, where no tables was extracted by regular extracter.
                    This is usually happening, when there is a join without join (from a,b where a.a=b.b)

                    """
                    findings = re.findall(r'FROM(?P<TABLES>([A-z0-9\.,\s]+))WHERE',
                                          string=expression_clean,
                                          flags=re.MULTILINE | re.VERBOSE)
                    for tup in findings:
                        for elem in tup:
                            if '\n' in elem:
                                elems = elem.replace(',', '')
                                elems = elem.split('\n')
                            else:
                                elems = elem.split(',')
                            for table in elems:
                                table = table.strip()
                                table = table.replace(',', '')
                                if table:
                                    table = table.split()[0].upper()
                                    tables.append(table)
            tables = list(set(tables))
            with open(os.path.join(results_dir, businessname + '.sql'), 'w') as queryfile:
                queryfile.write(expression_clean)
        if tables:
            for table in tables:
                object_info = {'XSI_TYPE': xsi_type, 'TYPE': type, 'OWNER': owner, 'BUSINESSNAME': businessname,
                               'TABLES': table, 'QUALIFIER': qualifier, 'KEYWORDS': keywords}
                parse_results.append(object_info)
        else:
            object_info = {'XSI_TYPE': xsi_type, 'TYPE': type, 'OWNER': owner, 'BUSINESSNAME': businessname,
                           'TABLES': None, 'QUALIFIER': qualifier, 'KEYWORDS': keywords}
            parse_results.append(object_info)

    fieldnames = ['XSI_TYPE', 'TYPE', 'OWNER', 'BUSINESSNAME', 'TABLES', 'QUALIFIER', 'KEYWORDS']
    with open(csv_res_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=csv.excel)
        writer.writeheader()
        for row in parse_results:
            writer.writerow(row)
    print(f'Extracted to {csv_res_file}')
    return results_dir
