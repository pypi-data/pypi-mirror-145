import os
import icli
import readline
import argcomplete
import neotermcolor

from elbus.rpc import RpcException

from neotermcolor import colored

neotermcolor.readline_always_safe = True

from .sharedobj import common, current_command
from .tools import print_tb, err
from .compl import ComplOID, ComplSvc, ComplDbSvc, ComplNode, ComplYamlFile
from .compl import ComplOIDtp, ComplSvcRpcMethod, ComplSvcRpcParams, ComplEdit
from .client import call_rpc

DEFAULT_RPC_ERROR_MESSAGE = {
    -32700: 'parse error',
    -32600: 'invalid request',
    -32601: 'method not found',
    -32602: 'invalid method params',
    -32603: 'internal server error'
}


def dispatcher(_command,
               _subc=None,
               debug=False,
               json=False,
               timeout=5.0,
               **kwargs):
    current_command.debug = debug
    current_command.json = json
    current_command.timeout = timeout
    try:
        method = _command
        if _subc is not None:
            method += '_' + _subc.replace('.', '_')
        getattr(common.cli, method)(**kwargs)
        current_command.exit_code = 0
    except RpcException as e:
        current_command.exit_code = 3
        code = e.rpc_error_code
        msg = e.rpc_error_payload
        if not msg:
            msg = DEFAULT_RPC_ERROR_MESSAGE.get(code)
        elif isinstance(msg, bytes):
            msg = msg.decode()
        err(f'{msg} (code: {code})')
        if current_command.debug:
            print_tb(force=True)
    except Exception as e:
        current_command.exit_code = 1
        err(f'{e.__class__.__name__}: {e}')
        if current_command.debug:
            print_tb(force=True)
    current_command.debug = False


class Parser(icli.ArgumentParser):

    def get_interactive_prompt(self):
        try:
            name = call_rpc('test')['system_name']
            banner = colored(f'eva.4:{name}', color='yellow')
        except:
            banner = colored('eva.4', color='grey')
        if self.current_section:
            return f'[{banner}/{"".join(self.current_section)}]# '
        else:
            return f'[{banner}]# '

    def print_global_help(self):
        print('cls - clear screen')
        print('date - print system date/time')
        print('sh - enter system shell')
        print('top - processes')
        print('uptime - system uptime')
        print('w - who is logged in')
        print()


