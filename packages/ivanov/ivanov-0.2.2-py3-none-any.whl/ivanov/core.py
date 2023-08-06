
import os.path
import os
import subprocess
import zipfile
import xml.etree.ElementTree as ET
import saspy
import logging
import tempfile
import hvac
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlparse
from .globals import all_obj_types
from sys import platform

if platform == "linux" or platform == "linux2":
    from .globals import java_linux as java
else:
    from .globals import java_windows as java

from .globals import hvac_url, hvac_token, hvac_secret_id, hvac_role_id, hvac_connections_path, hvac_connections_mountpoint


def create_saspyconn(sasobjsp_host, sasobjsp_port, java=java):
    saspy_conn = tempfile.NamedTemporaryFile(mode='w+', delete=False)  # needed to manually deleted after, to be compitable with win
    saspy_conn.write(f"""SAS_config_names=['sasconnection']
SAS_config_options = {{'lock_down': False,
                    'verbose'  : True,
                    'prompt'   : True
                    }}
SAS_output_options = {{'output' : 'html5'}} 
sasconnection = {{'java'      : '{java}',
            'iomhost'   : ['{sasobjsp_host}'],
            'iomport'   : {sasobjsp_port},
            'encoding': 'cyrillic',
            'options' : ["-fullstimer"]
            }}""")
    saspy_conn.seek(0)
    saspy_conn.close()
    return saspy_conn


class AbstractSAS(saspy.SASsession):
    def __init__(self, sasobjsp_user,
                       sasobjsp_pass,
                       sasobjsp_host,
                       sasobjsp_port,
                       java=java,
                       **kwargs):
        logging.debug('Initializing Abstract SAS class')
        self.sasobjsp_host = sasobjsp_host
        self.sasobjsp_port = sasobjsp_port
        self.sasobjsp_user = sasobjsp_user
        self.sasobjsp_pass = sasobjsp_pass
        self.java = java
        logging.debug('Generating saspy conn file')
        self.saspy_conn = create_saspyconn(sasobjsp_host=self.sasobjsp_host,
                                           sasobjsp_port=self.sasobjsp_port,
                                           java=self.java)
        logging.debug(f'Generated saspy conn file {self.saspy_conn.name}')
        super(AbstractSAS, self).__init__(cfgfile=self.saspy_conn.name,
                                           cfgname='sasconnection',
                                           omruser=self.sasobjsp_user,
                                           omrpw=self.sasobjsp_pass)
        print(f'Pid in sas server side({self.sasobjsp_host}) is  {self.SASpid}')

    def read_dataset(self, tablename: str, libname: str = 'WORK'):
        """
        Read data From SAS. Data is returned is in the form of Pandas DataFrame.
        :param libname: library, is which table is stored
        :param tablename: name of the table, you want to read
        :return: pd.Dataframe
        """
        df = self.sasdata2dataframe(table=tablename, libref=libname)
        return df

    def write_dataset(self, df, tablename: str, libname: str = 'WORK'):
        """
        Writes dataframe To SAS.
        :param df: dataframe to write
        :param tablename: table, in which you want to write data.
        :param libname: library, in which you want to write data.
        :return:
        """
        result = self.dataframe2sasdata(df=df, table=tablename, libref=libname)
        return result

    def show_libs(self):
        libs = self.assigned_librefs()
        return libs

    def run_script(self, script):
        if script:
            pass
        return self.submit(code=script)

    def endsas(self):
        os.unlink(self.saspy_conn.name)  # need to do it manually for win systems
        super(AbstractSAS, self).endsas()


