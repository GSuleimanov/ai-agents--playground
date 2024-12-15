#!/usr/bin/env python3
import argparse
from credentials import CredentialsManager

def main():
    parser = argparse.ArgumentParser(description='Manage credentials for AI agents')
    parser.add_argument('action', choices=['set', 'get', 'delete'], help='Action to perform')
    parser.add_argument('service', choices=['ollama', 'openai', 'jira'], help='Service to manage')
    parser.add_argument('--username', help='Optional username (defaults to current user)')
    
    args = parser.parse_args()
    
    # Map service names to CredentialsManager constants
    service_map = {
        'ollama': CredentialsManager.OLLAMA_SERVICE,
        'openai': CredentialsManager.OPENAI_SERVICE,
        'jira': CredentialsManager.JIRA_SERVICE
    }
    
    service_name = service_map[args.service]
    
    try:
        if args.action == 'set':
            credential = CredentialsManager.get_or_prompt_credential(
                service_name,
                f"Enter {args.service} credential: ",
                args.username
            )
            print(f"{args.service} credential stored successfully")
        
        elif args.action == 'get':
            credential = CredentialsManager.get_credential(service_name, args.username)
            if credential:
                print(f"{args.service} credential: {credential}")
            else:
                print(f"No credential found for {args.service}")
        
        elif args.action == 'delete':
            CredentialsManager.delete_credential(service_name, args.username)
            print(f"{args.service} credential deleted")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 