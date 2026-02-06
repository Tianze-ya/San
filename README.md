# Feturre

1. UI
2. 热更新
3. 远程执行
4. WebSocket

{
name:str,
sender:str,["node","server","client"]
status:str,["ready","success","fail"]
ip:str,["x.x.x.x",""]
token:str,
data:str
}

[{
"ping","node","ready","","xxx",""
},{
"pong","server","success","","",""
}]
[
{
"requestPhoto","node","ready","","xxx","x.x.x.x"
},{
"getPhoto","server","ready","","",""
},{
"photo","client","success","x.x.x.x","","PhotoBytes"
},{
"returnPhoto","server","success","","","PhotoPath"
}
]