def get_sas_connect(sasobjsp_host, sasobjsp_port, sasobjsp_user, sasobjsp_pass, java=java):
    """
    LEGACY!!!!!
    :param sasobjsp_host:
    :param sasobjsp_port:
    :param sasobjsp_user:
    :param sasobjsp_pass:
    :param java:
    :return:
    """
    saspy_conn = tempfile.NamedTemporaryFile(mode='w+', delete=True)
    saspy_conn.write(f"""SAS_config_names=['sasconnection']
SAS_config_options = {{'lock_down': False,
                    'verbose'  : True,
                    'prompt'   : True
                    }}
SAS_output_options = {{'output' : 'html5'}} 
sasconnection = {{'java'      : '{java}',
            'iomhost'   : ['{sasobjsp_host}'],
            'iomport'   : {sasobjsp_port},
            'encoding': 'cyrillic',
            'options' : ["-fullstimer"]
            }}""")
    saspy_conn.seek(0)
    try:
        sas = saspy.SASsession(cfgfile=saspy_conn.name, omruser=sasobjsp_user,
                               omrpw=sasobjsp_pass)
    except Exception as e:
        print(f'error!!! {str(e)}')
        return
    return sas


def get_objects_from_spk(spk_path: str, log_path: str, object_types: list = None):
    """
    Extracts information about metadata objects from spk
    :param spk_path: path (str) to spk
    :param log_path: path(str) to log file
    :param object_types: list of objects types (str), needed to be extracted.
    If not provided - defaults to ['DeployedFlow', 'DeployedJob',
    'ExternalFile', 'Folder', 'Library', 'Role', 'Server', 'StoredProcess',
    'Table', 'User']
    :return: dict with keys: 'Success' - indicating the success of operation and
    'Objects', containing dict with specified metadata object keys, containing
    list of path's --- FIX THAT DESCRIPTION!!!
    """
    logging.info(f"Object extraction from {spk_path} started.")
    log_lines = []
    validation_status = False
    if not object_types:
        object_types = all_obj_types
    extracted_objects = {i: [] for i in object_types}
    logging.debug(f"Objects to extract: {extracted_objects}")
    logging.debug(f"Opening file {spk_path}")
    try:
        spk = zipfile.ZipFile(spk_path)
        if 'DeployMap.xml' in spk.namelist():
            deploymap = ET.parse(spk.open('DeployMap.xml'))
            root = deploymap.getroot()
            for obj_type in extracted_objects.keys():
                for item in root.findall(f'Objects/{obj_type}'):
                    obj_path = item.get('Path').replace(f'({obj_type})', '')
                    extracted_objects[obj_type].append(obj_path)
                    logging.debug(f"Founded object {obj_type} in {obj_path}")
                    log_lines += f"Extracted object {obj_type}: {obj_path}\n"
            validation_status = True
            logging.info(f"List of objects extracted successfully.")
    except Exception as e:
        logging.error(f"Errors during extraction: {str(e)}")
        log_lines += str(e)
    finally:
        logging.debug(f"Writing log to {log_path}")
        with open(log_path, 'a') as logfile:
            logfile.writelines(log_lines)
        return {'Success': validation_status, 'Objects': extracted_objects}


def check_sas_code(sas_script_path, log_path):
    """
    Sas code checking. Implements various sas scripth checks
    (drop database includes, etc.)
    :param sas_script_path: path to sas log file (str)
    :param log_path: path to validation log file (str)
    :return: dict with key 'Success', indicating the results of validation.
    """
    logging.info(f"Checking of script {sas_script_path} stated.")
    validation_log_lines = []
    validation_status = False
    try:
        with open(sas_script_path, 'r') as script:
            validation_log_lines += 'Validated\n'
            validation_status = True
            logging.info(f"Script validated successfully.")
    except Exception as e:
        validation_log_lines += str(e)
        logging.critical(f"Script did not passed validation.")
    finally:
        logging.debug(f"Writing log to {log_path}")
        with open(log_path, 'a') as logfile:
            logfile.writelines(validation_log_lines)
        return {'Success': validation_status}


