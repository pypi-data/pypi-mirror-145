import logging
from tempfile import TemporaryDirectory
from uuid import uuid4

import rsa

# freezegun is not available in every project. This is ok if the tests are not executed there.
# Catch and raise the import errors to silence pylint:
try:
    import freezegun
except ImportError as importError:
    raise importError

from ..access_token_tools import AccessTokenTools, AccessTokenToolsException


def test_access_token():
    logger = logging.getLogger("test_access_token")
    logger.setLevel(logging.DEBUG)
    with TemporaryDirectory() as temp_directory:
        keys_directory = str(temp_directory)

        keys_creator = AccessTokenTools(keys_directory)
        keys_creator.create_rsa_key_files(logger)

        access_token_tools = AccessTokenTools(keys_directory)

        test_id = str(uuid4())
        test_id_2 = str(uuid4())
        valid_period = 5 * 60

        with freezegun.freeze_time("1970-01-01T00:00:00"):
            # Create a first token and verify its data
            token = access_token_tools.create_token(subject=test_id, expires_after_seconds=valid_period)
            assert type(token) == str
            assert len(token) > 0
            payload = access_token_tools.decode_payload(token)
            assert payload["sub"] == test_id
            assert payload["exp"] == valid_period
            assert access_token_tools.validate(token, test_id)
            assert not access_token_tools.validate(token, test_id_2)

            # Create a second token with the same data, it must have a different access token
            token2 = access_token_tools.create_token(subject=test_id, expires_after_seconds=valid_period)
            assert type(token2) == str
            assert token2 != token
            payload2 = access_token_tools.decode_payload(token2)
            assert payload2["sub"] == test_id
            assert payload2["exp"] == valid_period
            assert access_token_tools.validate(token2, test_id)
            assert not access_token_tools.validate(token2, test_id_2)

            # Create a third token with a different id, it must have a different access token
            token3 = access_token_tools.create_token(subject=test_id_2, expires_after_seconds=valid_period)
            assert type(token3) == str
            assert token3 != token
            assert token3 != token2
            payload3 = access_token_tools.decode_payload(token3)
            assert payload3["sub"] == test_id_2
            assert payload3["exp"] == valid_period
            assert access_token_tools.validate(token3, test_id_2)
            assert not access_token_tools.validate(token3, test_id)

            # Token must validate with the same test_id
            assert access_token_tools.validate(token, test_id) is True
            assert access_token_tools.validate(token2, test_id) is True
            assert access_token_tools.validate(token3, test_id_2) is True

            # Token may not validate with a different test_id
            assert access_token_tools.validate(token, str(uuid4())) is False
            assert access_token_tools.validate(token2, test_id_2) is False
            assert access_token_tools.validate(token3, test_id) is False

        # Let the tokens expire, they may not validate afterwards
        with freezegun.freeze_time("1970-01-01T00:05:01"):
            assert access_token_tools.validate(token, test_id) is False
            assert access_token_tools.validate(token2, test_id) is False
            assert access_token_tools.validate(token3, test_id_2) is False

        # Create a new token that will be refreshed before it expires
        with freezegun.freeze_time("1970-01-01T00:00:00"):
            token = access_token_tools.create_token(subject=test_id, expires_after_seconds=valid_period)
            token2 = access_token_tools.create_token(subject=test_id_2, expires_after_seconds=valid_period)

        with freezegun.freeze_time("1970-01-01T00:04:59"):
            assert access_token_tools.validate(token, test_id) is True
            assert access_token_tools.validate(token2, test_id) is False
            assert access_token_tools.validate(token2, test_id_2) is True
            token = access_token_tools.create_token(subject=test_id, expires_after_seconds=valid_period)
            token2 = access_token_tools.create_token(subject=test_id_2, expires_after_seconds=valid_period)

        with freezegun.freeze_time("1970-01-01T00:09:59"):
            assert access_token_tools.validate(token, test_id) is True
            assert access_token_tools.validate(token2, test_id_2) is True

        with freezegun.freeze_time("1970-01-01T00:10:00"):
            assert access_token_tools.validate(token, test_id) is False
            assert access_token_tools.validate(token2, test_id_2) is False


def test_access_token_verify_private_public_keys():
    logger = logging.getLogger("test_access_token")
    logger.setLevel(logging.DEBUG)
    with TemporaryDirectory() as temp_directory:
        keys_directory = str(temp_directory)

        keys_creator = AccessTokenTools(keys_directory)
        keys_creator.create_rsa_key_files(logger)

        access_token_tools = AccessTokenTools(keys_directory)
        assert b"BEGIN RSA PUBLIC KEY" in access_token_tools.public_key
        assert b"BEGIN RSA PUBLIC KEY" not in access_token_tools.private_key
        assert b"BEGIN RSA PRIVATE KEY" not in access_token_tools.public_key
        assert b"BEGIN RSA PRIVATE KEY" in access_token_tools.private_key

        try:
            rsa.PublicKey.load_pkcs1(access_token_tools.private_key)
            assert not "AccessTokenTools.private_key contains a public key"
        except ValueError as e:
            assert "No PEM start marker \"b'-----BEGIN RSA PUBLIC KEY-----'\" found" in str(e)

        try:
            rsa.PrivateKey.load_pkcs1(access_token_tools.public_key)
            assert not "AccessTokenTools.public_key contains a private key"
        except ValueError as e:
            assert "No PEM start marker \"b'-----BEGIN RSA PRIVATE KEY-----'\" found" in str(e)

        assert rsa.PublicKey.load_pkcs1(access_token_tools.public_key) is not None
        assert rsa.PrivateKey.load_pkcs1(access_token_tools.private_key) is not None


def test_access_token_key_files_must_exist():
    logger = logging.getLogger("test_access_token")
    logger.setLevel(logging.DEBUG)
    with TemporaryDirectory() as temp_directory:
        keys_directory = str(temp_directory)
        try:
            assert AccessTokenTools(f"{keys_directory}/does_not_exist").public_key is None
            assert AccessTokenTools(f"{keys_directory}/does_not_exist").private_key is None
            assert not "Expected 'AccessTokenToolsException' did not occur"
        except AccessTokenToolsException:
            pass

        try:
            assert AccessTokenTools(keys_directory).public_key is None
            assert AccessTokenTools(keys_directory).private_key is None
            assert not "Expected 'AccessTokenToolsException' did not occur"
        except AccessTokenToolsException:
            pass

        try:
            AccessTokenTools(keys_directory).create_rsa_key_files(logger)
            assert AccessTokenTools(keys_directory).public_key is not None
            assert AccessTokenTools(keys_directory).private_key is not None
        except AccessTokenToolsException as e:
            assert not f"Unexpected 'AccessTokenToolsException' occurred: {e}"
