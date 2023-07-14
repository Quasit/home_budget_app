# Kubernetes configuration files order

### To setup app with kubernetes and minikube follow below order

1. Start Minikube with your installed virtualization driver (check Minikube website for details - <a href="https://minikube.sigs.k8s.io/docs/drivers/">Minikube drivers</a>)
    ```sh
    minikube start --driver=**YOUR__DRIVER**   
    ```
2. Create ***0_postgres-secret.yaml*** file in kubernetes folder and fill it as below
   ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
        name: postgres-secret
    type: Opaque
    data:
        # Fill with your database credentials (ENCODED base64)
        postgres-username: **YOUR__DATABASE__USERNAME**
        postgres-password: **YOUR__DATABASE__PASSWORD**
   ```
3. Create ***1_app-secret.yaml*** file in kubernetes folder and fill it as below
   ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
        name: app-secret
    type: Opaque
    data:
        # Fill with your app secret key (ENCODED base64)
        app-secret-key: **YOUR__APP__SECRET__KEY**
   ```
4. Apply configuration files
    ```ssh
    kubectl apply -f ./kubernetes
    ```
5. Run Minikube Service (*Minikube service will open app in your browser*)
    ```ssh
    minikube service home-budget
    ```