def import_spk(sas_conn_file_path, spk_path, log_path, import_package_jar_path,
               target='/',
               safe_mode=True):
    """
    Importing or checking import of spk to target platform
    :param sas_conn_file_path: path (str) to sas .swa connection profile of
    target platform
    :param spk_path: path(str) to spk
    :param log_path: path (str) to logfile
    :param target: metadata root path (str) to import data. Defaults to '/',
    rarely changes to something else.
    :param import_package_jar_path: path (str) to
    ImportPackage or ImportPackage.exe If not provided - platform and global vars
    are used to determine which path to use.
    :param safe_mode: (bool) - Flag, indicating if spk is being imported,
    or just checking (-noexecute flag)
    :return: dict with key 'Success', results of import or check, key 'Warnings',
    indicating if there were warnings during the process
    """
    logging.info(f"Import of {spk_path} started.")
    logging.debug(f"'Check mode' is set to {safe_mode}")
    execution_log_lines = []
    execution_status = False
    warnings = False
    command = ['-profile', sas_conn_file_path, '-package', spk_path, '-target',
               target, '-log', log_path, '-preservePaths', ]
    if platform == "linux" or platform == "linux2":
        command.append('-disableX11')
    command.insert(0, import_package_jar_path)
    if safe_mode:
        logging.debug(f"Launching in -noexecute mode.")
        command.append('-noexecute')
    try:
        logging.debug(f"'Command to be run: {command}")
        import_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if import_process.returncode == 0:
            execution_status = True
            logging.info(f"Import process finished successfully")
        if import_process.returncode == 4:
            execution_status = True
            logging.warning(f"Import process finished with Warnings")
            warnings = True
    except Exception as e:
        execution_log_lines += str(e)
        logging.error(f"Import process finished ERRORS! {str(e)}")
    finally:
        logging.info(f"Log will be written to {log_path}")
        with open(log_path, 'a') as logfile:
            logfile.writelines(execution_log_lines)
        return {'Success': execution_status, 'Warnings': warnings}


def check_import(sas_conn_file_path, spk_path, import_package_jar_path,
                 log_path,
                 target='/'):
    """
    Spk import check, calls import_spk with key "safe_mode=True".
    Writes logs to provided log file.
    :param sas_conn_file_path: path (str) to sas .swa connection profile of
    target platform
    :param spk_path: path(str) to spk
    :param log_path: path (str) to logfile
    :param target: metadata root path (str) to import data. Defaults to '/',
    rarely changes to something else.
    :param import_package_jar_path: path (str) to
    ImportPackage \ ImportPackage.exe If not provided - platform and global vars
    are used to determine which path to use.
    :return: dict with key 'Success', results of import \ check, key 'Warnings',
    indicating if there were warnings during the process
    """
    logging.info(f"Import check of {spk_path} started.")
    check_result = import_spk(sas_conn_file_path=sas_conn_file_path,
                              spk_path=spk_path,
                              log_path=log_path,
                              target=target,
                              import_package_jar_path=import_package_jar_path,
                              safe_mode=True)
    return check_result


def launch_sas_code(sas_script_path, sasobjsp_host, sasobjsp_port, sasobjsp_user, sasobjsp_pass,
                    log_path):
    """
    Opens sas session and launches code, also saves results to log.
    :param sas_script_path: path to file, that contains sas script (.sas)
    :param saspy_cfg_file_path: path to pycfg file, which contains saspy
    connection descriptor.
    :param user: user for sas app server
    :param password: password for sas app server
    (can be encrypted in sas form, like {001}WDBAYDVWDVW)
    :param log_path: path (str) to execution log file
    :return: dict with key 'Success', indicating the success of code execution
    """
    logging.info(f"Launching of script {sas_script_path} started.")
    saspy_conn = tempfile.NamedTemporaryFile(mode='w+', delete=True)
    saspy_conn.write(f"""SAS_config_names=['sasconnection']
SAS_config_options = {{'lock_down': False,
                    'verbose'  : True,
                    'prompt'   : True
                    }}
SAS_output_options = {{'output' : 'html5'}} 
sasconnection = {{'java'      : '/usr/bin/java',
            'iomhost'   : ['{sasobjsp_host}'],
            'iomport'   : {sasobjsp_port},
            'encoding': 'cyrillic',
            'options' : ["-fullstimer"]
            }}""")
    saspy_conn.seek(0)
    execution_log_lines = []
    execution_status = False
    try:
        with open(sas_script_path, 'r') as sas_script:
            command = sas_script.read()
            execution_log_lines += 'The following script obtained from file:\n'
            execution_log_lines += command
        sas = saspy.SASsession(cfgfile=saspy_conn.name, omruser=sasobjsp_user,
                               omrpw=sasobjsp_pass)
        code = sas.submit(command)
        sas.endsas()
        execution_log_lines += code['LOG']
        execution_status = True
    except Exception as e:
        logging.error(f"Error while executing script. {str(e)}")
        execution_log_lines += str(e)
    finally:
        logging.info(f"Log will be written to {log_path}")
        with open(log_path, 'a') as log:
            log.writelines(execution_log_lines)
        return {'Success': execution_status}


