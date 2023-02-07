from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path
from devops.websocket.terminal_consumers import StreamConsumer
from devops.websocket.logs_consumers import StreamLogConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^workload/terminal/(?P<namespace>.*)/(?P<pod_name>.*)/(?P<container>.*)/', StreamConsumer),
            re_path(r'^workload/container_log/(?P<namespace>.*)/(?P<pod_name>.*)/(?P<container>.*)/', StreamLogConsumer),
        ])
    ),
})