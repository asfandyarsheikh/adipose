"""AvaloniaUI C# frontend generator."""

from adipose.core.generator import CodeGenerator


class AvaloniaUIGenerator(CodeGenerator):
    """Generate AvaloniaUI C# API client."""
    
    def generate(self):
        """Generate AvaloniaUI frontend code."""
        print("\n=== Generating AvaloniaUI Frontend ===\n")
        
        self._generate_csproj()
        self._generate_api_client()
        self._generate_models()
        self._generate_services()
        self._generate_auth_manager()
        self._generate_error_handler()
        self._generate_http_client()
        self._generate_config()
        
        print("\n=== AvaloniaUI Frontend Generation Complete ===\n")
    
    def _generate_csproj(self):
        """Generate .csproj file."""
        context = self.get_context()
        content = self.render_template('frontend/avaloniaui/project.csproj.j2', context)
        self.write_file(f'{self.config.project.name}Client.csproj', content)
    
    def _generate_api_client(self):
        """Generate base API client."""
        context = self.get_context()
        content = self.render_template('frontend/avaloniaui/ApiClient.cs.j2', context)
        self.write_file('API/ApiClient.cs', content)
    
    def _generate_models(self):
        """Generate model classes."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('frontend/avaloniaui/Model.cs.j2', ctx)
            self.write_file(f'Models/{model_name}.cs', content)
    
    def _generate_services(self):
        """Generate API services."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('frontend/avaloniaui/Service.cs.j2', ctx)
            self.write_file(f'Services/{endpoint.model}Service.cs', content)
    
    def _generate_auth_manager(self):
        """Generate authentication manager."""
        context = self.get_context()
        content = self.render_template('frontend/avaloniaui/AuthManager.cs.j2', context)
        self.write_file('Auth/AuthManager.cs', content)
    
    def _generate_error_handler(self):
        """Generate error handler."""
        context = self.get_context()
        content = self.render_template('frontend/avaloniaui/ErrorHandler.cs.j2', context)
        self.write_file('Utils/ErrorHandler.cs', content)
    
    def _generate_http_client(self):
        """Generate HTTP client factory."""
        context = self.get_context()
        content = self.render_template('frontend/avaloniaui/HttpClientFactory.cs.j2', context)
        self.write_file('API/HttpClientFactory.cs', content)
    
    def _generate_config(self):
        """Generate configuration file."""
        context = self.get_context()
        content = self.render_template('frontend/avaloniaui/ApiConfig.cs.j2', context)
        self.write_file('Config/ApiConfig.cs', content)
