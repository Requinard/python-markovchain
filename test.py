import markov
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr


class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        if type(self.channel) == str:
            c.join(self.channel)
        else:
            for chan in self.channel:
                c.join(chan)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        try:
            brain.learn(a[1])
        except Exception:
            brain.learn(a[0])
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments[0])

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))
        else:
            c.notice(nick, "Not understood: " + cmd)


if __name__ == '__main__':
    brain = markov.Brain()

    try:
        brain.load()
    except:
        brain.learn(
            'hi my name is Al and i live in a box that i like very much and i can live in there as long as i want')
        brain.learn(
            "The problem is motivation. You wanna learn something? But the fact is you are in prison. Yeah you can learn about rocket science and become a master in it but no one gonna give you a job since you have a record. I am not saying you shouldn't learn but to develop that focus when you are in prison probably the hardest thing someone can do. Just my opinion, I think the motivation is very important.")
        brain.learn(
            "Served 30 months in Florida at age 18...food was terrible, boredom is mind numbing, the feeling that the world is leaving you behind is quite painful...perhaps the worst of it though is the stigma associated with being a convicted felon. I have been turned down twice for jobs I am capable of excelling at (former space coast area Machinist now living in oil country). Problem is, I am totally honest with them and the convictions are 25 years old.")

        brain.learn(
            "Served 30 months in Florida at age 18...food was terrible, boredom is mind numbing, the feeling that the world is leaving you behind is quite painful...perhaps the worst of it though is the stigma associated with being a convicted felon. I have been turned down twice for jobs I am capable of excelling at (former space coast area Machinist now living in oil country). Problem is, I am totally honest with them and the convictions are 25 years old.")

    bot_news = TestBot(["#news", "#8chan"], "samynv", "irc.rizon.net")

    bot_news.start()