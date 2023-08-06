from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import collective.embeddedpage


class CollectiveEmbeddedpageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.embeddedpage)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.embeddedpage:default")


EMBEDDEDPAGE_FIXTURE = CollectiveEmbeddedpageLayer()


EMBEDDEDPAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EMBEDDEDPAGE_FIXTURE,),
    name="CollectiveEmbeddedpageLayer:IntegrationTesting",
)


EMBEDDEDPAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EMBEDDEDPAGE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="CollectiveEmbeddedpageLayer:FunctionalTesting",
)


EMBEDDEDPAGE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EMBEDDEDPAGE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="CollectiveEmbeddedpageLayer:AcceptanceTesting",
)