def append_registry_cli(root_sp):
    ap = root_sp.add_parser('registry', help='registry commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    p = sp.add_parser('manage', help='manage EVA ICS registry')
    p.add_argument('--offline', action='store_true', help='manage offline')


def append_server_cli(root_sp):
    ap = root_sp.add_parser('server', help='server commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    p = sp.add_parser('start', help='start the local node')
    p = sp.add_parser('stop', help='start the local node')
    p = sp.add_parser('reload', help='reload the local node')
    p = sp.add_parser('restart', help='restart the local node')
    p = sp.add_parser('launch',
                      help='launch the local node in the verbose mode')
    p = sp.add_parser('status', help='local node status')


def append_action_cli(root_sp):
    ap = root_sp.add_parser('action', help='action commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    p = sp.add_parser('exec', help='exec unit action')
    p.add_argument('i', metavar='OID',
                   help='unit OID').completer = ComplOIDtp('unit')
    p.add_argument('status', metavar='STATUS', type=int)
    p.add_argument('-v', '--value', metavar='VALUE')
    p.add_argument('-p', '--priority', metavar='PRIORITY', type=int)
    p.add_argument('-w',
                   '--wait',
                   metavar='SEC',
                   type=float,
                   help='wait max seconds until the action is completed')

    p = sp.add_parser('run', help='run lmacro')
    p.add_argument('i', metavar='OID',
                   help='lmacro OID').completer = ComplOIDtp('lmacro')
    p.add_argument('-a',
                   '--arg',
                   metavar='ARG',
                   action='append',
                   help='argument, can be multiple')
    p.add_argument('--kwarg',
                   metavar='KWARG',
                   action='append',
                   help='keyword argument name=value, can be multiple')
    p.add_argument('-p', '--priority', metavar='PRIORITY', type=int)
    p.add_argument('-w',
                   '--wait',
                   metavar='SEC',
                   type=float,
                   help='wait max seconds until the action is completed')

    p = sp.add_parser('toggle', help='exec unit toggle action')
    p.add_argument('i', metavar='OID',
                   help='unit OID').completer = ComplOIDtp('unit')
    p.add_argument('-p', '--priority', metavar='PRIORITY', type=int)
    p.add_argument('-w',
                   '--wait',
                   metavar='SEC',
                   type=float,
                   help='wait max seconds until the action is completed')

    p = sp.add_parser('result', help='get action result')
    p.add_argument('u', metavar='UUID', help='action UUID')

    p = sp.add_parser('terminate', help='terminate action (if possible)')
    p.add_argument('u', metavar='UUID', help='action UUID')

    p = sp.add_parser(
        'kill', help='cancel/terminate all actions for the item (if possible)')
    p.add_argument('i', metavar='OID',
                   help='unit OID').completer = ComplOIDtp('unit')

    p = sp.add_parser('list', help='list recent actions')
    p.add_argument('-i', '--oid', metavar='OID',
                   help='filter by OID').completer = ComplOID()
    p.add_argument(
        '-q',
        '--status-query',
        help='filter by status',
        choices=['waiting', 'running', 'completed', 'failed', 'finished'])
    p.add_argument('-s', '--svc', metavar='SVC',
                   help='filter by service').completer = ComplSvc()
    p.add_argument('-t',
                   '--time',
                   metavar='SEC',
                   type=int,
                   help='get actions for the last SEC seconds')
    p.add_argument('-n',
                   '--limit',
                   metavar='LIMIT',
                   type=int,
                   help='limit action list to')


def append_broker_cli(root_sp):
    ap = root_sp.add_parser('broker', help='ELBUS broker commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    sp.add_parser('client.list', help='list registered ELBUS clients')
    sp.add_parser('test', help='test broker')
    sp.add_parser('info', help='broker info')
    sp.add_parser('stats', help='broker stats')


def append_svc_cli(root_sp):
    ap = root_sp.add_parser('svc', help='service commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')
    sp.add_parser('list', help='list services')

    p = sp.add_parser('restart', help='restart service')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()

    p = sp.add_parser('edit', help='edit service config')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()

    p = sp.add_parser('test', help='test service')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()

    p = sp.add_parser('info', help='get service info')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()

    p = sp.add_parser('call', help='perform RPC call to the service')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()
    p.add_argument('-f',
                   '--file',
                   metavar='FILE',
                   help='read call params payload form the file'
                  ).completer = ComplYamlFile()
    p.add_argument('method', metavar='METHOD').completer = ComplSvcRpcMethod()
    p.add_argument('params',
                   nargs='*',
                   help='param=value',
                   metavar='PARAM=VALUE').completer = ComplSvcRpcParams()

    p = sp.add_parser('export', help='export service(s) to the deployment file')
    p.add_argument('i', metavar='MASK').completer = ComplSvc()
    p.add_argument('-o', '--output', metavar='FILE',
                   help='output file').completer = ComplYamlFile()

    p = sp.add_parser('deploy',
                      help='deploy service(s) from the deployment file')
    p.add_argument('-f', '--file', metavar='FILE',
                   help='deployment file').completer = ComplYamlFile()

    p = sp.add_parser('undeploy',
                      help='undeploy service(s) by the deployment file')
    p.add_argument('-f', '--file', metavar='FILE',
                   help='deployment file').completer = ComplYamlFile()

    p = sp.add_parser('create', help='create service from the template config')
    p.add_argument('i', metavar='SVC', help='service id').completer = ComplSvc()
    p.add_argument('f', metavar='FILE',
                   help='configuration template').completer = ComplYamlFile()

    p = sp.add_parser('destroy', help='destroy service')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()

    p = sp.add_parser(
        'purge', help='purge service (destroy and delete all service data)')
    p.add_argument('i', metavar='SVC').completer = ComplSvc()


def append_item_cli(root_sp):
    ap = root_sp.add_parser('item', help='item commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    p = sp.add_parser(
        'announce',
        help='forcibly announce current item states via the local bus')
    p.add_argument('i', metavar='MASK').completer = ComplOID('state')
    p.add_argument('-n', metavar='NODE').completer = ComplNode()

    p = sp.add_parser('list', help='list items')
    p.add_argument('i', metavar='MASK').completer = ComplOID()
    p.add_argument('-n', metavar='NODE').completer = ComplNode()

    p = sp.add_parser('state', help='item states')
    p.add_argument('i', metavar='MASK').completer = ComplOID('state')
    p.add_argument('-y', '--full', action='store_true')

    p = sp.add_parser('history', help='item state history')
    p.add_argument('i', metavar='OID').completer = ComplOID('state')
    p.add_argument('-a',
                   '--db-svc',
                   help='database service',
                   metavar='SVC',
                   required=True).completer = ComplDbSvc()
    p.add_argument('-s', '--time-start', metavar='TIME', help='start time')
    p.add_argument('-e', '--time-end', metavar='TIME', help='end time')
    p.add_argument('-z',
                   '--time-zone',
                   metavar='ZONE',
                   help='time zone (pytz, e.g. UTC or Europe/Prague)')
    p.add_argument('-n',
                   '--limit',
                   metavar='LIMIT',
                   type=int,
                   help='limit records to')
    p.add_argument('-x',
                   '--prop',
                   metavar='PROP',
                   choices=['status', 'value'],
                   help='item state prop (status/value)')
    p.add_argument(
        '-w',
        '--fill',
        metavar='INTERVAL',
        help='fill (e.g. 1T - 1 min, 2H - 2 hours), requires start time,'
        ' value precision can be specified as e.g. 1T:2 '
        'for 2 digits after comma')

    p = sp.add_parser('slog', help='item state log')
    p.add_argument('i', metavar='OID').completer = ComplOID()
    p.add_argument('-a',
                   '--db-svc',
                   help='database service',
                   metavar='SVC',
                   required=True).completer = ComplDbSvc()
    p.add_argument('-s', '--time-start', metavar='TIME', help='start time')
    p.add_argument('-e', '--time-end', metavar='TIME', help='end time')
    p.add_argument('-z',
                   '--time-zone',
                   metavar='ZONE',
                   help='time zone (pytz, e.g. UTC or Europe/Prague)')
    p.add_argument('-n',
                   '--limit',
                   metavar='LIMIT',
                   type=int,
                   help='limit records to')

    p = sp.add_parser('create', help='create an item')
    p.add_argument('i', metavar='OID').completer = ComplOID()

    p = sp.add_parser('destroy', help='destroy item(s)')
    p.add_argument('i', metavar='MASK').completer = ComplOID()

    p = sp.add_parser('enable', help='enable item(s)')
    p.add_argument('i', metavar='MASK').completer = ComplOID()

    p = sp.add_parser('disable', help='disable item(s)')
    p.add_argument('i', metavar='MASK').completer = ComplOID()

    p = sp.add_parser('edit', help='edit item config')
    p.add_argument('i', metavar='OID').completer = ComplOID()

    p = sp.add_parser('set', help='forcibly set item state')
    p.add_argument('i', metavar='OID').completer = ComplOID()
    p.add_argument('status', metavar='STATUS', type=int)
    p.add_argument('-v', '--value', metavar='VALUE')

    sp.add_parser('summary', help='item summary per source')

    p = sp.add_parser('export', help='export item(s) to the deployment file')
    p.add_argument('i', metavar='MASK').completer = ComplOID()
    p.add_argument('-o', '--output', metavar='FILE',
                   help='output file').completer = ComplYamlFile()

    p = sp.add_parser('deploy', help='deploy item(s) from the deployment file')
    p.add_argument('-f', '--file', metavar='FILE',
                   help='deployment file').completer = ComplYamlFile()
    p.add_argument('--replace',
                   action='store_true',
                   help='replace existing items')

    p = sp.add_parser('undeploy',
                      help='undeploy item(s) by the deployment file')
    p.add_argument('-f', '--file', metavar='FILE',
                   help='deployment file').completer = ComplYamlFile()

    p = sp.add_parser('watch', help='Watch item state')
    p.add_argument('i', metavar='OID').completer = ComplOID()
    p.add_argument('-n',
                   '--interval',
                   help='Watch interval (default: 1s)',
                   metavar='SEC',
                   default=1,
                   type=float)
    p.add_argument('-r', '--rows', help='Rows to plot', metavar='NUM', type=int)
    p.add_argument('-x',
                   '--prop',
                   help='State prop to use (default: value)',
                   choices=['status', 'value'],
                   metavar='PROP',
                   default='value')
    p.add_argument('-p',
                   '--chart-type',
                   help='Chart type',
                   choices=['bar', 'line'],
                   default='bar')


def append_lvar_cli(root_sp):
    ap = root_sp.add_parser('lvar', help='lvar commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    p = sp.add_parser('set', help='set lvar state')
    p.add_argument('i', metavar='OID').completer = ComplOIDtp('lvar')
    p.add_argument('status', metavar='STATUS', nargs='?', type=int)
    p.add_argument('-v', '--value', metavar='VALUE')

    p = sp.add_parser('reset', help='reset lvar state')
    p.add_argument('i', metavar='OID').completer = ComplOIDtp('lvar')

    p = sp.add_parser('clear', help='clear lvar state')
    p.add_argument('i', metavar='OID').completer = ComplOIDtp('lvar')

    p = sp.add_parser('toggle', help='toggle lvar state')
    p.add_argument('i', metavar='OID').completer = ComplOIDtp('lvar')

    p = sp.add_parser('incr', help='increment lvar value')
    p.add_argument('i', metavar='OID').completer = ComplOIDtp('lvar')

    p = sp.add_parser('decr', help='decrement lvar value')
    p.add_argument('i', metavar='OID').completer = ComplOIDtp('lvar')


def append_log_cli(root_sp):
    ap = root_sp.add_parser('log', help='log commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    sp.add_parser('purge', help='purge memory log')

    p = sp.add_parser('get', help='get memory log records')
    p.add_argument('level',
                   help='Log level',
                   nargs='?',
                   choices=[
                       'trace', 't', 'debug', 'd', 'info', 'i', 'warn', 'w',
                       'error', 'e'
                   ])
    p.add_argument('-t',
                   '--time',
                   metavar='SEC',
                   type=int,
                   help='get records for the last SEC seconds')
    p.add_argument('-n',
                   '--limit',
                   metavar='LIMIT',
                   type=int,
                   help='limit records to')
    p.add_argument('-m', '--module', metavar='MOD', help='filter by module')
    p.add_argument('-x', '--regex', metavar='REGEX', help='filter by regex')
    p.add_argument('-y',
                   '--full',
                   action='store_true',
                   help='display full log records')
    # p.add_argument('-f',
    # '--follow',
    # action='store_true',
    # help='follow log until C-c')


def append_node_cli(root_sp):
    ap = root_sp.add_parser('node', help='node commands')
    sp = ap.add_subparsers(dest='_subc',
                           metavar='SUBCOMMAND',
                           help='sub command')

    p = sp.add_parser('list', help='list nodes')


def sys_cmd(cmd):
    if cmd == 'top':
        import distutils.spawn
        top_cmd = distutils.spawn.find_executable('htop')
        if not top_cmd:
            top_cmd = cmd
        os.system(top_cmd)
    elif cmd == 'cls':
        os.system('clear')
    elif cmd == 'sh':
        print('Executing system shell')
        sh_cmd = os.getenv('SHELL')
        if sh_cmd is None:
            import distutils.spawn
            sh_cmd = distutils.spawn.find_executable('bash')
            if not sh_cmd:
                sh_cmd = 'sh'
        os.system(sh_cmd)
    else:
        os.system(cmd)


def init_ap():
    ap = Parser()

    completer = argcomplete.CompletionFinder(
        ap, default_completer=argcomplete.completers.SuppressCompleter())
    readline.set_completer_delims('')
    readline.set_completer(completer.rl_complete)
    readline.parse_and_bind('tab: complete')

    ap.sections = {
        'action': [],
        'broker': [],
        'item': [],
        'lvar': [],
        'log': [],
        'svc': [],
        'server': [],
        'registry': [],
        'node': []
    }

    ap.add_argument('-D',
                    '--debug',
                    help='debug the bus call',
                    action='store_true')
    ap.add_argument('-J', '--json', help='JSON output', action='store_true')
    ap.add_argument('-T',
                    '--timeout',
                    help='RPC timeout',
                    type=float,
                    default=5.0)

    sp = ap.add_subparsers(dest='_command', metavar='COMMAND', help='command')

    append_action_cli(sp)
    append_broker_cli(sp)
    append_item_cli(sp)
    append_lvar_cli(sp)
    append_log_cli(sp)
    append_node_cli(sp)
    append_registry_cli(sp)
    append_server_cli(sp)

    sp.add_parser('save', help='save scheduled states (if instant-save is off)')
    append_svc_cli(sp)
    sp.add_parser('test', help='core test/info')

    p = sp.add_parser('edit', help='edit the configuration keys and xc files')
    p.add_argument(
        'fname',
        metavar='CONFIG',
        help='config key to edit',
    ).completer = ComplEdit()
    p.add_argument(
        '--offline',
        action='store_true',
        help=
        'for keys: connect directly to the registry db when the node is offline'
    )

    try:
        import requests
        from . import REPOSITORY_URL
        p = sp.add_parser('update', help='update the node')
        p.add_argument('-u',
                       '--repository-url',
                       metavar='URL',
                       help='repository url',
                       default=REPOSITORY_URL)
        p.add_argument('--YES',
                       dest='yes',
                       action='store_true',
                       help='update without a confirmation')
        p.add_argument(
            '-i',
            '--info-only',
            action='store_true',
            help='do not perform the actual update, get the info only')
        p.add_argument('--test',
                       action='store_true',
                       help='install a build marked as test')
    except ModuleNotFoundError:
        pass

    sp.add_parser('version', help='core version')

    for c in ('cls', 'date', 'sh', 'top', 'uptime', 'w'):
        ap.interactive_global_commands[c] = sys_cmd

    ap.interactive_history_file = '~/.eva4_history'
    readline.set_history_length(300)

    ap.run = dispatcher

    return ap
