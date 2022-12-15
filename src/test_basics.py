from unittest.mock import Mock
from flask import Flask, redirect, make_response, url_for
import webwork
import dbdata
from main import stays, index, register, home


def test_index():
    # Arrange
    app = Flask(__name__)

    with app.test_request_context():
        # Act
        result = index()

        # Assert
        assert isinstance(result, redirect)
        assert result.location == url_for('register')


def test_register():
    # Arrange
    app = Flask(__name__)

    with app.test_request_context():
        # Act
        result = register()

        # Assert
        assert isinstance(result, make_response)
        assert "register.html" in result.response
        assert "UserID=0" in result.cookies
        assert result.cookies["UserID"].max_age == 0


def test_home():
    # Arrange
    app = Flask(__name__)
    with app.test_request_context(method="POST", referrer="/register"):
        webwork.signup_in = Mock(return_value="signup_in_result")

        # Act
        result = home()

        # Assert
        assert result == "signup_in_result"

    with app.test_request_context(method="POST", referrer="/stays"):
        webwork.stay = Mock(return_value="stay_result")

        # Act
        result = home()

        # Assert
        assert result == "stay_result"

    with app.test_request_context(method="POST", referrer="/drinkselector"):
        webwork.drink = Mock(return_value="drink_result")

        # Act
        result = home()

        # Assert
        assert result == "drink_result"

    with app.test_request_context(method="GET"):
        # Act
        result = home()

        # Assert
        assert result[1] == 404


def test_stays():
    # Arrange
    app = Flask(__name__)
    app.get_uid_from_cookie = Mock(return_value=1)
    dbdata.get_vname_by_id = Mock(return_value="VName")
    dbdata.get_nname_by_id = Mock(return_value="NName")
    dbdata.get_stay_counter_by_id = Mock(return_value=2)
    dbdata.get_stay_start_end_by_id = Mock(return_value=("start", "end"))

    with app.test_request_context():
        # Act
        result = stays()

        # Assert
        assert "stays.html" in result.response
        assert "VName" in result.response
        assert "NName" in result.response
        assert "start" in result.response
        assert "end" in result.response
        assert "counter=2" in result.response
