import sys
import webtest

from pyramid.config import Configurator
from cubicweb.devtools.testlib import CubicWebTC

ACCEPTED_ORIGINS = ["example.com"]


class TestApp(webtest.TestApp):
    def __init__(self, *args, admin_login, admin_password, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_login = admin_login
        self.admin_password = admin_password
        self._ident_cookie = None
        self._csrf_token = None

    def reset(self):
        super().reset()
        self._ident_cookie = None
        self._csrf_token = None

    def post(
        self,
        route,
        params=None,
        do_not_grab_the_crsf_token=False,
        do_not_inject_origin=False,
        **kwargs,
    ):
        if params is None:
            params = {}

        if (
            isinstance(params, dict)
            and not do_not_grab_the_crsf_token
            and "csrf_token" not in params
        ):
            csrf_token = self.get_csrf_token()

            # "application/json" doesn't submit token in form params but as header value
            if kwargs.get("headers", {}).get("Content-Type") != "application/json":
                if "csrf_token" not in params:
                    params["csrf_token"] = csrf_token
            else:
                if "headers" in kwargs:
                    kwargs["headers"]["X-CSRF-Token"] = csrf_token
                else:
                    kwargs["headers"] = {"X-CSRF-Token": csrf_token}

        if not do_not_inject_origin:
            if "headers" in kwargs and "Origin" not in kwargs["headers"]:
                kwargs["headers"]["Origin"] = "https://" + ACCEPTED_ORIGINS[0]
            elif "headers" not in kwargs:
                kwargs["headers"] = {"Origin": "https://" + ACCEPTED_ORIGINS[0]}

        return super().post(route, params, **kwargs)

    def get_csrf_token(self):
        if "csrf_token" not in self.cookies:
            try:
                self.get("/")
            except Exception as e:
                sys.stderr.write(
                    f"ERROR: failed to do a GET on '/' to get the csrf token because: {e}\n"
                )
                raise

        return self.cookies["csrf_token"]

    def login(self, user=None, password=None, additional_arguments=None):
        """Log the current http session for the provided credential

        If no user is provided, admin connection are used.
        """
        if user is None:
            user = self.admin_login
            password = self.admin_password
        if password is None:
            password = user

        arguments = {"__login": user, "__password": password}
        if additional_arguments:
            arguments.update(additional_arguments)

        response = self.post("/login", arguments)

        assert response.status_int == 303

        return response

    def logout(self):
        return self.get("/logout")


class _BasePyramidCWTest(CubicWebTC):
    settings = {}

    @classmethod
    def init_config(cls, config):
        super().init_config(config)
        config.global_set_option("anonymous-user", "anon")

    def _generate_pyramid_config(self):
        settings = {
            "cubicweb.bwcompat": True,
            "cubicweb.session.secret": "test",
        }
        settings.update(self.settings)
        pyramid_config = Configurator(settings=settings)

        pyramid_config.registry["cubicweb.repository"] = self.repo
        pyramid_config.include("cubicweb.pyramid")

        self.includeme(pyramid_config)
        self.pyr_registry = pyramid_config.registry

        return pyramid_config

    def includeme(self, config):
        config.registry.settings["pyramid.csrf_trusted_origins"] = ACCEPTED_ORIGINS

    def login(self, user=None, password=None, **args):
        return self.webapp.login(user, password, additional_arguments=args)

    def logout(self):
        return self.webapp.logout()


class PyramidCWTest(_BasePyramidCWTest):
    def setUp(self):
        # Skip CubicWebTestTC setUp
        super().setUp()
        settings = {
            "cubicweb.bwcompat": True,
            "cubicweb.session.secret": "test",
        }
        settings.update(self.settings)
        pyramid_config = Configurator(settings=settings)

        pyramid_config.registry["cubicweb.repository"] = self.repo
        pyramid_config.include("cubicweb.pyramid")

        self.includeme(pyramid_config)
        self.pyr_registry = pyramid_config.registry
        self.webapp = TestApp(
            pyramid_config.make_wsgi_app(),
            extra_environ={"wsgi.url_scheme": "https"},
            admin_login=self.admlogin,
            admin_password=self.admpassword,
        )

    def tearDown(self):
        del self.webapp
        super().tearDown()
