"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    count = 0  # Example state variable

    @staticmethod
    def increment():
        State.count += 1

    @staticmethod
    def decrement():
        State.count -= 1


def app_component() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to My Reflex App"),
        rx.hstack(
            rx.button("Increment", on_click=State.increment),
            rx.button("Decrement", on_click=State.decrement),
        ),
        rx.text(f"Current Count: {State.count}"),
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(app_component)
