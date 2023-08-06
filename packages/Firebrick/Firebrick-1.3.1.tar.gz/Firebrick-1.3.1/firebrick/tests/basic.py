from firebrick.tests.test import *


class BasicGETViewTest(ResolveUrlTest, GetViewTest):
    pass


class BasicGETOr404ViewTest(ResolveUrlTest, GetViewOr404Test):
    pass


class BasicGETLoginRequired(ResolveUrlTest, GetLoginRequired):
    pass