from kubernetes import client, config

def create_service(api_instance, namespace, service_name, target_port, port, service_type):
	# Define the Service manifest based on the chosen Service type
	service_manifest = {
    	"apiVersion": "v1",
    	"kind": "Service",
    	"metadata": {"name": service_name},
    	"spec": {
        	"selector": {"app": "your-app-label"},
        	"ports": [
            	{"protocol": "TCP", "port": port, "targetPort": target_port}
        	]
    	}
	}

	if service_type == "ClusterIP":
    	# No additional changes required for ClusterIP, it is the default type
    	pass
	elif service_type == "NodePort":
    	# Set the NodePort field to expose the service on a specific port on each node
    	service_manifest["spec"]["type"] = "NodePort"
	elif service_type == "LoadBalancer":
    	# Set the LoadBalancer type to get an external load balancer provisioned
    	service_manifest["spec"]["type"] = "LoadBalancer"
	elif service_type == "ExternalName":
    	# Set the ExternalName type to create an alias for an external service
    	service_manifest["spec"]["type"] = "ExternalName"
    	# Set the externalName field to the DNS name of the external service
    	service_manifest["spec"]["externalName"] = "my-external-service.example.com"

	api_response = api_instance.create_namespaced_service(
    	body=service_manifest,
    	namespace=namespace,
	)
	print(f"Service '{service_name}' created with type '{service_type}'. Status: {api_response.status}")


def list_services(api_instance, namespace):
	api_response = api_instance.list_namespaced_service(namespace=namespace)
	print("Existing Services:")
	for service in api_response.items:
    	print(f"Service Name: {service.metadata.name}, Type: {service.spec.type}")


def delete_service(api_instance, namespace, service_name):
	api_response = api_instance.delete_namespaced_service(
    	name=service_name,
    	namespace=namespace,
	)
	print(f"Service '{service_name}' deleted. Status: {api_response.status}")


if __name__ == "__main__":