def redeploy_jobs(objects_list,
                  serverusername,
                  serverpassword,
                  execution_log_path,
                  sas_conn_file_path,
                  deploy_dir,
                  deployjob_jar_path,
                  deploytype='REDEPLOY',
                  metarepository='Foundation',
                  appservername='SASApp',
                  display='localhost:99'):
    """
    Launches redeploy or deploy process of given objects on given platform.
    Writes results to log.
    :param objects_list: (list) of path's (str) of metata objects, being
    deployed or redeployed
    :param serverusername: (str) username for app server
    :param serverpassword: (str) password for app server
    :param execution_log_path: path (str) to log file
    :param sas_conn_file_path: path (str) to sas .swa connection file
    :param deploytype: DEPLOY or REDEPLOY (str), indicates the type of action.
    :param deploy_dir: (str) - path where to deploy .sas code
    :param metarepository: (str) Name of repository, where deploy or redeploy is
    happening. Defaults to 'Foundation'.
    :param appservername: (str) name of App server, to perform action. Defaults
    to 'SASApp'.
    :param deployjob_jar_path: path (str) to DeployJobs \ DeployJobs.exe If not
    provided - platform and global vars
    are used to determine which path to use.
    :param display: (str) 'DISPLAY' env variable, that is needed to be provided
    to perform action on linux platform.
    Defaults to 'localhost:99' since we have xvfb launched as service.
    :return: dict with key 'Success', results of redeploy, key 'Warnings',
    indicating if there were warnings during the process
    """
    logging.info(f"Redeploy process started")
    execution_log_lines = []
    execution_status = False
    warnings = False
    env = os.environ.copy()
    env['DISPLAY'] = display
    command = ['-profile', sas_conn_file_path, '-deploytype', deploytype,
               '-objects', *objects_list, '-sourcedir',
               deploy_dir, '-metarepository', metarepository, '-appservername',
               appservername, '-serverusername', serverusername,
               '-serverpassword', serverpassword, '-log', execution_log_path]
    command.insert(0, deployjob_jar_path)
    logging.debug(f"Command to be executed: {command}")
    try:
        redeploy_process = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if redeploy_process.returncode == 0:
            logging.info(f"Redeploy process finished successfully.")
            execution_status = True
        elif redeploy_process.returncode == 4:
            execution_status = True
            warnings = True
            logging.warning(f"Redeploy process finished with warnings.")
            # execution_log_lines += redeploy_process.stdout
        else:
            # execution_log_lines += redeploy_process.stderr
            logging.error(f"Redeploy process finished with Errors! Check log!")
    except Exception as e:
        logging.error(f"Errors while performing redeploy {str(e)}")
        execution_log_lines += str(e)
    finally:
        logging.info(f"Log will be written to {execution_log_path}")
        with open(execution_log_path, 'a+') as log:
            log.writelines(execution_log_lines)
        return {'Success': execution_status, 'Warnings': warnings}


