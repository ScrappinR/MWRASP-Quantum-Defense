"""
CLI Management Tools for Homomorphic Swarm
Command-line interface for operations and administration
"""

import click
import asyncio
import aiohttp
import json
import yaml
from tabulate import tabulate
from typing import Dict, List, Any, Optional
import time
from datetime import datetime
import os

# Configuration
DEFAULT_CONFIG = {
    "queen_url": os.getenv("SWARM_QUEEN_URL", "https://localhost:8443"),
    "auth_token": os.getenv("SWARM_AUTH_TOKEN"),
    "output_format": "table"
}

@click.group()
@click.option('--config', '-c', type=click.Path(exists=True), help='Config file path')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), default='table')
@click.pass_context
def cli(ctx, config, format):
    """Homomorphic Swarm Management CLI"""
    ctx.ensure_object(dict)
    
    # Load config
    if config:
        with open(config) as f:
            ctx.obj = yaml.safe_load(f)
    else:
        ctx.obj = DEFAULT_CONFIG.copy()
        
    ctx.obj['output_format'] = format

@cli.group()
@click.pass_context
def node(ctx):
    """Node management commands"""
    pass

@node.command()
@click.pass_context
def list(ctx):
    """List all nodes in the swarm"""
    async def _list_nodes():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            async with session.get(f"{ctx.obj['queen_url']}/api/v1/nodes", headers=headers) as resp:
                if resp.status == 200:
                    nodes = await resp.json()
                    
                    if ctx.obj['output_format'] == 'json':
                        click.echo(json.dumps(nodes, indent=2))
                    elif ctx.obj['output_format'] == 'yaml':
                        click.echo(yaml.dump(nodes))
                    else:
                        # Table format
                        table_data = []
                        for n in nodes:
                            table_data.append([
                                n['id'],
                                n['type'],
                                n['host'],
                                n['port'],
                                '✓' if n['active'] else '✗',
                                f"{n['trust_score']:.2f}"
                            ])
                        click.echo(tabulate(
                            table_data,
                            headers=['ID', 'Type', 'Host', 'Port', 'Active', 'Trust'],
                            tablefmt='grid'
                        ))
                else:
                    click.echo(f"Error: {resp.status}")
                    
    asyncio.run(_list_nodes())

@node.command()
@click.argument('node_id')
@click.pass_context
def info(ctx, node_id):
    """Get detailed info about a node"""
    async def _node_info():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            async with session.get(f"{ctx.obj['queen_url']}/api/v1/nodes/{node_id}", headers=headers) as resp:
                if resp.status == 200:
                    node_data = await resp.json()
                    
                    click.echo(f"\nNode: {node_id}")
                    click.echo(f"Type: {node_data['type']}")
                    click.echo(f"Status: {'Active' if node_data['active'] else 'Inactive'}")
                    click.echo(f"Trust Score: {node_data['trust_score']:.2f}")
                    click.echo(f"Tasks Completed: {node_data['tasks_completed']}")
                    click.echo(f"Last Heartbeat: {node_data['last_heartbeat']}")
                    
                    if 'performance' in node_data:
                        click.echo("\nPerformance Metrics:")
                        for metric, value in node_data['performance'].items():
                            click.echo(f"  {metric}: {value}")
                            
    asyncio.run(_node_info())

@node.command()
@click.argument('node_id')
@click.option('--reason', '-r', required=True, help='Reason for exclusion')
@click.pass_context
def exclude(ctx, node_id, reason):
    """Exclude a node from the swarm"""
    if click.confirm(f'Are you sure you want to exclude node {node_id}?'):
        async def _exclude_node():
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
                data = {"reason": reason}
                async with session.post(
                    f"{ctx.obj['queen_url']}/api/v1/nodes/{node_id}/exclude",
                    headers=headers,
                    json=data
                ) as resp:
                    if resp.status == 200:
                        click.echo(f"Node {node_id} excluded successfully")
                    else:
                        click.echo(f"Error: {resp.status}")
                        
        asyncio.run(_exclude_node())

@cli.group()
@click.pass_context
def compute(ctx):
    """Computation commands"""
    pass

