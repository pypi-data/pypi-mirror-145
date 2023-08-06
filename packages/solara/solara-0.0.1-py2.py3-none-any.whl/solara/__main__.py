import os
import site
import sys
import threading
import time
import typing
import webbrowser

import rich_click as click
import uvicorn

HOST_DEFAULT = os.environ.get("HOST", "localhost")
if "arm64-apple-darwin" in HOST_DEFAULT:  # conda activate script
    HOST_DEFAULT = "localhost"


def find_all_packages_paths():
    paths = []
    # sitepackages = set([os.path.dirname(k) for k in site.getsitepackages()])
    sitepackages = set([k for k in site.getsitepackages()])
    paths.extend(list(sitepackages))
    print(sitepackages)
    for name, module in sys.modules.items():
        if hasattr(module, "__path__"):
            try:
                path = module.__path__[0]
            except:  # noqa: E722
                pass  # happens for namespace packages it seems
                # print(f"Error for {name}")
                # if path:
                #     skip = False
                #     for sitepackage in sitepackages:
                #         if path.startswith(sitepackage):
                #             skip = True
                # if not skip:
                # print(name, path, skip)
                paths.append(str(path))
    # print("PATHS", paths)
    return paths


@click.command()
@click.option("--port", default=int(os.environ.get("PORT", 8765)))
@click.option("--host", default=HOST_DEFAULT)
@click.option("--dev/--no-devn", default=False)
@click.option("--open/--no-open", default=False)
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload.")
@click.option(
    "--reload-dir",
    "reload_dirs",
    multiple=True,
    help="Set reload directories explicitly, instead of using the current working" " directory.",
    type=click.Path(exists=True),
)
@click.option(
    "--reload-exclude",
    "reload_excludes",
    multiple=True,
    help="Set glob patterns to exclude while watching for files. Includes "
    "'.*, .py[cod], .sw.*, ~*' by default; these defaults can be overridden "
    "with `--reload-include`. This option has no effect unless watchgod is "
    "installed.",
)
@click.option(
    "--workers",
    default=None,
    type=int,
    help="Number of worker processes. Defaults to the $WEB_CONCURRENCY environment" " variable if available, or 1. Not valid with --reload.",
)
@click.argument("app")
def main(app, host, port, open, reload: bool, reload_dirs: typing.Optional[typing.List[str]], dev: bool, reload_excludes: typing.List[str], workers: int):
    reload_dirs = reload_dirs if reload_dirs else None
    url = f"http://{host}:{port}"

    failed = False
    if dev:
        reload_dirs = reload_dirs if reload_dirs else []
        reload_dirs = list(reload_dirs) + list(find_all_packages_paths())
        reload = True

    def open_browser():
        import socket

        s = socket.socket()
        for i in range(100):
            if failed:
                return
            try:
                s.connect((host, port))
                break
            except Exception as e:
                print(f"Server is not running get, will try again soon: {e}")
            time.sleep(1)

        print(f"Server is up, opening page {url}, disable this option by passing the --no-open argument to solara")
        webbrowser.open(url)

    if open:
        threading.Thread(target=open_browser, daemon=True).start()

    kwargs = locals().copy()
    os.environ["SOLARA_APP"] = app
    kwargs["app"] = "solara.server.fastapi:app"
    for item in "open_browser open url failed dev".split():
        del kwargs[item]
    try:
        uvicorn.run(**kwargs)
    finally:
        failed = True


if __name__ == "__main__":
    main()