def export_objects(objects_list, log_path, sas_conn_file_path,
                   export_package_jar_path,
                   package_path):
    """
    Launches meta objects export process
    :param objects_list: list of metadata path strings
    :param log_path: path to lig file (it will be created by export process)
    :param sas_conn_file_path: path to .swa file with connection description
    :param export_package_jar_path: path to ExportPackage binary
    :param package_path: path to spk file, that will be created.
    :return: dict with key 'Success', results of export process, key 'Warnings',
    indicating if there were warnings during the process
    """
    execution_log_lines = []
    env = os.environ.copy()
    execution_status = False
    warnings = False
    logging.info(f"Starting metadata export process.")
    command = ['-profile', sas_conn_file_path, '-package', package_path,
               '-objects', *objects_list, '-log', log_path]
    if platform == "linux" or platform == "linux2":
        command.append('-disableX11')
    command.insert(0, export_package_jar_path)
    logging.debug(f"Command to be executed: {command}")
    try:
        export_process = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(80 * '*')
        if export_process.returncode == 0:
            logging.info(f"Objects succesfully exported to {package_path}.")
            execution_status = True
        elif export_process.returncode == 4:
            # print(f'Export process finished with warnings.')
            execution_status = True
            warnings = True
            logging.warning(f"Warnings during export process. Check log: {log_path}")
            # logging.info(f"Objects exported to {package_path}.")
            # execution_log_lines += redeploy_process.stdout
        else:
            logging.error(f"Errors during export process. Check log: {log_path}")
            # execution_log_lines += redeploy_process.stderr
            # print(f'Export process finished with ERRORS.')
    except Exception as e:
        execution_log_lines += str(e)
        logging.error(f"Export process finished with ERRORS: {str(e)}")
    finally:
        logging.info(f"Log will be written to: {log_path}")
        with open(log_path, 'a') as log:
            log.writelines(execution_log_lines)
        return {'Success': execution_status, 'Warnings': warnings}


def backup_metadata(backup_script_path, comment, sas_conn_file_path, log_path):
    """
    Launches metadata backup
    :param backup_script_path: path to sas-backup-metadata script
    :param comment: comment(str) to be written on backup
    :param sas_conn_file_path: path to .swa file with connection description
    :param log_path: path to lig file
    :return: dict with key 'Success', results of backup process,
    key 'Backup_name', containing the backup name
    """
    logging.info(f"Full metadata backup started")
    execution_log_lines = []
    env = os.environ.copy()
    backup_success = False
    backup_name = None
    warnings = False
    command = [backup_script_path, '-comment', comment,
               '-profile', sas_conn_file_path, '-log', log_path]
    logging.debug(f"Command to run: {command}")
    try:
        backup_process = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if backup_process.returncode == 0:
            backup_success = True
            backup_name = str(backup_process.stdout.readline()).split()[2]
            logging.info(f"Backup {backup_name} completed successfully.")
        elif backup_process.returncode == 4:
            backup_success = False
            backup_name = str(backup_process.stdout.readline()).split()[2]
            logging.warning(f"Backup {backup_name} completed with WARNINGS.")
            warnings = True
        else:
            # execution_log_lines += backup_process.stderr
            logging.warning(f"Backup NOT completed!")
    except Exception as e:
        execution_log_lines += str(e)
        logging.error(f"Errors during backup process! {str(e)}")
    finally:
        logging.info(f"Log will be written to {log_path}")
        with open(log_path, 'a+') as log:
            log.writelines(execution_log_lines)
        return {'Success': backup_success, 'Backup_name': backup_name}


def recover_metadata(recover_script_path, backup_name, comment,
                     sas_conn_file_path, log_path):
    """
    Launches metadata restore
    :param recover_script_path: path to sas-recover-metadata script
    :param backup_name: name of backup (actually, name of folder)
    :param comment: comment(str) to be written on restore
    :param sas_conn_file_path: path to .swa file with connection description
    :param log_path: path to lig file
    :return: dict with key 'Success', results of restore process,
    key 'Backup_name', containing the backup name
    """
    logging.info(f"Metadata recovery from backup {backup_name} started.")
    execution_log_lines = []
    env = os.environ.copy()
    restore_success = False
    warnings = False
    command = [recover_script_path, backup_name, '-comment', comment,
               '-profile', sas_conn_file_path, '-log', log_path]
    logging.info(f"Command to run: {command}")
    try:
        backup_process = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(80 * '*')
        if backup_process.returncode == 0:
            restore_success = True
            logging.info(f"Restore from backup {backup_name} finished successfully")
        elif backup_process.returncode == 4:
            restore_success = False
            warnings = True
            logging.warning(f"Restore from backup {backup_name} finished with warnings")
            # execution_log_lines += redeploy_process.stdout
        else:
            logging.warning(f"Restore from backup {backup_name} not finished!")
            # execution_log_lines += redeploy_process.stderr
    except Exception as e:
        execution_log_lines += str(e)
        logging.error(f"Restore from backup {backup_name} not finished. ERRORS: {str(e)}")
    finally:
        logging.info(f"Log file will be written to {log_path}")
        with open(log_path, 'a') as log:
            log.writelines(execution_log_lines)
        return {'Success': restore_success}


