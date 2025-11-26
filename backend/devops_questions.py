devops_questions = [
    {"question": "What is Git?", "answer": "Git is a distributed version control system."},
    {"question": "What is CI/CD?", "answer": "CI/CD automates build, test and deploy pipelines."},
    {"question": "What is Docker?", "answer": "Docker packages apps into containers."},
    {"question": "What is Kubernetes?", "answer": "Kubernetes orchestrates containers at scale."},
    
    {"question": "What are common Terraform challenges faced?", 
     "answer": "State file corruption, drift, dependency management, resource conflicts, secret management."},
    
    {"question": "How do you handle state file management in Terraform?", 
     "answer": "Use remote backends (e.g., S3, GCS, Azure Blob) to store the state centrally.\n"
               "Enable state locking (e.g., DynamoDB for S3) to prevent concurrent modifications.\n"
               "Versioning/backups to recover from corruption.\n"
               "Restrict access with IAM policies to secure sensitive information in the state."},
    
    {"question": "How do you manage secrets securely in Terraform?", 
     "answer": "Keep secrets out of code and state, leverage secret managers, and enforce encryption and access control."},
    
    {"question": "What is the difference between a Deployment and a StatefulSet in Kubernetes?", 
     "answer": "Deployment: Manages stateless pods. Pods are interchangeable; no stable identity or persistent storage required.\n"
               "StatefulSet: Manages stateful pods. Pods have stable network IDs, persistent storage, and ordered deployment/termination."},
    
    {"question": "What's the difference between COPY and ADD commands in Dockerfile?", 
     "answer": "Use COPY for simple copying; use ADD only when you need archive extraction or remote file fetch."},
    
    {"question": "How does the Kubernetes scheduler decide where to place pods?", 
     "answer": "Kubernetes scheduler decision factors:\n"
               "- Resource availability: CPU, memory, and other requested resources on nodes.\n"
               "- Node constraints: Labels, taints, and tolerations.\n"
               "- Affinity/Anti-affinity rules: Pod/node affinity preferences.\n"
               "- Pod priorities: Higher priority pods can preempt lower priority ones.\n"
               "- Topology & spreading: Spread pods across zones/nodes for high availability."},
    
    {"question": "What is DevOps?", "answer": "Collaboration between development and operations to deliver software faster and reliably."},
    
    {"question": "Benefits of DevOps?", "answer": "Faster delivery, improved quality, automation, better collaboration, continuous feedback."},
    
    {"question": "What is CI/CD?", 
     "answer": "Continuous Integration = code integration & build automation\n"
               "Continuous Deployment/Delivery = automated testing & deployment."},
    
    {"question": "Tools for CI/CD?", "answer": "Jenkins, GitLab CI, CircleCI, TravisCI, ArgoCD."},
    
    {"question": "What is version control?", "answer": "System to track code changes, e.g., Git."},
    
    {"question": "Git commands you must know?", "answer": "git clone, git pull, git commit, git push, git merge, git branch."},
    
    {"question": "What is containerization?", "answer": "Packaging app + dependencies in isolated containers (Docker)."},
    
    {"question": "Difference between VM and container?", 
     "answer": "VM = full OS, heavier; Container = lightweight, shares host OS."},
    
    {"question": "What is Docker?", "answer": "Tool to build, ship, and run containers."},
    
    {"question": "What is Kubernetes?", "answer": "Orchestrates containerized apps: deployment, scaling, networking."},
    
    {"question": "What is a pipeline?", "answer": "Sequence of stages to build, test, and deploy code."},
    
    {"question": "What is Infrastructure as Code (IaC)?", "answer": "Managing infrastructure via code/scripts, e.g., Terraform, CloudFormation."},
    
    {"question": "Benefits of IaC?", "answer": "Consistency, automation, versioning, easy replication."},
    
    {"question": "What is a shell?", "answer": "Interface to interact with OS, e.g., Bash."},
    
    {"question": "What is a kernel?", "answer": "Core of OS; manages hardware & resources."},
    
    {"question": "Basic file commands?", "answer": "ls = list, cd = change directory, pwd = print path."},
    
    {"question": "File manipulation commands?", "answer": "cp = copy, mv = move/rename, rm = remove, touch = create file"}
]
