# coding=utf-8
import unittest
from datetime import datetime
from decimal import Decimal

from fluent_compiler.bundle import FluentBundle

from fluentogram import (
    FluentTranslator,
    TranslatorHub,
    TranslatorRunner,
    MoneyTransformer,
    DateTimeTransformer,
)


class BasicUsage(unittest.TestCase):
    def test_full_usage(self):
        example_ftl_file_content = """
welcome = Welcome to the fluent aiogram addon!
greet-by-name = Hello, { $user }!
shop-success-payment = Your money, { $amount }, has been sent successfully at { $dt }.
        """
        t_hub = TranslatorHub(
            {"ua": ("ua", "ru", "en"), "ru": ("ru", "en"), "en": ("en",)},
            translators=[
                FluentTranslator(
                    locale="en",
                    translator=FluentBundle.from_string(
                        "en-US", example_ftl_file_content, use_isolating=False
                    ),
                )
            ],
            root_locale="en",
        )
        translator_runner: TranslatorRunner = t_hub.get_translator_by_locale("en")

        # Welcome to the fluent aiogram addon!
        # Hello, Alex!
        # Your money, $500.00, has been sent successfully at Apr 10, 2023.
        print(
            "You have to manually check the correctness of the output:\n",
            translator_runner.welcome(),
            translator_runner.greet.by.name(user="Alex"),
            translator_runner.shop.success.payment(
                amount=MoneyTransformer(currency="$", amount=Decimal("500")),
                dt=DateTimeTransformer(datetime.now()),
            ),
            sep="\n",
        )

        assert translator_runner.welcome() == "Welcome to the fluent aiogram addon!"
        assert translator_runner.greet.by.name(user="Alex") == "Hello, Alex!"
