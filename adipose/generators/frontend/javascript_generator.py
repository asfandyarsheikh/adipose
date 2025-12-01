"""JavaScript/TypeScript frontend generator."""

from adipose.core.generator import CodeGenerator


class JavaScriptGenerator(CodeGenerator):
    """Generate JavaScript/TypeScript API client."""
    
    def generate(self):
        """Generate JavaScript frontend code."""
        print("\n=== Generating JavaScript Frontend ===\n")
        
        self._generate_package_json()
        self._generate_api_client()
        self._generate_models()
        self._generate_services()
        self._generate_auth_manager()
        self._generate_error_handler()
        self._generate_config()
        self._generate_types()
        
        print("\n=== JavaScript Frontend Generation Complete ===\n")
    
    def _generate_package_json(self):
        """Generate package.json."""
        context = self.get_context()
        content = self.render_template('frontend/javascript/package.json.j2', context)
        self.write_file('package.json', content)
    
    def _generate_api_client(self):
        """Generate base API client."""
        context = self.get_context()
        content = self.render_template('frontend/javascript/api-client.ts.j2', context)
        self.write_file('src/api/client.ts', content)
    
    def _generate_models(self):
        """Generate model classes."""
        context = self.get_context()
        for model_name, model_config in self.config.models.items():
            ctx = {**context, 'model_name': model_name, 'model': model_config}
            content = self.render_template('frontend/javascript/model.ts.j2', ctx)
            self.write_file(f'src/models/{model_name}.ts', content)
    
    def _generate_services(self):
        """Generate API services."""
        context = self.get_context()
        for endpoint in self.config.endpoints:
            ctx = {**context, 'endpoint': endpoint}
            content = self.render_template('frontend/javascript/service.ts.j2', ctx)
            self.write_file(f'src/services/{endpoint.resource}Service.ts', content)
    
    def _generate_auth_manager(self):
        """Generate authentication manager."""
        context = self.get_context()
        content = self.render_template('frontend/javascript/auth-manager.ts.j2', context)
        self.write_file('src/auth/AuthManager.ts', content)
    
    def _generate_error_handler(self):
        """Generate error handler."""
        context = self.get_context()
        content = self.render_template('frontend/javascript/error-handler.ts.j2', context)
        self.write_file('src/utils/ErrorHandler.ts', content)
    
    def _generate_config(self):
        """Generate configuration file."""
        context = self.get_context()
        content = self.render_template('frontend/javascript/config.ts.j2', context)
        self.write_file('src/config/api.config.ts', content)
    
    def _generate_types(self):
        """Generate TypeScript type definitions."""
        context = self.get_context()
        content = self.render_template('frontend/javascript/types.ts.j2', context)
        self.write_file('src/types/index.ts', content)