@compute.command()
@click.argument('operation', type=click.Choice(['add', 'multiply', 'bootstrap']))
@click.option('--data', '-d', required=True, help='Input data (JSON)')
@click.option('--wait/--no-wait', default=True, help='Wait for result')
@click.pass_context
def submit(ctx, operation, data, wait):
    """Submit computation job"""
    async def _submit_compute():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            
            # Parse input data
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                click.echo("Error: Invalid JSON data")
                return
                
            payload = {
                "operation": operation,
                "data": parsed_data
            }
            
            async with session.post(
                f"{ctx.obj['queen_url']}/api/v1/compute",
                headers=headers,
                json=payload
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    click.echo(f"Operation ID: {result['operation_id']}")
                    
                    if wait:
                        # Poll for result
                        click.echo("Waiting for result...")
                        final_result = await _wait_for_result(
                            session, 
                            result['operation_id'],
                            headers
                        )
                        click.echo(f"Result: {final_result}")
                        
    async def _wait_for_result(session, operation_id, headers):
        while True:
            async with session.get(
                f"{ctx.obj['queen_url']}/api/v1/operations/{operation_id}",
                headers=headers
            ) as resp:
                if resp.status == 200:
                    op_data = await resp.json()
                    if op_data['status'] == 'completed':
                        return op_data['result']
                    elif op_data['status'] == 'failed':
                        return f"Failed: {op_data.get('error', 'Unknown error')}"
            await asyncio.sleep(1)
            
    asyncio.run(_submit_compute())

@cli.group()
@click.pass_context
def monitor(ctx):
    """Monitoring commands"""
    pass

@monitor.command()
@click.option('--interval', '-i', default=5, help='Update interval in seconds')
@click.pass_context
def status(ctx, interval):
    """Monitor swarm status"""
    async def _monitor_status():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            
            while True:
                try:
                    async with session.get(
                        f"{ctx.obj['queen_url']}/api/v1/status",
                        headers=headers
                    ) as resp:
                        if resp.status == 200:
                            status = await resp.json()
                            
                            # Clear screen
                            click.clear()
                            
                            # Header
                            click.echo("HOMOMORPHIC SWARM STATUS")
                            click.echo("=" * 50)
                            click.echo(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            click.echo()
                            
                            # Metrics
                            click.echo(f"Average Speedup: {status['average_speedup']:.1f}%")
                            click.echo(f"Total Operations: {status['total_operations']:,}")
                            click.echo(f"Byzantine Detections: {status['byzantine_detections']}")
                            click.echo()
                            
                            # Node summary
                            active_nodes = sum(1 for n in status['nodes'].values() if n['active'])
                            click.echo(f"Active Nodes: {active_nodes}/{len(status['nodes'])}")
                            
                            # Node table
                            node_data = []
                            for node_id, info in status['nodes'].items():
                                node_data.append([
                                    node_id,
                                    info['type'],
                                    '✓' if info['active'] else '✗',
                                    f"{info['trust_score']:.2f}"
                                ])
                            
                            click.echo()
                            click.echo(tabulate(
                                node_data,
                                headers=['Node', 'Type', 'Active', 'Trust'],
                                tablefmt='simple'
                            ))
                            
                    await asyncio.sleep(interval)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"Error: {e}")
                    await asyncio.sleep(interval)
                    
    asyncio.run(_monitor_status())

@monitor.command()
@click.pass_context
def metrics(ctx):
    """Display performance metrics"""
    async def _show_metrics():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            async with session.get(f"{ctx.obj['queen_url']}/metrics", headers=headers) as resp:
                if resp.status == 200:
                    metrics_text = await resp.text()
                    click.echo(metrics_text)
                    
    asyncio.run(_show_metrics())

@cli.group()
@click.pass_context
def batch(ctx):
    """Batch job commands"""
    pass

@batch.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--job-type', '-t', required=True, help='Job type')
@click.option('--priority', '-p', default=5, help='Priority (1-10)')
@click.pass_context
def submit(ctx, file_path, job_type, priority):
    """Submit batch job from file"""
    with open(file_path) as f:
        data = json.load(f)
        
    async def _submit_batch():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            
            payload = {
                "job_type": job_type,
                "items": data,
                "priority": priority
            }
            
            async with session.post(
                f"{ctx.obj['queen_url']}/api/v1/batch",
                headers=headers,
                json=payload
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    click.echo(f"Batch job ID: {result['job_id']}")
                else:
                    click.echo(f"Error: {resp.status}")
                    
    asyncio.run(_submit_batch())

@batch.command()
@click.argument('job_id')
@click.pass_context
def status(ctx, job_id):
    """Check batch job status"""
    async def _job_status():
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {ctx.obj['auth_token']}"}
            async with session.get(
                f"{ctx.obj['queen_url']}/api/v1/batch/{job_id}",
                headers=headers
            ) as resp:
                if resp.status == 200:
                    job_data = await resp.json()
                    
                    click.echo(f"Job ID: {job_id}")
                    click.echo(f"Status: {job_data['status']}")
                    click.echo(f"Progress: {job_data['completed']}/{job_data['total']}")
                    
                    if job_data['status'] == 'completed':
                        click.echo(f"Completed at: {job_data['completed_at']}")
                    elif job_data['status'] == 'failed':
                        click.echo(f"Error: {job_data['error']}")
                        
    asyncio.run(_job_status())

@cli.group()
@click.pass_context
def config(ctx):
    """Configuration commands"""
    pass

@config.command()
@click.pass_context
def show(ctx):
    """Show current configuration"""
    click.echo(yaml.dump(ctx.obj, default_flow_style=False))

@config.command()
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx, key, value):
    """Set configuration value"""
    ctx.obj[key] = value
    
    # Save to config file
    config_path = os.path.expanduser("~/.swarm/config.yaml")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(ctx.obj, f)
        
    click.echo(f"Set {key} = {value}")

@cli.command()
@click.pass_context
def shell(ctx):
    """Interactive shell"""
    import readline
    import rlcompleter
    
    # Setup readline
    readline.parse_and_bind("tab: complete")
    
    click.echo("Homomorphic Swarm Interactive Shell")
    click.echo("Type 'help' for commands, 'exit' to quit")
    
    while True:
        try:
            cmd = input("swarm> ").strip()
            if cmd == 'exit':
                break
            elif cmd == 'help':
                click.echo("Available commands: node, compute, monitor, batch, config")
            else:
                # Parse and execute command
                parts = cmd.split()
                if parts:
                    # Execute CLI command
                    try:
                        cli.main(parts, standalone_mode=False)
                    except SystemExit:
                        pass
        except KeyboardInterrupt:
            click.echo("\nUse 'exit' to quit")
        except EOFError:
            break

if __name__ == '__main__':
    cli()
