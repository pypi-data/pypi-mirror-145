from airflow.providers.google.cloud.secrets.secret_manager import CloudSecretManagerBackend


class SecretManagerBackendAdapter(CloudSecretManagerBackend):

    def get_variable(self, key):
        key = key.replace('::', '-').replace(':', '-')

        return super().get_variable(key)
