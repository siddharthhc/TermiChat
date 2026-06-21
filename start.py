from instagrapi import Client
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Input,
    Static,
    ListView,
    ListItem
)
from textual.reactive import reactive
from rich.text import Text
import threading
import time

# =========================
# LOGIN
# =========================

cl = Client()

cl.load_settings("session.json")

cl.login_by_sessionid(
    cl.get_settings()["authorization_data"]["sessionid"]
)

print("[+] Instagram Login Success")

# =========================
# CHAT BOX
# =========================

class ChatBox(Static):

    messages = reactive("")

    def clear_chat(self):

        self.messages = ""

        self.update("")

    def add_message(
        self,
        sender,
        text,
        tm,
        mine=False
    ):

        color = "green" if mine else "magenta"

        self.messages += (
            f"[{color}]"
            f"[{tm}] {sender}: {text}"
            f"[/{color}]\n"
        )

        self.update(
            Text.from_markup(self.messages)
        )

# =========================
# MAIN APP
# =========================

class InstaDM(App):

    CSS = """

    Screen {
        layout: horizontal;
    }

    #left {
        width: 30%;
        border: solid cyan;
    }

    #right {
        width: 70%;
        border: solid magenta;
    }

    #chatbox {
        height: 90%;
        overflow-y: auto;
    }

    """

    current_thread_id = None
    current_username = None

    shown_per_thread = {}

    # IMPORTANT
    active_chat_token = 0

    def compose(self) -> ComposeResult:

        yield Header()

        with Horizontal():

            with Vertical(id="left"):

                yield Static(
                    " Instagram DMs "
                )

                self.chat_list = ListView()

                yield self.chat_list

            with Vertical(id="right"):

                self.chatbox = ChatBox(
                    id="chatbox"
                )

                yield self.chatbox

                self.msg_input = Input(
                    placeholder="Type message..."
                )

                yield self.msg_input

        yield Footer()

    # =========================
    # LOAD THREADS
    # =========================

    def on_mount(self):

        self.load_threads()

    def load_threads(self):

        self.threads = cl.direct_threads(
            amount=20
        )

        for t in self.threads:

            try:

                username = t.users[0].username

                self.chat_list.append(
                    ListItem(
                        Static(f"@{username}")
                    )
                )

            except:
                pass

    # =========================
    # OPEN CHAT
    # =========================

    def on_list_view_selected(self, event):

        index = event.list_view.index

        thread = self.threads[index]

        self.current_thread_id = thread.id

        self.current_username = (
            thread.users[0].username
        )

        # NEW TOKEN
        self.active_chat_token += 1

        token = self.active_chat_token

        self.chatbox.clear_chat()

        if (
            self.current_thread_id
            not in self.shown_per_thread
        ):

            self.shown_per_thread[
                self.current_thread_id
            ] = set()

        # LOAD OLD MSGS
        msgs = cl.direct_messages(
            self.current_thread_id,
            amount=20
        )

        msgs.reverse()

        shown = self.shown_per_thread[
            self.current_thread_id
        ]

        for msg in msgs:

            shown.add(msg.id)

            text = (
                msg.text
                if msg.text
                else "[MEDIA]"
            )

            tm = msg.timestamp.strftime(
                "%H:%M"
            )

            mine = (
                str(msg.user_id)
                == str(cl.user_id)
            )

            sender = (
                "ME"
                if mine
                else self.current_username
            )

            self.chatbox.add_message(
                sender,
                text,
                tm,
                mine
            )

        # START RECEIVER FOR THIS CHAT
        threading.Thread(
            target=self.receiver_loop,
            args=(token,),
            daemon=True
        ).start()

    # =========================
    # SEND MESSAGE
    # =========================

    def on_input_submitted(self, event):

        if not self.current_thread_id:
            return

        msg = event.value.strip()

        if not msg:
            return

        try:

            users = cl.direct_thread(
                self.current_thread_id
            ).users

            ids = [u.pk for u in users]

            cl.direct_send(msg, ids)

            self.msg_input.value = ""

        except Exception as e:

            self.chatbox.add_message(
                "SYSTEM",
                str(e),
                "ERR"
            )

    # =========================
    # RECEIVER
    # =========================

    def receiver_loop(self, token):

        thread_id = self.current_thread_id

        username = self.current_username

        while True:

            try:

                # STOP OLD THREAD
                if token != self.active_chat_token:
                    return

                msgs = cl.direct_messages(
                    thread_id,
                    amount=10
                )

                msgs.reverse()

                shown = (
                    self.shown_per_thread
                    .setdefault(
                        thread_id,
                        set()
                    )
                )

                for msg in msgs:

                    if msg.id in shown:
                        continue

                    shown.add(msg.id)

                    text = (
                        msg.text
                        if msg.text
                        else "[MEDIA]"
                    )

                    tm = msg.timestamp.strftime(
                        "%H:%M"
                    )

                    mine = (
                        str(msg.user_id)
                        == str(cl.user_id)
                    )

                    sender = (
                        "ME"
                        if mine
                        else username
                    )

                    self.call_from_thread(
                        self.chatbox.add_message,
                        sender,
                        text,
                        tm,
                        mine
                    )

            except:
                pass

            time.sleep(1)

# =========================
# RUN
# =========================

app = InstaDM()

app.run()
