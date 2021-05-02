import contextlib
import os
import posixpath
import socket
import sys
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, SimpleHTTPRequestHandler


def _get_best_family(*address):
    infos = socket.getaddrinfo(
        *address,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    family, type, proto, canonname, sockaddr = next(iter(infos))
    return family, sockaddr


class PacHTTPRequestHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in '.pac':
            return 'application/x-ns-proxy-autoconfig'
        return super().guess_type(path)

    def copyfile(self, source, outputfile):
        super().copyfile(source, outputfile)


def run(HandlerClass=BaseHTTPRequestHandler,
        ServerClass=ThreadingHTTPServer,
        protocol="HTTP/1.0", port=8000, bind=None):
    ServerClass.address_family, addr = _get_best_family(bind, port)

    HandlerClass.protocol_version = protocol
    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving Pac server HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )
        httpd.serve_forever()


def start_(bind=None, port=10811):
    """

    :param port:
    :type bind: object
    """
    handler_class = partial(PacHTTPRequestHandler,
                            directory=os.getcwd())

    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    run(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=port,
        bind=bind,
    )



