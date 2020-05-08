import Event = Laya.Event;
import Socket = Laya.Socket;
import Byte = Laya.Byte;



export class Net {
    public static _inst: Net;
    private socket: Socket;
    constructor() {
        console.log("Net         constructor");

    }
    public static Init(): Net {
        if (this._inst == null || this._inst == undefined) {
            this._inst = new Net();
        }
        return this._inst;
    }

    public connect(): void {
        this.socket = new Socket();

        var _name = Math.random() * 1000 + "_______aaaaa";
        var url = "ws://127.0.0.1:8001/chat?username=" + _name + ""
        this.socket.connectByUrl(url);

        this.socket.on(Event.OPEN, this, this.onSocketOpen);
        this.socket.on(Event.CLOSE, this, this.onSocketClose);
        this.socket.on(Event.MESSAGE, this, this.onMessageReveived);
        this.socket.on(Event.ERROR, this, this.onConnectError);
    }
    private onSocketOpen(): void {
        console.log("onSocketOpen");
        this.sendTestMsg();
    }
    private onSocketClose(): void {
        console.log("onSocketClose");
    }
    private onMessageReveived(): void {
        console.log("onMessageReveived");
    }
    private onConnectError(): void {
        console.log("onConnectError");
    }
    private sendTestMsg(): void {
        var _msg: Object;
        _msg = {
            id: 111111,
            msg: "222222222",
        }
        _msg = JSON.stringify(_msg);
        if (this.socket.connected) {
            this.socket.send(_msg);
        }

    }

}
