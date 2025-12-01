"""Swift iOS frontend generator."""

from adipose.core.generator import CodeGenerator


class SwiftGenerator(CodeGenerator):
    """Generate Swift iOS API client."""
    
    def generate(self):
        """Generate Swift frontend code."""
        print("\n=== Generating Swift iOS Frontend ===\n")
        
        self._generate_package_swift()
        self._generate_api_client()
        self._generate_models()
        self._generate_services()
        self._generate_auth_manager()
        self._generate_error_handler()
        self._generate_networking()
        self._generate_config()
        
        print("\n=== Swift iOS Frontend Generation Complete ===\n")
    
    def _generate_package_swift(self):
        """Generate Package.swift."""
        context = self.get_context()
        content = self.render_template('frontend/swift/Package.swift.j2', context)
        self.write_file('Package.swift', content)
    
    def _generate_api_client(self):
        """Generate base API client."""
        context = self.get_context()
        content = self.render_template('frontend/swift/APIClient.swift.j2', context)
        self.write_file('Sources/API/APIClient.swift', content)
    
    def _generate_models(self):
        """Generate model classes."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('frontend/swift/Model.swift.j2', ctx)
            self.write_file(f'Sources/Models/{model_name}.swift', content)
    
    def _generate_services(self):
        """Generate API services."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('frontend/swift/Service.swift.j2', ctx)
            self.write_file(f'Sources/Services/{endpoint.model}Service.swift', content)
    
    def _generate_auth_manager(self):
        """Generate authentication manager."""
        context = self.get_context()
        content = self.render_template('frontend/swift/AuthManager.swift.j2', context)
        self.write_file('Sources/Auth/AuthManager.swift', content)
    
    def _generate_error_handler(self):
        """Generate error handler."""
        context = self.get_context()
        content = self.render_template('frontend/swift/ErrorHandler.swift.j2', context)
        self.write_file('Sources/Utils/ErrorHandler.swift', content)
    
    def _generate_networking(self):
        """Generate networking utilities."""
        context = self.get_context()
        content = self.render_template('frontend/swift/NetworkManager.swift.j2', context)
        self.write_file('Sources/Networking/NetworkManager.swift', content)
    
    def _generate_config(self):
        """Generate configuration file."""
        context = self.get_context()
        content = self.render_template('frontend/swift/APIConfig.swift.j2', context)
        self.write_file('Sources/Config/APIConfig.swift', content)
