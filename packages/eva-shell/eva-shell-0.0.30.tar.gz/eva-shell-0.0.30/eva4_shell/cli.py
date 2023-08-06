import elbus
import msgpack
import os
import sys
import time
from neotermcolor import colored
from functools import partial
from rapidtables import format_table, FORMAT_GENERATOR, FORMAT_GENERATOR_COLS

from .tools import print_result, ok, edit_config, read_file, err
from .tools import print_action_result, format_value, prepare_time
from .tools import get_node_svc_info, edit_file, get_term_size
from .client import call_rpc
from .sharedobj import common, current_command


def eva_control_c(c, pfx=''):
    cmd = f'{pfx}{common.dir_eva}/sbin/eva-control {c}'
    os.system(cmd)


class CLI:

    def test(self):
        data = call_rpc('test')
        print_result(data, need_header=False, name_value=True)

    def save(self):
        call_rpc('save')
        ok()

    def server_start(self):
        eva_control_c('start')
        time.sleep(1)

    def server_stop(self):
        eva_control_c('stop')
        time.sleep(1)

    def server_restart(self):
        eva_control_c('restart')
        time.sleep(1)

    def server_reload(self):
        until = time.time() + current_command.timeout
        call_rpc('core.shutdown')
        while True:
            time.sleep(1)
            try:
                call_rpc('test')
                break
            except:
                pass
            if time.time() > until:
                raise TimeoutError
        ok()

    def server_launch(self):
        eva_control_c('launch', 'VERBOSE=1 ')

    def server_status(self):
        eva_control_c('status')

    def update(self, repository_url, yes, info_only, test):
        import json
        from .tools import safe_download, set_file_lock
        from .tools import remove_file_lock, get_arch
        arch = get_arch()
        if arch.startswith('arm'):
            arch_sfx = 'armv7'
        elif arch == 'x86_64':
            arch_sfx = 'x86_64-musl'
        elif arch == 'aarch64':
            arch_sfx = 'aarch64-musl'
        else:
            raise RuntimeError(f'unsupported architecture: {arch}, '
                               'please update the system manually')
        try:
            set_file_lock('update')
        except RuntimeError:
            raise RuntimeError('update is already active')
        try:
            os.environ['EVA_REPOSITORY_URL'] = repository_url
            print('Using repository : ' +
                  colored(repository_url, color='green', attrs=['bold']))
            print()
            info = get_node_svc_info()
            build = info['build']
            version = info['version']
            if 'EVA_UPDATE_FORCE_VERSION' in os.environ:
                new_version, new_build = os.environ[
                    'EVA_UPDATE_FORCE_VERSION'].split(':')
                new_build = int(new_build)
                forced_version = True
            else:
                if test:
                    update_info = 'update_info_test.json'
                else:
                    update_info = 'update_info.json'
                result = json.loads(
                    safe_download(f'{repository_url}/{update_info}'))
                new_build = int(result['build'])
                new_version = result['version']
                forced_version = False
            if info_only:
                data = {
                    'build': build,
                    'new_build': new_build,
                    'new_version': new_version,
                    'update_available': build < new_build
                }
                print_result(data, need_header=False, name_value=True)
                return
            print(
                colored('Current build', color='blue', attrs=['bold']) + ' : ' +
                colored(f'{build} (v{version})', color='cyan'))
            print(
                colored(
                    f'{"Selected" if forced_version else "Latest available"}'
                    ' build',
                    color='blue',
                    attrs=['bold']) + ' : ' +
                colored('{} (v{})'.format(new_build, new_version),
                        color='yellow'))
            if build == new_build:
                return
            if build > new_build:
                raise RuntimeError(
                    'Your build is newer than then update server has')
            manifest = json.loads(
                safe_download(f'{repository_url}/{new_version}/nightly/'
                              f'manifest-{new_build}.json'))
            if not yes:
                if version != new_version:
                    try:
                        content = safe_download(
                            f'{repository_url}/{new_version}/nightly/UPDATE.rst'
                        )
                    except Exception as e:
                        err('Unable to download update info')
                        raise
                    print()
                    print(content.decode())
                try:
                    u = input('Type ' +
                              colored('YES', color='red', attrs=['bold']) +
                              ' (uppercase) to update, or press ' +
                              colored('ENTER', color='white') + ' to abort > ')
                except:
                    print()
                    u = ''
                if u != 'YES':
                    return
            update_script = f'update-{new_build}.sh'
            update_files = [
                update_script, f'eva-{new_version}-{new_build}-{arch_sfx}.tgz'
            ]
            print()
            print('Updating...')
            try:
                os.chdir(common.dir_eva)
                for f in update_files:
                    url = f'{repository_url}/{new_version}/nightly/{f}'
                    try:
                        data = manifest['content'][f]
                        sig = data['signature']
                    except KeyError:
                        raise RuntimeError(
                            f'Signature for {url} not found in manifest')
                    with open(f, 'wb') as fh:
                        fh.write(
                            safe_download(url,
                                          manifest=manifest,
                                          timeout=current_command.timeout * 20))
                    try:
                        if os.system(f'./sbin/rsatool verify "{f}" '
                                     f'"./share/eva.key" "{sig}" > /dev/null'):
                            raise RuntimeError(
                                'Signature verification error for {url}')
                    except:
                        os.unlink(f)
                        raise
                if os.system(f'bash {update_script}'):
                    err('FAILED TO APPLY UPDATE! '
                        'TRYING TO BRING THE NODE BACK ONLINE')
                    self.server_start()
                    raise RuntimeError(f'update failed')
                print('Update completed', end='')
            finally:
                for f in update_files:
                    try:
                        os.unlink(f)
                    except FileNotFoundError:
                        pass
            if common.interactive:
                print('. Now exit EVA shell and log in back')
            else:
                print()
            return
        finally:
            remove_file_lock('update')

    def registry_manage(self, offline=False):
        cmd = f'{common.dir_eva}/bin/eva-registry'
        if offline:
            cmd += ' --offline'
        os.system(cmd)

    def edit(self, fname, offline=False):
        if fname.startswith('config'):
            cmd = f'{common.dir_eva}/bin/eva-registry'
            if offline:
                cmd += ' --offline'
            cmd += f' edit eva/"{fname}"'
            if not os.system(cmd) and fname != 'config/python-venv':
                print('restart or reload the node server to apply changes')
        else:
            edit_file(fname)

    def log_purge(self):
        call_rpc('log.purge')
        ok()

    def log_get(self, level, time, limit, module, regex, full):

        def log_record_color(level):
            if level == 'TRACE':
                return dict(color='grey', attrs='dark')
            elif level == 'DEBUG':
                return dict(color='grey')
            elif level == 'WARN':
                return dict(color='yellow', attrs='bold')
            elif level == 'ERROR':
                return dict(color='red')
            return {}

        width, height = get_term_size()

        params = {
            'level': level,
            'time': time,
            'limit': limit if limit else height - 3,
            'module': module,
            'rx': regex
        }
        records = call_rpc('log.get', params)
        if current_command.json:
            print_result(records)
        elif records:
            data = []
            for r in records:
                data.append(
                    dict(time=r['dt'],
                         host=r['h'],
                         module=r['mod'],
                         level=r['lvl'].upper(),
                         message=r['msg']))
            header, rows = format_table(data, fmt=FORMAT_GENERATOR)
            if not full:
                header = header[:width]
            print(colored(header, color='blue'))
            print(colored('-' * len(header), color='grey'))
            for row, record in zip(rows, data):
                print(
                    colored(row if full else row[:width],
                            **log_record_color(record['level'])))

    def svc_list(self):
        data = call_rpc('svc.list')
        print_result(data, cols=['id', 'status', 'pid', 'launcher'])

    def svc_export(self, i, output=None):
        import yaml
        c = 0
        configs = []
        for svc in call_rpc('svc.list'):
            name = svc['id']
            if (i.startswith('*') and name.endswith(i[1:])) or \
                (i.endswith('*') and name.startswith(i[:-1])) or \
                (i.startswith('*') and i.endswith('*') and i[1:-1] in name) or \
                i == name:
                c += 1
                configs.append(
                    dict(id=name,
                         params=call_rpc('svc.get_params', dict(i=name))))
        dump = yaml.dump(configs, default_flow_style=False)
        if output is None:
            print(dump)
        else:
            with open(output, 'w') as fh:
                fh.write(dump)
            print(f'{c} service(s) exported')
            print()

    def svc_deploy(self, file=None, replace=False):
        import yaml
        svcs = yaml.safe_load(read_file(file).decode())
        call_rpc('svc.deploy', dict(svcs=svcs))
        print(f'{len(svcs)} service(s) deployed')
        print()

    def svc_undeploy(self, file=None):
        import yaml
        svcs = yaml.safe_load(read_file(file).decode())
        call_rpc('svc.undeploy', dict(svcs=svcs))
        print(f'{len(svcs)} service(s) undeployed')
        print()

    def svc_restart(self, i):
        call_rpc('svc.restart', dict(i=i))
        ok()

    def svc_destroy(self, i):
        call_rpc('svc.undeploy', dict(svcs=[i]))
        ok()

    def svc_purge(self, i):
        call_rpc('svc.purge', dict(svcs=[i]))
        ok()

    def svc_call(self, i, file, method, params):
        if file:
            import yaml
            payload = yaml.safe_load(read_file(file))
        else:
            payload = {}
            for p in params:
                n, v = p.split('=', 1)
                payload[n] = format_value(v, advanced=True)
        result = call_rpc(method, payload if payload else None, target=i)
        if current_command.json or isinstance(result, list):
            print_result(result)
        elif isinstance(result, dict):
            print_result(result, name_value=True)
        elif result is None:
            ok()
        else:
            print(result)
            print()

    def svc_edit(self, i):

        def deploy(cfg, i):
            call_rpc('svc.deploy', dict(svcs=[dict(id=i, params=cfg)]))
            print(f'service re-deployed: {i}')
            print()

        config = call_rpc('svc.get_params', dict(i=i))
        edit_config(config, f'svc|{i}|config', deploy_fn=partial(deploy, i=i))

    def svc_create(self, i, f):

        def deploy(cfg, i):
            call_rpc('svc.deploy', dict(svcs=cfg))
            print(f'service deployed: {i}')
            print()

        lines = read_file(f).decode().split('\n')
        tpl = (' ' * 4) + ('\n' + ' ' * 4).join(lines).rstrip()
        config = f'- id: {i}\n  params:\n{tpl}'
        if sys.stdin.isatty():
            edit_config(config,
                        f'svc|{i}|config',
                        deploy_fn=partial(deploy, i=i))
        else:
            import yaml
            deploy(yaml.safe_load(config), i)

    def svc_test(self, i):
        call_rpc('test', target=i)
        ok()

    def svc_info(self, i):
        data = call_rpc('info', target=i)
        if not current_command.json:
            try:
                del data['methods']
            except KeyError:
                pass
        print_result(data, need_header=False, name_value=True)

    def broker_test(self):
        call_rpc('test', target='.broker')
        ok()

    def broker_info(self):
        data = call_rpc('info', target='.broker')
        print_result(data, need_header=False, name_value=True)

    def broker_stats(self):
        data = call_rpc('stats', target='.broker')
        print_result(data, need_header=False, name_value=True)

    def broker_client_list(self):
        data = call_rpc('client.list', target='.broker')
        if current_command.json:
            print_result(data)
        else:
            print_result(
                [d for d in data['clients'] if d['name'] != common.elbus_name])

    def action_exec(self, i, status, value, priority, wait):
        params = dict(i=i, wait=wait)
        if priority is not None:
            params['priority'] = int(priority)
        params['status'] = int(status)
        if value is not None:
            params['value'] = format_value(value)
        result = call_rpc('action', params)
        if current_command.json:
            import uuid
            result['uuid'] = str(uuid.UUID(bytes=result['uuid']))
            print_result(result)
        else:
            print_action_result(result)

    def action_run(self, i, arg, kwarg, priority, wait):
        params = dict(i=i, wait=wait)
        if priority is not None:
            params['priority'] = int(priority)
        if arg:
            params['args'] = [format_value(v) for v in arg]
        if kwarg:
            kw = {}
            for k in kwarg:
                n, v = k.split('=', 1)
                kw[n] = format_value(v)
            params['kwargs'] = kw
        result = call_rpc('run', params)
        if current_command.json:
            import uuid
            result['uuid'] = str(uuid.UUID(bytes=result['uuid']))
            print_result(result)
        else:
            print_action_result(result)

    def action_toggle(self, i, priority, wait):
        params = dict(i=i, wait=wait)
        if priority is not None:
            params['priority'] = int(priority)
        result = call_rpc('action.toggle', params)
        if current_command.json:
            import uuid
            result['uuid'] = str(uuid.UUID(bytes=result['uuid']))
            print_result(result)
        else:
            print_action_result(result)

    def action_terminate(self, u):
        import uuid
        call_rpc('action.terminate', dict(u=uuid.UUID(u).bytes))
        ok()

    def action_kill(self, i):
        call_rpc('action.kill', dict(i=i))
        ok()

    def action_result(self, u):
        import uuid
        result = call_rpc('action.result', dict(u=uuid.UUID(u).bytes))
        if current_command.json:
            import uuid
            result['uuid'] = str(uuid.UUID(bytes=result['uuid']))
            print_result(result)
        else:
            print_action_result(result)

    def action_list(self, oid, status_query, svc, time, limit):
        import uuid
        from .tools import ACTION_STATUS_COLOR
        params = dict(i=oid, sq=status_query, svc=svc, time=time)
        if limit is not None:
            params['limit'] = limit
        result = call_rpc('action.list', params)
        if current_command.json:
            for r in result:
                r['uuid'] = str(uuid.UUID(bytes=r['uuid']))
            print_result(result)
        elif result:
            data = []
            for r in result:
                if r['status'] in ['completed', 'failed', 'terminated']:
                    times = [v for _, v in r['time'].items()]
                    elapsed = '{:.6f}'.format(max(times) - min(times))
                else:
                    elapsed = ''
                data.append({
                    'uuid': str(uuid.UUID(bytes=r['uuid'])),
                    'oid': r['oid'],
                    'status': r['status'],
                    'elapsed': elapsed,
                    'node': r['node'],
                    'svc': r['svc']
                })
            spacer = '  '
            header, rows = format_table(data, fmt=FORMAT_GENERATOR_COLS)
            for i, c in enumerate(header):
                if i > 0:
                    print(spacer, end='')
                print(colored(c, color='blue'), end='')
            print()
            print(
                colored('-' * (sum(len(s) for s in header) +
                               (len(header) - 1) * 2),
                        color='grey'))
            for d, r in zip(data, rows):
                for i, c in enumerate(r):
                    if i > 0:
                        print(spacer, end='')
                    if i == 2:
                        print(colored(c,
                                      color=ACTION_STATUS_COLOR.get(
                                          d['status'])),
                              end='')
                    else:
                        print(c, end='')
                print()

    def item_summary(self):
        data = call_rpc('item.summary')
        if current_command.json:
            print_result(data)
        else:
            print_result(data['sources'], name_value=['node', 'items'])
            print('total:', colored(data['items'], color='yellow'))
            print()

    def node_list(self):
        data = call_rpc('node.list')
        for d in data:
            if d['remote']:
                d['type'] = 'remote'
            else:
                d['type'] = 'local'
        print_result(data, cols=['name', 'svc', 'type', 'online'])

    def item_list(self, i, n=None):
        data = call_rpc(
            'item.list',
            dict(i=i, node=n),
        )
        print_result(data,
                     cols=[
                         'oid', 'status', 'value', 't|n=set time|f=time',
                         'node', 'connected', 'enabled'
                     ])

    def item_announce(self, i, n=None):
        data = call_rpc(
            'item.announce',
            dict(i=i, node=n),
        )
        ok()

    def item_export(self, i, output=None):
        import yaml
        c = 0
        configs = []
        for item in call_rpc('item.list', dict(i=i, node='.local')):
            c += 1
            configs.append(call_rpc('item.get_config', dict(i=item['oid'])))
        dump = yaml.dump(configs, default_flow_style=False)
        if output is None:
            print(dump)
        else:
            with open(output, 'w') as fh:
                fh.write(dump)
            print(f'{c} item(s) exported')
            print()

    def item_set(self, i, status, value):
        payload = dict(status=status, force=True)
        if value is not None:
            val = format_value(value)
            payload['value'] = val
        common.bus.send(
            'RAW/' + i.replace(':', '/', 1),
            elbus.client.Frame(msgpack.dumps(payload),
                               tp=elbus.client.OP_PUBLISH,
                               qos=1)).wait_completed()
        time.sleep(0.1)
        state = call_rpc('item.state', dict(i=i))[0]
        try:
            if state['status'] != status or (value is not None and
                                             state['value'] != val):
                err('FAILED')
            else:
                ok()
        except KeyError:
            err(f'{i} has no status')

    def item_deploy(self, file=None, replace=False):
        import yaml
        items = yaml.safe_load(read_file(file).decode())
        call_rpc('item.deploy', dict(items=items, replace=replace))
        print(f'{len(items)} item(s) deployed')
        print()

    def item_undeploy(self, file=None):
        import yaml
        items = yaml.safe_load(read_file(file).decode())
        call_rpc('item.undeploy', dict(items=items))
        print(f'{len(items)} item(s) undeployed')
        print()

    def item_create(self, i):
        call_rpc('item.create', dict(i=i))
        ok()

    def item_destroy(self, i):
        call_rpc('item.destroy', dict(i=i))
        ok()

    def item_enable(self, i):
        call_rpc('item.enable', dict(i=i))
        ok()

    def item_edit(self, i):

        def deploy_edited_item(cfg, i):
            call_rpc('item.deploy', dict(items=[cfg], replace=True))
            print(f'item re-deployed: {i}')
            print()

        config = call_rpc('item.get_config', dict(i=i))
        edit_config(config,
                    f'item|{i}|config',
                    deploy_fn=partial(deploy_edited_item, i=i))

    def item_disable(self, i):
        call_rpc('item.disable', dict(i=i))
        ok()

    def item_state(self, i, full):
        data = call_rpc(
            'item.state',
            dict(i=i, full=full),
        )
        print_result(data,
                     cols=[
                         'oid', 'status', 'value', 'ieid',
                         't|n=set time|f=time', 'node', 'connected', 'act'
                     ])

    def item_slog(self, i, db_svc, time_start, time_end, time_zone, limit):
        time_start = prepare_time(time_start)
        time_end = prepare_time(time_end)
        data = call_rpc('state_log',
                        dict(i=i,
                             t_start=time_start,
                             t_end=time_end,
                             limit=limit),
                        target=db_svc)
        print_result(
            data,
            cols=[
                'oid', 'status', 'value',
                't|n=time|f=time{}'.format(f':{time_zone}' if time_zone else '')
            ])

    def item_history(self, i, db_svc, time_start, time_end, time_zone, limit,
                     prop, fill):
        time_start = prepare_time(time_start)
        time_end = prepare_time(time_end)
        precs = None
        if fill is not None:
            if ':' in fill:
                fill, precs = fill.split(':', 1)
                precs = int(precs)
        data = call_rpc('state_history',
                        dict(i=i,
                             t_start=time_start,
                             t_end=time_end,
                             fill=fill,
                             precision=precs,
                             prop=prop,
                             limit=limit),
                        target=db_svc)
        cols = []
        if prop == 'status' or prop is None:
            cols += ['status']
        if prop == 'value' or prop is None:
            cols += ['value']
        cols += [
            't|n=time|f=time{}'.format(f':{time_zone}' if time_zone else '')
        ]
        print_result(data, cols=cols)

    def item_watch(self, i, interval, rows, prop, chart_type):
        from . import charts
        import datetime
        vals = []
        to_clear = 0
        old_width = 0
        old_height = 0
        limit = rows
        limit_auto_set = rows is None

        def _append(label, value, limit):
            if chart_type == 'bar':
                vals.append((label, value))
            else:
                if isinstance(value, float):
                    vals.append(value)
                else:
                    try:
                        v = float(value)
                    except:
                        v = 0
                    vals.append(v)
            while len(vals) > limit:
                vals.pop(0)

        next_step = time.perf_counter() + interval
        try:
            while True:
                if chart_type == 'bar':
                    label = datetime.datetime.now().strftime('%T.%f')[:-5]
                else:
                    label = datetime.datetime.now().isoformat()
                width, height = get_term_size()
                if limit is None:
                    if chart_type == 'bar':
                        limit = height - 2
                    else:
                        limit = width - 12
                if width != old_width or height != old_height:
                    os.system('clear')
                    if chart_type == 'bar':
                        print(colored(i, color='yellow'))
                    old_width, old_height = width, height
                    if limit_auto_set:
                        if chart_type == 'bar':
                            limit = height - 2
                        else:
                            rows = height - 6
                elif chart_type == 'bar':
                    for t in range(to_clear):
                        sys.stdout.write('\033[F\033[K')
                elif chart_type == 'line':
                    os.system('clear')
                res = call_rpc('item.state', dict(i=i))
                for data in res:
                    if data['oid'] == i:
                        break
                else:
                    raise ValueError('no state returned')
                v = data.get(prop)
                if isinstance(v, str):
                    try:
                        v = int(v)
                    except:
                        try:
                            v = float(v)
                        except:
                            v = None
                if chart_type == 'bar':
                    _append(label, v, limit)
                    charts.plot_bar_chart(vals)
                    to_clear = len(vals)
                else:
                    _append(label, v, width)
                    max_value_width = 0
                    for z in vals:
                        x = len(str(z))
                        if x > max_value_width:
                            max_value_width = x
                    while len(vals) > width - (max_value_width if
                                               max_value_width > 7 else 7) - 5:
                        vals.pop(0)
                    max_value_width += 2
                    print(
                        f'{colored(i, color="yellow")} '
                        f'{colored(label, color="cyan")}: ',
                        end='')
                    if v is None:
                        print(colored('NaN', color='magenta'))
                    else:
                        print(colored(v, color='green', attrs='bold'))
                    charts.plot_line_chart(vals, rows, max_value_width)
                t = time.perf_counter()
                sleep_to = next_step - t
                if sleep_to > 0:
                    time.sleep(sleep_to)
                    next_step += interval
                else:
                    next_step = t
        except KeyboardInterrupt:
            return
        pass

    def lvar_set(self, i, status, value):
        params = dict(i=i)
        if status is not None:
            params['status'] = status
        if value is not None:
            params['value'] = format_value(value)
        call_rpc('lvar.set', params)
        ok()

    def lvar_reset(self, i):
        call_rpc('lvar.reset', dict(i=i))
        ok()

    def lvar_clear(self, i):
        call_rpc('lvar.clear', dict(i=i))
        ok()

    def lvar_toggle(self, i):
        call_rpc('lvar.toggle', dict(i=i))
        ok()

    def lvar_incr(self, i):
        val = call_rpc('lvar.incr', dict(i=i))
        print(val)

    def lvar_decr(self, i):
        val = call_rpc('lvar.decr', dict(i=i))
        print(val)

    def version(self):
        from . import __version__
        info = get_node_svc_info()
        if current_command.json:
            d = {
                'cli_version': __version__,
                'build': info['build'],
                'version': info['version'],
            }
        else:
            d = [{
                'name': 'version',
                'value': info['version']
            }, {
                'name': 'build',
                'value': info['build']
            }, {
                'name': 'CLI version',
                'value': __version__
            }]
        print_result(d, need_header=False, name_value=False)
