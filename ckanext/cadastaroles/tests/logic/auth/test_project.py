from .base import TestProjectBase


class TestProjectResource(TestProjectBase):
    def test_cadasta_upload_project_resource(self):
        self.assert_authorization_fails('cadasta_upload_project_resource',
                                        [None], self.project['id'],
                                        'project_id')

        self.assert_authorization_passes('cadasta_upload_project_resource',
                                         ['surveyor', 'admin', 'editor'],
                                         self.project['id'], 'project_id')

    def test_cadasta_delete_project_resource(self):
        self.assert_authorization_fails('cadasta_delete_project_resource',
                                        [None, 'surveyor'],
                                        self.project['id'], 'project_id')

        self.assert_authorization_passes('cadasta_delete_project_resource',
                                         ['admin', 'editor'],
                                         self.project['id'], 'project_id')


class TestProject(TestProjectBase):
    def test_cadasta_get_project_overview(self):
        self.assert_authorization_passes('cadasta_get_project_overview',
                                         [None, 'surveyor', 'admin', 'editor'],
                                         self.project['id'], 'id')
