#!/usr/bin/env python3
import os
import click
from app import create_app

@click.group()
def cli():
    """ICHTP Rebuild 管理工具"""
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host address')
@click.option('--port', default=5000, help='Port')
@click.option('--debug', is_flag=True, default=True, help='Enable debug mode')
def run(host, port, debug):
    """啟動本地開發伺服器"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)

@cli.command()
def env():
    """顯示關鍵環境變數"""
    print("FLASK_ENV        =", os.getenv("FLASK_ENV"))
    print("SECRET_KEY       =", os.getenv("SECRET_KEY"))
    print("STATIC_ROOT      =", os.path.abspath("static"))
    print("TEMPLATES_ROOT   =", os.path.abspath("app/templates"))

if __name__ == "__main__":
    cli()