def get_hvac_client(hvac_url: str = hvac_url,
                    namespace: str = None,
                    token: str = hvac_token,
                    hvac_role_id: str = hvac_role_id,
                    hvac_secret_id: str = hvac_secret_id,
                    ldap_login: str = None,
                    ldap_password: str = None, **kwargs):
    if token:
        client = hvac.Client(url=hvac_url, token=token, namespace=namespace)
    elif hvac_role_id and hvac_secret_id:
        client = hvac.Client(url=hvac_url, namespace=namespace)
        client.auth.approle.login(hvac_role_id, hvac_secret_id, use_token=True)
    elif ldap_login and ldap_password:
        client = hvac.Client(url=hvac_url, namespace=namespace)
        client.auth.ldap.login(username=ldap_login, password=ldap_password)
    else:
        raise Exception
    return client


def _normalize_conn_type(conn_type):
    if conn_type == 'postgresql':
        conn_type = 'postgres'
    elif '-' in conn_type:
        conn_type = conn_type.replace('-', '_')
    return conn_type


def _parse_netloc_to_hostname(uri_parts):
    """Parse a URI string to get correct Hostname."""
    hostname = unquote(uri_parts.hostname or '')
    if '/' in hostname:
        hostname = uri_parts.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = unquote(hostname)
    return hostname


def _parse_from_uri(uri: str):
    uri_parts = urlparse(uri)
    conn_type = uri_parts.scheme
    conn_type = _normalize_conn_type(conn_type)
    host = _parse_netloc_to_hostname(uri_parts)
    quoted_schema = uri_parts.path[1:]
    schema = unquote(quoted_schema) if quoted_schema else quoted_schema
    login = unquote(uri_parts.username) if uri_parts.username else uri_parts.username
    password = unquote(uri_parts.password) if uri_parts.password else uri_parts.password
    port = uri_parts.port
    extra = ''
    if uri_parts.query:
        query = dict(parse_qsl(uri_parts.query, keep_blank_values=True))
        if '__extra__' in query:
            extra = query['__extra__']
        else:
            extra = query
    return {'conn_type': conn_type,
            'host': host,
            'schema': schema,
            'login': login,
            'password': password,
            'port': port,
            'extra': extra}


def get_secret_from_vault(vault_path: str, vault_mount_point: str, client: hvac.Client = None, **kwargs):
    if not client:
        client = get_hvac_client(**kwargs)
    creds = client.secrets.kv.v2.read_secret_version(path=vault_path, mount_point=vault_mount_point)
    creds = creds['data']['data']
    key = list(creds.keys())[0]  # EXTREMELY DANGER!
    value = list(creds.values())[0]  # EXTREMELY DANGER!
    return key, value


def get_connection_from_vault(connection_id: str,
                              connections_path: str = hvac_connections_path,
                              mount_point=hvac_connections_mountpoint,
                              client: hvac.Client = None, **kwargs):
    if not client:
        client = get_hvac_client(**kwargs)
    conn_path = f"{connections_path}/{connection_id}"
    response = client.secrets.kv.v2.read_secret_version(path=conn_path, mount_point=mount_point)
    conn_uri = response['data']['data']['conn_uri']
    return _parse_from_uri(conn_uri)
